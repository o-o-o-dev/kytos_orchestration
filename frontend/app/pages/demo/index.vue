<script setup lang="ts">
const NodesPodsServicesRef = ref<NodesPodsServices>({
    nodes: [
        {
            id: "node-1",
            cpu_capacity: 128,
            mem_capacity: 4096,
            cpu_usage: 51,
            mem_usage: 1700,
        },
        {
            id: "node-2",
            cpu_capacity: 96,
            mem_capacity: 2048,
            cpu_usage: 36,
            mem_usage: 1200,
        },
        {
            id: "node-3",
            cpu_capacity: 64,
            mem_capacity: 4096,
            cpu_usage: 27,
            mem_usage: 900,
        },
        {
            id: "node-4",
            cpu_capacity: 64,
            mem_capacity: 2048,
            cpu_usage: 9,
            mem_usage: 300,
        },
    ],
    pods: [
        // Service A
        {
            id: "pod-lb-a",
            cpu_usage: 15,
            mem_usage: 500,
            current_node: "node-1",
            service: "service-a",
            priority: 8,
        },
        {
            id: "pod-a-1",
            cpu_usage: 18,
            mem_usage: 600,
            current_node: "node-1",
            service: "service-a",
            priority: 6,
        },
        {
            id: "pod-a-2",
            cpu_usage: 18,
            mem_usage: 600,
            current_node: "node-2",
            service: "service-a",
            priority: 6,
        },
        {
            id: "pod-a-3",
            cpu_usage: 18,
            mem_usage: 600,
            current_node: "node-3",
            service: "service-a",
            priority: 6,
        },
        // Service B
        {
            id: "pod-lb-b",
            cpu_usage: 18,
            mem_usage: 600,
            current_node: "node-2",
            service: "service-b",
            priority: 6,
        },
        {
            id: "pod-b-1",
            cpu_usage: 9,
            mem_usage: 300,
            current_node: "node-1",
            service: "service-b",
            priority: 3,
        },
        {
            id: "pod-b-2",
            cpu_usage: 9,
            mem_usage: 300,
            current_node: "node-3",
            service: "service-b",
            priority: 3,
        },
        {
            id: "pod-b-3",
            cpu_usage: 9,
            mem_usage: 300,
            current_node: "node-4",
            service: "service-b",
            priority: 3,
        },
    ],
    services: [
        {
            id: "service-a",
            load_balancer_pod: "pod-lb-a",
            auto_scaling_enabled: true,
            current_request_rate: 80,
            priority: 8,
        },
        {
            id: "service-b",
            load_balancer_pod: "pod-lb-b",
            auto_scaling_enabled: true,
            current_request_rate: 40,
            priority: 6,
        },
    ],
});

const podSimulationStates = new Map<
    string,
    {
        trend: -1 | 0 | 1;
        trendDuration: number;
        cpuUsageHistory: number[];
        memoryToCpuRatio: number;
    }
>();

const initialData = NodesPodsServicesRef.value;
initialData.pods.forEach((pod) => {
    podSimulationStates.set(pod.id, {
        trend: 0,
        trendDuration: 0,
        cpuUsageHistory: [pod.cpu_usage],
        memoryToCpuRatio:
            pod.cpu_usage > 0 ? pod.mem_usage / pod.cpu_usage : 10,
    });
});

const outageNodes = ref(new Set<string>());

const toggleNodeOutage = (nodeId: string) => {
    const node = NodesPodsServicesRef.value.nodes.find((n) => n.id === nodeId);
    if (!node) return;

    const newOutageSet = new Set(outageNodes.value);

    if (newOutageSet.has(nodeId)) {
        newOutageSet.delete(nodeId);
        toast.add({
            title: "Node Restored",
            description: `Node ${nodeId} is back online.`,
            icon: "i-heroicons-check-circle",
            color: "success",
        });
    } else {
        newOutageSet.add(nodeId);
        toast.add({
            title: "Node Outage",
            description: `Node ${nodeId} is now offline.`,
            icon: "i-heroicons-exclamation-triangle",
            color: "warning",
        });
    }
    outageNodes.value = newOutageSet;
};

