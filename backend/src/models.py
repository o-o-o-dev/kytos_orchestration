from typing import List, Optional


from pydantic import BaseModel


from enum import Enum


class ServiceProfile(BaseModel):
    id: str
    load_balancer_pod: str
    auto_scaling_enabled: bool = False
    min_replicas: int = 1
    max_replicas: Optional[int] = None
    current_request_rate: float = 0.0
    target_request_rate_per_pod: float = 100.0
    priority: float = 10  # Higher is more important


class Node(BaseModel):
    id: str
    cpu_capacity: float  # in milliCPU
    mem_capacity: float  # in MiB
    cpu_usage: float = 0  # in milliCPU
    mem_usage: float = 0  # in MiB


class Pod(BaseModel):
    id: str
    cpu_usage: float  # in milliCPU
    mem_usage: float  # in MiB
    current_node: Optional[str] = None
    service: Optional[str] = None  # Link to ServiceProfile
    priority: float = 1  # Higher is more important (Used if service_name is not found)


class ClusterState(BaseModel):
    nodes: List[Node]
    pods: List[Pod]
    services: List[ServiceProfile]


class AnealingSettings(BaseModel):
    load_balance_weight: float = 5.0
    move_cost_weight: float = 1.8
    move_cost_resource_coeff: float = 0.7
    anti_affinity_weight: float = 1.0
    desire_weight: float = 1.0
    cpu_limit_weight: float = 0.5
    mem_limit_weight: float = 0.5
    one_hot_relaxed_weight: float = 50.0
    cpu_digit_adjustment: float = -1.5
    mem_digit_adjustment: float = -3
    num_reads: int = 100


class OptimizationRequest(BaseModel):
    state: ClusterState
    settings: AnealingSettings = AnealingSettings()


class ActionType(Enum):
    MOVE = "move"
    KEEP = "keep"
    CREATE = "create"
    REMOVE = "remove"


class Action(BaseModel):
    pod_id: str
    target_node_id: Optional[str] = None
    action: ActionType


class OptimizationResponse(BaseModel):
    pods: List[Pod]
    placements: List[Action]
    energy: float
