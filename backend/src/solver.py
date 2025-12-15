from fastapi import HTTPException
import jijmodeling as jm
from ommx.v1 import Instance
from ommx_openjij_adapter import OMMXOpenJijSAAdapter

from .scaling import auto_scale_desired_exsistence
from .models import (
    Action,
    ActionType,
    AnealingSettings,
    ClusterState,
    OptimizationResponse,
    Pod,
)
from typing import List, Dict, Any


def _define_problem() -> jm.Problem:
    """
    数理最適化モデルを定義します。
    """
    problem = jm.Problem("Kytos Orchestration")

    # 重み
    load_balance_weight = jm.Placeholder(
        "load_balance_weight", description="負荷分散の重み"
    )
    move_cost_weight = jm.Placeholder(
        "move_cost_weight", description="移動コストの重み"
    )
    anti_affinity_weight = jm.Placeholder(
        "anti_affinity_weight", description="アンチアフィニティの重み"
    )
    desire_weight = jm.Placeholder("desire_weight", description="配置意欲の重み")

    # 現在の配置
    pods = jm.Placeholder("pods", ndim=2, description="ポッドの現在の配置")
    num_pods = pods.len_at(0)
    num_nodes = pods.len_at(1)

    # リソース情報
    cpu_req = jm.Placeholder(
        "cpu_req", shape=(num_pods,), description="各PodのCPU要求量"
    )
    mem_req = jm.Placeholder(
        "mem_req", shape=(num_pods,), description="各Podのメモリ要求量"
    )

    cpu_cap = jm.Placeholder(
        "cpu_cap", shape=(num_nodes,), description="各NodeのCPU容量"
    )
    mem_cap = jm.Placeholder(
        "mem_cap", shape=(num_nodes,), description="各Nodeのメモリ容量"
    )

    move_cost = jm.Placeholder(
        "move_cost", shape=(num_pods, num_nodes), description="Podの移動コスト"
    )

    anti_affinity = jm.Placeholder(
        "anti_affinity",
        shape=(num_pods, num_pods),
        description="同じサービスのPodを分散配置する",
    )

    desire = jm.Placeholder(
        "desire", shape=(num_pods,), description="Podの作成,削除提案"
    )

    # 変数定義
    x = jm.BinaryVar("x", shape=(num_pods, num_nodes), description="PodのNode割り当て")
    p = jm.Element("p", (0, num_pods), description="Podのインデックス")
    n = jm.Element("n", (0, num_nodes), description="Nodeのインデックス")

    # 制約条件
    # 各Podは最大1つのNodeに割り当てる (Relaxed One-hot制約)
    # desireの値に応じて配置するかどうかを決定するため、必ずしも1つに割り当てる必要はない
    problem += jm.Constraint("one_hot_relaxed", jm.sum(n, x[p, n]) <= 1, forall=[p])

    # リソース容量制約 (CPU, Memory)
    problem += jm.Constraint(
        "cpu_limit", jm.sum(p, x[p, n] * cpu_req[p]) <= cpu_cap[n], forall=[n]
    )
    problem += jm.Constraint(
        "mem_limit", jm.sum(p, x[p, n] * mem_req[p]) <= mem_cap[n], forall=[n]
    )

    # 目的関数
    # 負荷分散 (使用率の二乗和の最小化)
    cpu_load = jm.sum(p, x[p, n] * cpu_req[p])
    mem_load = jm.sum(p, x[p, n] * mem_req[p])

    problem += (
        jm.sum(
            n,
            (cpu_load / cpu_cap[n]) ** 2 + (mem_load / mem_cap[n]) ** 2,
        )
        * 10 * load_balance_weight
    )

    # 移動コスト
    problem += jm.sum([p, n], x[p, n] * move_cost[p, n]) * move_cost_weight

    # アンチアフィニティ (同じサービスの分散配置)
    # i と p が同じサービスなら anti_affinity[i, p] > 0
    # 同じノード j に配置されると x[i,j]*x[p,j] = 1
    p2 = jm.Element("p", (0, num_pods))
    problem += (
        jm.sum([n, p, p2], anti_affinity[p, p2] * x[p, n] * x[p2, n])
        * anti_affinity_weight
    )

    # Desire (配置意欲)
    # desireが高い(1.0)場合は配置することでエネルギーを下げる (-1 * 1.0 * 1 = -1)
    # desireが低い(-1.0)場合は配置するとエネルギーが上がる (-1 * -1.0 * 1 = +1) -> 配置しない(0)方が良い
    problem += jm.sum(p, -1.0 * desire[p] * jm.sum(n, x[p, n])) * desire_weight

    # print(problem._repr_latex_())

    return problem


