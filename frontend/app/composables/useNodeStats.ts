export const useNodeStats = (nodesData: NodesPodsServices) => {
  const isLoadBalancer = (pod: Pod): boolean => {
    const service = nodesData.services.find((s) => s.id === pod.service);
    return service?.load_balancer_pod === pod.id;
  };

  const calculatePercentage = (usage: number, capacity: number): number => {
    if (capacity === 0) return 0;
    return Math.round((usage / capacity) * 100);
  };

  const getNodeStats = (
    node: ComputeNode,
  ): {
    cpu_capacity: number;
    mem_capacity: number;
    cpu: number;
    memory: number;
  } => {
    return {
      cpu_capacity: node.cpu_capacity,
      mem_capacity: node.mem_capacity,
      cpu: calculatePercentage(node.cpu_usage || 0, node.cpu_capacity),
      memory: calculatePercentage(node.mem_usage || 0, node.mem_capacity),
    };
  };

  const getPodCpuPercentage = (pod: Pod): number => {
    const node = nodesData.nodes.find((n) => n.id === pod.current_node);
    if (!node || node.cpu_capacity === 0) return 0;
    return Math.round((pod.cpu_usage / node.cpu_capacity) * 100);
  };

  const getPodsForNode = (nodeId: string | null): Pod[] => {
    return nodesData.pods.filter((pod) => pod.current_node === nodeId);
  };

  const getNodeforPod = (pod: Pod): ComputeNode | null => {
    const node = nodesData.nodes.find((n) => n.id === pod.current_node);
    return node || null;
  };

  return {
    isLoadBalancer,
    getNodeStats,
    getPodCpuPercentage,
    getPodsForNode,
    getNodeforPod,
  };
};
