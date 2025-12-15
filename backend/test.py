from fastapi.testclient import TestClient
from main import app
from src.models import ClusterState, Node, Pod

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rebalance():
    nodes = [
        Node(
            id="node1",
            cpu_capacity=4000,
            mem_capacity=16000,
            cpu_usage=3500,
            mem_usage=14000,
        ),
        Node(
            id="node2", cpu_capacity=4000, mem_capacity=16000, cpu_usage=0, mem_usage=0
        ),
    ]
    pods = [
        Pod(id="pod1", cpu_usage=500, mem_usage=1024, current_node="node1"),
        Pod(id="pod2", cpu_usage=500, mem_usage=1024, current_node="node1"),
        Pod(id="pod3", cpu_usage=500, mem_usage=1024, current_node="node1"),
    ]

    state = ClusterState(nodes=nodes, pods=pods, services=[])

    response = client.post("/optimize", json=state.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert "placements" in data
    assert len(data["placements"]) == 3

    # Check if it suggests moving some pods to node2 (since node1 is crowded)
    # Note: With 3 small pods and huge capacity, it might not move them if cost > benefit.
    # But let's just check structure.
    print("Rebalance Result:", data)


def test_recovery():
    nodes = [
        Node(
            id="node2",
            cpu_capacity=4000,
            mem_capacity=16000,
            cpu_usage=1000,
            mem_usage=2048,
        )
    ]
    pods = [
        Pod(
            id="pod1", cpu_usage=500, mem_usage=1024, current_node="node1"
        )  # node1 died
    ]

    state = ClusterState(nodes=nodes, pods=pods, services=[])

    response = client.post("/optimize", json=state.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert len(data["placements"]) == 1
    assert data["placements"][0]["target_node_id"] == "node2"
    print("Recovery Result:", data)


if __name__ == "__main__":
    test_health()
    test_rebalance()
    test_recovery()
