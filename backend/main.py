from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from zoneinfo import ZoneInfo

from src.models import OptimizationRequest, OptimizationResponse
from src.solver import solve_placement

app = FastAPI(title="Kytos Orchestration API")

# CORS
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "https://kytos.o-o-o.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.now(ZoneInfo("Asia/Tokyo")),
        "version": "0.1.0",
        "detail": "Kytos Orchestration running",
    }


@app.post("/optimize", response_model=OptimizationResponse)
def optimize(request: OptimizationRequest):
    """
    クラスタの状態を受け取り、ポッドの最適配置を計算して返す。
    新規配置したいポッドは、current_nodeをNoneにする。

    ```
    {
        state: {
            nodes: {
                id: str,
                cpu_capacity: float,
                mem_capacity: float,
                cpu_usage?: float = 0,
                mem_usage?: float = 0,
            }[],
            pods: {
                id: str,
                cpu_usage: float,
                mem_usage: float,
                current_node?: str | null,
                service?: str | null,
                priority?: float = 1,
            }[],
            services: {
                id: str,
                load_balancer_pod: str,
                auto_scaling_enabled?: bool = false,
                min_replicas?: int = 1,
                max_replicas?: int | null,
                current_request_rate?: float = 0.0,
                target_request_rate_per_pod?: float = 100.0,
                priority?: float = 10,
            }[]
        },
        settings?: {
            load_balance_weight?: float = 5.0,
            move_cost_weight?: float = 1.0,
            anti_affinity_weight?: float = 5.0,
            desire_weight?: float = 10.0,
            cpu_limit_weight?: float = 1.0,
            mem_limit_weight?: float = 1.0,
            one_hot_relaxed_weight?: float = 20.0,
            num_reads?: int = 100,
        }
    }
    ```
    """
    return solve_placement(request.state, request.settings)
