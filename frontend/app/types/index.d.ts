interface Service {
  id: string;
  load_balancer_pod: string; // id of load balancer
  auto_scaling_enabled?: boolean;
  min_replicas?: number;
  max_replicas?: number | null;
  current_request_rate?: Float;
  target_request_rate_per_pod?: Float;
  priority?: number;
}

interface Pod {
  id: string;
  cpu_usage: number;
  mem_usage: number;
  current_node?: string | null; // id of the node
  service?: string | null; // id of the service
  priority?: number;
}

interface ComputeNode {
  id: string;
  cpu_capacity: number;
  mem_capacity: number;
  cpu_usage?: number;
  mem_usage?: number;
}

interface NodesPodsServices {
  nodes: ComputeNode[];
  pods: Pod[];
  services: Service[];
}

interface PodsResponse {
  id: string;
  cpu_usage: number;
  mem_usage: number;
  current_node: string;
  service: string;
  priority: number;
}

interface PlacementResponse {
  pod_id: string;
  target_node_id: string;
  action: "move";
}

interface AnnealingResponse {
  pods: PodsResponse[];
  placements: PlacementResponse[];
  energy: number;
}
