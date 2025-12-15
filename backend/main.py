import os
from fastapi import FastAPI, HTTPException
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
]
vercel_origin = os.environ.get("FRONTEND_ORIGIN")
if vercel_origin:
    origins.append(vercel_origin)

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
    """
    try:
        return solve_placement(request.state, request.settings)
    except HTTPException as e:
        return e