def _prepare_data(
    state: ClusterState, settings: AnealingSettings
) -> tuple[Dict[str, Any], List[Pod]]:
    """
    ソルバーに渡すデータを準備します。
    """
    pods, desires = auto_scale_desired_exsistence(state)

    # 移動コストの計算
    m_costs = []
    for pod in pods:
        row = []
        for node in state.nodes:
            if pod.current_node is None:
                row.append(0.0)
                continue

            if pod.current_node != node.id:
                row.append(
                    0.5 * pod.priority
                    + pod.mem_usage * 0.00001
                    + pod.cpu_usage * 0.0001
                )  # 基本移動コスト
                continue

            row.append(0.0)
        m_costs.append(row)

    # アンチアフィニティ行列の作成
    # 同じ service_name を持つPodペアに対してペナルティを設定
    num_pods = len(pods)
    affinity_matrix = [[0.0] * num_pods for _ in range(num_pods)]
    for i in range(num_pods):
        for k in range(
            i + 1, num_pods
        ):  # 上三角だけで十分だが、式は全和なので両方埋めるか、i<kで制限するか。
            # jm.sum([j, i, p]) は全組み合わせ走るので、重複カウントされる。
            # x[i]*x[p] と x[p]*x[i] は同じ。
            # 対称行列にしておけば係数が2倍になるだけなのでOK。
            if (
                pods[i].service
                and pods[k].service
                and pods[i].service == pods[k].service
            ):
                affinity_matrix[i][k] = 1.0
                affinity_matrix[k][i] = 1.0

    return {
        "load_balance_weight": settings.load_balance_weight,
        "move_cost_weight": settings.move_cost_weight,
        "anti_affinity_weight": settings.anti_affinity_weight,
        "desire_weight": settings.desire_weight,
        "pods": [
            [1 if pod.current_node == node.id else 0 for node in state.nodes]
            for pod in pods
        ],
        "cpu_req": [p.cpu_usage for p in pods],
        "mem_req": [p.mem_usage for p in pods],
        "cpu_cap": [n.cpu_capacity for n in state.nodes],
        "mem_cap": [n.mem_capacity for n in state.nodes],
        "move_cost": m_costs,
        "anti_affinity": affinity_matrix,
        "desire": desires,
    }, pods


def _decode_result(
    response: dict[tuple[int, ...], float],
    state: ClusterState,
) -> tuple[List[Pod], List[Action]]:
    """
    ソルバーの結果をデコードしてレスポンス形式に変換します。
    """
    num_pods = len(state.pods)
    num_nodes = len(state.nodes)

    actions: List[Action] = []
    new_pods_list: List[Pod] = []

    for p in range(num_pods):
        pod = state.pods[p]
        fond_node = False

        for n in range(num_nodes):
            if response.get((p, n), 0) == 1:
                target_node = state.nodes[n]
                if pod.id in [p.id for p in new_pods_list]:
                    print("Warning: Pod assigned to multiple nodes!")
                    break

                new_pods_list.append(
                    Pod(
                        id=pod.id,
                        cpu_usage=pod.cpu_usage,
                        mem_usage=pod.mem_usage,
                        current_node=target_node.id,
                        service=pod.service,
                        priority=pod.priority,
                    )
                )
                fond_node = True

                if pod.current_node is None:
                    actions.append(
                        Action(
                            pod_id=pod.id,
                            target_node_id=target_node.id,
                            action=ActionType.CREATE,
                        )
                    )

                elif pod.current_node != target_node.id:
                    actions.append(
                        Action(
                            pod_id=pod.id,
                            target_node_id=target_node.id,
                            action=ActionType.MOVE,
                        )
                    )

                else:
                    actions.append(
                        Action(
                            pod_id=pod.id,
                            target_node_id=target_node.id,
                            action=ActionType.KEEP,
                        )
                    )

        if not fond_node:
            # 配置されなかったPodは削除扱い
            actions.append(
                Action(
                    pod_id=pod.id,
                    action=ActionType.REMOVE,
                )
            )

    return new_pods_list, actions


def solve_placement(
    state: ClusterState,
    settings: AnealingSettings = AnealingSettings(),
) -> OptimizationResponse:
    if not state.nodes or not state.pods:
        raise HTTPException(
            status_code=400, detail="ノードまたはポッドの情報が不足しています。"
        )

    # 問題定義
    problem = _define_problem()

    # データ準備
    instance_data, pods = _prepare_data(state, settings)

    # QUBO変換と解決
    interpreter = jm.Interpreter(instance_data)
    instance: Instance = interpreter.eval_problem(problem)

    multipliers = {
        "cpu_limit": settings.cpu_limit_weight,  # Weak constraint (penalty ~ 1.0 * excess^2)
        "mem_limit": settings.mem_limit_weight,  # Weak constraint
        "one_hot_relaxed": settings.one_hot_relaxed_weight,  # Stronger than desire (10.0) to prevent double assignment
    }

    penalty_weights: dict[int, float] = {}
    for constraint in instance.constraints:
        if constraint.name in multipliers:
            penalty_weights[constraint.id] = multipliers[constraint.name]

    result = OMMXOpenJijSAAdapter.sample(
        instance, num_reads=settings.num_reads, penalty_weights=penalty_weights
    )
    try:
        best_sample = result.best_feasible_unrelaxed.extract_decision_variables("x")
        energy = result.best_feasible_unrelaxed.objective
    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="有効な解が見つかりませんでした。制約条件が厳しすぎるか、試行回数が不足している可能性があります。",
        )

    # 結果のデコード
    state.pods = pods  # 更新されたPodリストをstateにセット
    new_pods, actions = _decode_result(best_sample, state)

    return OptimizationResponse(pods=new_pods, placements=actions, energy=energy)
