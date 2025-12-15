import math
from typing import List
import uuid
from .models import ClusterState, Pod


def auto_scale_desired_exsistence(state: ClusterState) -> tuple[list[Pod], list[float]]:
    """
    Generates a list of pods including existing ones and new candidates based on scaling needs.
    Assigns 'desire' value to each pod.
    """
    # Calculate margins
    total_cpu_capacity = sum(n.cpu_capacity for n in state.nodes)
    total_mem_capacity = sum(n.mem_capacity for n in state.nodes)
    current_cpu_usage = sum(p.cpu_usage for p in state.pods)
    current_mem_usage = sum(p.mem_usage for p in state.pods)

    cpu_margin = 1.0 - (current_cpu_usage / total_cpu_capacity)
    mem_margin = 1.0 - (current_mem_usage / total_mem_capacity)
    cluster_margin = (cpu_margin + mem_margin) / 2.0

    # Group pods by service
    pods_by_service = {}
    for p in state.pods:
        if p.service:
            pods_by_service.setdefault(p.service, []).append(p)

    pods: List[Pod] = []
    desires: List[float] = []

    for service in state.services:
        current_pods: List[Pod] = pods_by_service.get(service.id, [])
        current_count = len(current_pods)

        cpu_usage_avg = (
            sum(p.cpu_usage for p in current_pods) / current_count
            if current_count > 0
            else 0
        )

        mem_usage_avg = (
            sum(p.mem_usage for p in current_pods) / current_count
            if current_count > 0
            else 0
        )

        # Calculate needed
        needed = math.ceil(
            service.current_request_rate / service.target_request_rate_per_pod
        )
        desired_count = max(needed, service.min_replicas)  # サービスごとの最小値保証
        desired_count = max(desired_count, current_count - 2)  # 急激なスケールイン防止
        desired_count = min(
            desired_count, current_count + 2
        )  # 急激なスケールアウト防止
        if service.max_replicas is not None:
            desired_count = min(
                desired_count, service.max_replicas
            )  # サービスごとの最大値保証

        # Calculate urgency (0 to 1)
        if current_count > 0:
            urgency = min(1.0, max(0.0, (needed - current_count) / current_count))
        else:
            urgency = 1.0 if desired_count > 0 else 0.0

        # Calculate desire for new pods
        # High urgency -> close to 1. Low margin -> close to -1.
        new_pod_desire = urgency - (1.0 - cluster_margin)
        new_pod_desire = max(-1.0, min(1.0, new_pod_desire))

        if desired_count > current_count:
            # Scale out: Keep existing, add new
            for p in current_pods:
                pods.append(p)
                desires.append(1.0)  # Strong desire to keep

            num_to_add = desired_count - current_count

            for i in range(num_to_add):
                new_pod = Pod(
                    id=f"{service.id}-{uuid.uuid4().hex[:6]}",
                    cpu_usage=cpu_usage_avg,
                    mem_usage=mem_usage_avg,
                    service=service.id,
                    priority=service.priority,
                )
                pods.append(new_pod)
                desires.append(new_pod_desire)

        elif desired_count < current_count:
            # Scale in: Reduce desire for excess pods
            for i, p in enumerate(current_pods):
                if i < desired_count:
                    pods.append(p)
                    desires.append(1.0)  # Strong desire to keep
                else:
                    desires.append(-1.0)  # Strong desire to remove
        else:
            # Keep as is
            for p in current_pods:
                pods.append(p)
                desires.append(1.0)  # Strong desire to keep
    for p in state.pods:
        if p not in pods:
            pods.append(p)
            desires.append(1.0)  # Strong desire to keep

    return pods, desires
