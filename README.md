# Kytos Orchestration (Prototype)

**Quantum-Optimized Kubernetes Pod Placement & Orchestration System**

## 1. 概要 (Overview)
**Kytos Orchestration** は、KubernetesクラスタにおけるPod配置（スケジューリング）を、量子アニーリング（およびイジングモデル）を用いて最適化するプロトタイプシステムです。
従来の「空いている場所に詰める（First Fit / Best Fit）」アルゴリズムではなく、クラスタ全体の状態をエネルギー関数として定義し、その最小値を探索することで「大域的最適解」を導き出します。

本プロトタイプは **FastAPI** を用いたマイクロサービスとして実装され、以下の3つの主要機能を提供します。

## 2. コア機能 (Core Features)

### Feature 1: 定期リバランサー (Periodic Rebalancer)
* **目的:** 稼働中のクラスタにおいて、断片化（フラグメンテーション）したリソースを整理し、ノードの集約率を高める。
* **ユースケース:** 定期実行（例: 1時間ごと）により、不要なノードを削除してクラウドコストを削減する。
* **最適化指標:**
    * ノード使用数の最小化
    * リソースの分散（または集約）
    * **マイグレーションコストの最小化**（現在動いている場所から移動させるとペナルティ）
    * **アンチアフィニティ**: 同じサービスのインスタンスは異なるノードに分散させる。

### Feature 2: マシン障害時の再配置 (Disaster Recovery Optimization)
* **目的:** ノードダウン発生時、退避が必要な複数のPodを、生き残ったノード群に対して「連鎖障害を起こさないように」安全に再配置する。
* **ユースケース:** スポットインスタンスの中断通知や、物理障害時の緊急退避。
* **最適化指標:**
    * 生き残りノードの負荷平準化（特定ノードへの集中回避）
    * 重要度（Priority）の高いPodの配置保証
    * **優先度制御**: Load Balancer等の重要コンポーネントを最優先し、冗長性のあるAPIインスタンスの優先度を下げる。

### Feature 3: コールドスタート配置最適化 (Cold Start Placement)
* **目的:** 新規Pod作成時（特にFaaSのコールドスタートやバッチジョブ開始時）に、将来の負荷や通信トポロジーを考慮した最適な初期配置を決定する。
* **ユースケース:** スパイクアクセス時のスケールアウト、重いバッチ処理の投入。
* **最適化指標:**
    * 通信レイテンシの最小化（トポロジー考慮）
    * 起動待ち時間の最小化

### Feature 4: オートスケーリング最適化 (Auto-scaling Optimization)
* **目的:** APIごとのリクエスト頻度とクラスタ全体の余裕容量に基づき、最適なインスタンス数を算出する。
* **ユースケース:** トラフィック変動への追従。
* **機能:**
    * APIごとのスケーリング有効化設定
    * リクエスト頻度に基づく必要数算出
    * クラスタ余裕容量（Margin）を考慮したスケールアウト抑制

## 定式化

$$\begin{array}{cccc}\text{Problem:} & \text{Kytos Orchestration} & & \\& & \min \quad \displaystyle \sum_{n = 0}^{\mathrm{len}\left(pods, 1\right) - 1} \left(\left(\sum_{p = 0}^{\mathrm{len}\left(pods, 0\right) - 1} x_{p, n} \cdot cpu_req_{p} \cdot cpu_cap_{n}^{(-1)}\right)^{2} + \left(\sum_{p = 0}^{\mathrm{len}\left(pods, 0\right) - 1} x_{p, n} \cdot mem_req_{p} \cdot mem_cap_{n}^{(-1)}\right)^{2}\right) \cdot load_balance_weight + \sum_{p = 0}^{\mathrm{len}\left(pods, 0\right) - 1} \sum_{n = 0}^{\mathrm{len}\left(pods, 1\right) - 1} x_{p, n} \cdot move_cost_{p, n} \cdot move_cost_weight + \sum_{n = 0}^{\mathrm{len}\left(pods, 1\right) - 1} \sum_{p = 0}^{\mathrm{len}\left(pods, 0\right) - 1} \sum_{p = 0}^{\mathrm{len}\left(pods, 0\right) - 1} anti_affinity_{p, p} \cdot x_{p, n} \cdot x_{p, n} \cdot anti_affinity_weight + \sum_{p = 0}^{\mathrm{len}\left(pods, 0\right) - 1} - desire_{p} \cdot \sum_{n = 0}^{\mathrm{len}\left(pods, 1\right) - 1} x_{p, n} \cdot desire_weight & \\\text{{s.t.}} & & & \\ & \text{cpu\_limit} & \displaystyle \sum_{p = 0}^{\mathrm{len}\left(pods, 0\right) - 1} x_{p, n} \cdot cpu_req_{p} \leq cpu_cap_{n} & \forall n \in \left\{0,\ldots,\mathrm{len}\left(pods, 1\right) - 1\right\} \\ & \text{mem\_limit} & \displaystyle \sum_{p = 0}^{\mathrm{len}\left(pods, 0\right) - 1} x_{p, n} \cdot mem_req_{p} \leq mem_cap_{n} & \forall n \in \left\{0,\ldots,\mathrm{len}\left(pods, 1\right) - 1\right\} \\ & \text{one\_hot\_relaxed} & \displaystyle \sum_{n = 0}^{\mathrm{len}\left(pods, 1\right) - 1} x_{p, n} \leq 1 & \forall p \in \left\{0,\ldots,\mathrm{len}\left(pods, 0\right) - 1\right\} \\\text{{where}} & & & \\& x & 2\text{-dim binary variable}& \text{PodのNode割り当て}\\\end{array}$$