const updateNodeUsages = () => {
    const data = NodesPodsServicesRef.value;
    const nodeUsageMap = new Map<
        string,
        { cpu: number; mem: number; pods: Pod[] }
    >();

    // Initialize node usage map
    data.nodes.forEach((node) => {
        nodeUsageMap.set(node.id, { cpu: 0, mem: 0, pods: [] });
    });

    // 1. Calculate Proposed Usages for Pods
    data.pods.forEach((pod) => {
        let simState = podSimulationStates.get(pod.id);
        if (!simState) {
            simState = {
                trend: 0,
                trendDuration: 0,
                cpuUsageHistory: [pod.cpu_usage],
                memoryToCpuRatio:
                    pod.cpu_usage > 0 ? pod.mem_usage / pod.cpu_usage : 10,
            };
            podSimulationStates.set(pod.id, simState);
        }

        const currentNode = data.nodes.find(
            (node) => node.id === pod.current_node,
        );
        const nodeCapacity = currentNode ? currentNode.cpu_capacity : 100;

        // Update Trend with "Gravity" to prevent sticking to 0 or Max
        if (simState.trendDuration <= 0) {
            const usageRatio = pod.cpu_usage / nodeCapacity;
            const rand = Math.random();

            // Gravity: High usage -> bias down, Low usage -> bias up
            let probDown = 0.33;
            let probUp = 0.33;

            if (usageRatio > 0.6) {
                probDown = 0.7;
                probUp = 0.1;
            } else if (usageRatio < 0.1) {
                probDown = 0.1;
                probUp = 0.7;
            }

            if (rand < probDown) {
                simState.trend = -1;
            } else if (rand < probDown + (1 - probDown - probUp)) {
                simState.trend = 0;
            } else {
                simState.trend = 1;
            }

            simState.trendDuration = Math.floor(Math.random() * 6) + 3;
        }

        simState.trendDuration -= 1;

        // Calculate Proposed CPU
        const cpuBias = simState.trend * (Math.random() * 3);
        const cpuNoise = (Math.random() - 0.5) * 2;
        let newCpuUsage = pod.cpu_usage + cpuBias + cpuNoise;
        newCpuUsage = Math.max(1, Math.min(newCpuUsage, nodeCapacity)); // Soft clamp

        // Calculate Proposed Memory (based on delayed CPU)
        // Note: We don't push newCpuUsage to history yet, we do it after scaling
        const delayedCpu = simState.cpuUsageHistory[0] || newCpuUsage;
        const targetMemoryUsage = delayedCpu * simState.memoryToCpuRatio;
        const memoryNoise = (Math.random() - 0.5) * 20;
        let newMemoryUsage = targetMemoryUsage + memoryNoise;
        const nodeMemCapacity = currentNode ? currentNode.mem_capacity : 2048;
        newMemoryUsage = Math.max(
            10,
            Math.min(newMemoryUsage, nodeMemCapacity),
        );

        // Assign proposed values temporarily
        pod.cpu_usage = Math.round(newCpuUsage);
        pod.mem_usage = Math.round(newMemoryUsage);

        // Add to node map for aggregation
        if (pod.current_node && nodeUsageMap.has(pod.current_node)) {
            const nodeData = nodeUsageMap.get(pod.current_node)!;
            nodeData.cpu += pod.cpu_usage;
            nodeData.mem += pod.mem_usage;
            nodeData.pods.push(pod);
        }
    });

    // 2. Enforce Node Capacity Constraints (Scaling) & Update History
    data.nodes.forEach((node) => {
        const usageData = nodeUsageMap.get(node.id);
        if (!usageData) return;

        // Check and Scale CPU
        if (usageData.cpu > node.cpu_capacity) {
            const scaleFactor = node.cpu_capacity / usageData.cpu;
            usageData.pods.forEach((pod) => {
                pod.cpu_usage = Math.floor(pod.cpu_usage * scaleFactor);
                if (pod.cpu_usage < 1) pod.cpu_usage = 1;
            });
            // Recalculate total
            usageData.cpu = usageData.pods.reduce(
                (sum, p) => sum + p.cpu_usage,
                0,
            );
        }

        // Check and Scale Memory
        if (usageData.mem > node.mem_capacity) {
            const scaleFactor = node.mem_capacity / usageData.mem;
            usageData.pods.forEach((pod) => {
                pod.mem_usage = Math.floor(pod.mem_usage * scaleFactor);
                if (pod.mem_usage < 1) pod.mem_usage = 1;
            });
            usageData.mem = usageData.pods.reduce(
                (sum, p) => sum + p.mem_usage,
                0,
            );
        }

        // Update History for Pods on this node (using the final scaled values)
        usageData.pods.forEach((pod) => {
            const simState = podSimulationStates.get(pod.id);
            if (simState) {
                simState.cpuUsageHistory.push(pod.cpu_usage);
                while (simState.cpuUsageHistory.length > 3) {
                    simState.cpuUsageHistory.shift();
                }
            }
        });

        // 3. Update Node Usage
        node.cpu_usage = usageData.cpu;
        node.mem_usage = usageData.mem;

        const randomAction = Math.random();
        // 0.5% chance to add a pod
        // if (randomAction < 0.005) {
        if (randomAction < 0.01) {
            const newPodId = `pod-new-${Date.now()}`;
            // 66% chance for existing service, 17% for null, 17% for new service
            const randService = Math.random();
            let serviceId: string | null = null;

            if (randService < 0.66 && data.services.length > 0) {
                // Pick a random existing service
                const randomServiceIndex = Math.floor(
                    Math.random() * data.services.length,
                );
                const randomService = data.services[randomServiceIndex];
                if (randomService) serviceId = randomService.id;
                else serviceId = null;
            } else if (randService < 0.83) {
                serviceId = null;
            } else {
                const newServiceId = `service-new-${Math.floor(Math.random() * 100)}`;
                // Check if service exists, if not create it and its LB
                if (!data.services.find((s) => s.id === newServiceId)) {
                    const lbId = `pod-lb-${newServiceId}`;
                    const newService: Service = {
                        id: newServiceId,
                        load_balancer_pod: lbId,
                        auto_scaling_enabled: true,
                        current_request_rate: 50,
                        priority: 5,
                    };
                    data.services.push(newService);

                    const newLbPod: Pod = {
                        id: lbId,
                        cpu_usage: 5,
                        mem_usage: 128,
                        current_node: null, // Queue
                        service: newServiceId,
                        priority: 7,
                    };
                    data.pods.push(newLbPod);
                    podSimulationStates.set(newLbPod.id, {
                        trend: 0,
                        trendDuration: 5,
                        cpuUsageHistory: [5],
                        memoryToCpuRatio: 25.6,
                    });
                }
                serviceId = newServiceId;
            }

            const newPod: Pod = {
                id: newPodId,
                cpu_usage: 10, // Fixed initial value
                mem_usage: 256, // Fixed initial value
                current_node: null, // Queue
                service: serviceId,
                priority: 4,
            };
            data.pods.push(newPod);
            // Initialize simulation state for the new pod
            podSimulationStates.set(newPod.id, {
                trend: 0,
                trendDuration: 5,
                cpuUsageHistory: [10],
                memoryToCpuRatio: 25.6,
            });
        }
        // 0.5% chance to delete a pod (excluding LBs)
        // else if (randomAction > 0.995) {
        else if (randomAction >= 0.995) {
            const deletablePods = data.pods.filter(
                (p) => !p.id.includes("lb") && p.current_node !== null,
            );
            if (deletablePods.length > 0) {
                const podToDelete =
                    deletablePods[
                        Math.floor(Math.random() * deletablePods.length)
                    ];
                if (podToDelete) {
                    data.pods = data.pods.filter(
                        (p) => p.id !== podToDelete.id,
                    );
                    podSimulationStates.delete(podToDelete.id);
                }
            }
        }
    });
};