## 3. システムアーキテクチャ (Architecture)

```mermaid
graph LR
    User[User / K8s Event] -->|Request| API[Kytos API (FastAPI)]
    API -->|Input Data| Solver[Annealing Solver]
    Solver -->|QUBO Formulation| QA[Quantum/Digital Annealer]
    QA -->|Optimal State| Solver
    Solver -->|JSON Response| API
    API -->|Action| K8s[Kubernetes Cluster]
```

* **API Layer:** FastAPI (Python)
* **Solver Layer:** OpenJij (シミュレータ) または D-Wave Ocean SDK
* **Data Model:** Pydantic

## 4. API仕様 (API Specification)

### 共通データ構造 (Request Body)

全ての最適化エンドポイントは、現在のクラスタ状態（Nodes, Pods）を受け取ります。

```json
{
  "nodes": [
    {"id": "node-1", "cpu_capacity": 4000, "mem_capacity": 16000, "current_load": {...}},
    ...
  ],
  "pods": [
    {"id": "pod-a", "cpu_request": 500, "mem_request": 1024, "current_node": "node-1"},
    ...
  ]
}
```

### Endpoints

#### `POST /optimize/rebalance`

  * **Input:** 全ノードと全Podの状態。
  * **Logic:** 全Podを再配置対象として計算するが、`current_node` と異なる配置になった場合、移動コスト項を加算する。
  * **Output:** 移動すべきPodとその移動先ノードのリスト。

#### `POST /optimize/recovery`

  * **Input:** 生存ノードのリスト、退避が必要な（死んだノードにいた）Podリスト。
  * **Logic:** PodごとのPriorityを重み付けし、絶対に配置できないPod（容量オーバー）が出た場合はPriorityの低いものを切り捨てる判断を行う。
  * **Output:** 退避Podごとの新しい配置先。

#### `POST /optimize/placement`

  * **Input:** 新規作成予定のPodスペック、現在のノード状態。
  * **Logic:** 新規Podを入れた後のシステム全体のエネルギー（負荷分散など）が最も低くなるノードを選択。
  * **Output:** 対象Podの推奨ノードID。

#### `POST /optimize/auto_scale`

  * **Input:** クラスタ状態（Nodes, Pods）およびサービス定義（Services）。
  * **Logic:** 各サービスの現在のリクエストレートとターゲットレートを比較し、推奨レプリカ数を算出。クラスタ全体のCPU余裕率が低い場合、スケールアウトを抑制する。
  * **Output:** サービスごとの推奨レプリカ数（Scaling Actions）。

## 5. 数理モデル (Mathematical Model / QUBO)

本システムでは、問題を **QUBO (Quadratic Unconstrained Binary Optimization)** として定式化します。

**決定変数:**
$$x_{i,j} \in \{0, 1\}$$
（Pod $i$ が ノード $j$ に配置される場合 1、そうでない場合 0）

**ハミルトニアン（目的関数）:**
$$H = A \cdot H_{constraint} + B \cdot H_{load} + C \cdot H_{cost} + D \cdot H_{affinity}$$

1.  **制約項 ($H_{constraint}$):**
      * One-hot制約: 各Podは必ず1つのノードに配置される。
      * 容量制約: 各ノードのリソース使用量は上限を超えない。
2.  **負荷項 ($H_{load}$):**
      * 各ノードの使用率の分散を最小化（平準化）、またはノード使用有無の総和を最小化（集約）。
3.  **コスト項 ($H_{cost}$):**
      * 移動コスト: 現在のノード $j_{current}$ と異なる $j_{new}$ を選んだ場合、ペナルティを加算。
      * **優先度重み付け**: 重要度の高いPod（Load Balancer等）の移動コストを高く設定し、配置を安定させる。
4.  **アンチアフィニティ項 ($H_{affinity}$):**
      * 同じサービスに属するPodペア $i, p$ が同じノード $j$ に配置された場合、ペナルティを加算。
      * $\sum_{j} \sum_{i<p, service(i)=service(p)} x_{i,j} x_{p,j}$

## 6. 技術スタック (Tech Stack)

  * **Language:** Python 3.10+
  * **Web Framework:** FastAPI
  * **Optimization Library:**
      * `openjij` (ローカルでのシミュレーテッド・アニーリング用 / プロトタイプ段階で使用)
      * `dimod`, `dwave-ocean-sdk` (将来的なD-Wave接続用)
  * **Dependency Management:** uv

## 7. 開発・実行手順 (How to Run)

1.  依存ライブラリのインストール
    ```bash
    uv sync
    ```
2.  サーバー起動
    ```bash
    uv run uvicorn main:app --reload
    ```
3.  Docs確認
    `http://localhost:8000/docs` にアクセスし、Swagger UIからAPIをテストする。