const toast = useToast();

const recalculateNodeStats = () => {
    const data = NodesPodsServicesRef.value;
    const nodeUsageMap = new Map<string, { cpu: number; mem: number }>();

    data.nodes.forEach((node) => {
        nodeUsageMap.set(node.id, { cpu: 0, mem: 0 });
    });

    data.pods.forEach((pod) => {
        if (pod.current_node && nodeUsageMap.has(pod.current_node)) {
            const usage = nodeUsageMap.get(pod.current_node)!;
            usage.cpu += pod.cpu_usage;
            usage.mem += pod.mem_usage;
        }
    });

    data.nodes.forEach((node) => {
        const usage = nodeUsageMap.get(node.id);
        if (usage) {
            node.cpu_usage = usage.cpu;
            node.mem_usage = usage.mem;
        }
    });
};

const fetchUpdates = async () => {
    const activeNodes = NodesPodsServicesRef.value.nodes.filter(
        (n) => !outageNodes.value.has(n.id),
    );
    const requestData = {
        state: {
            nodes: activeNodes,
            pods: NodesPodsServicesRef.value.pods,
            services: NodesPodsServicesRef.value.services,
        },
    };
    console.log("request data is: ", requestData);
    try {
        const response = await fetch(`api/kytos/optimize`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData),
        });
        if (!response.ok) {
            toast.add({
                title: "リクエストが失敗しました",
                description: "There was a problem with your request.",
                icon: "i-lucide-wifi",
                color: "error",
            });
        }

        const result = (await response.json()) as AnnealingResponse;

        return result;
    } catch (error) {
        console.error(error);
        toast.add({
            title: "ネットワークエラー",
            description: "Could not reach the server.",
            icon: "i-lucide-wifi-off",
            color: "error",
        });
    }
};

const quantumUpdateLines = async () => {
    const annealing_result = await fetchUpdates();
    console.log("fetch results: ", annealing_result);
    if (!annealing_result) return;

    NodesPodsServicesRef.value.pods = annealing_result.pods.map((p) => ({
        id: p.id,
        cpu_usage: p.cpu_usage,
        mem_usage: p.mem_usage,
        current_node: p.current_node,
        service: p.service,
        priority: p.priority,
    }));

    recalculateNodeStats();

    toast.add({
        title: "ノード配置が最適化されました",
        description: "Node and Pod assignments have been updated.",
        icon: "i-lucide-refresh-cw",
        color: "success",
    });
};

onMounted(() => {
    setInterval(() => {
        updateNodeUsages();
        quantumUpdateLines();
    }, 5000);
});
</script>
<template>
    <div class="nodes-container">
        <KytosNode
            :nodes="NodesPodsServicesRef"
            :outage-nodes="outageNodes"
            @toggle-outage="toggleNodeOutage"
        />
    </div>
</template>

<style scoped lang="scss">
.nodes-container {
    min-height: 100vh;
    padding: 0 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
