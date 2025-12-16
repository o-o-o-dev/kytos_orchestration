<script setup lang="ts">
const props = defineProps<{
    nodes: NodesPodsServices;
    outageNodes?: Set<string>;
}>();

const emit = defineEmits<{
    (e: "toggle-outage", nodeId: string): void;
}>();

const { isLoadBalancer, getNodeStats, getPodCpuPercentage, getPodsForNode } =
    useNodeStats(props.nodes);

const containerRef = ref<HTMLElement | null>(null);
const podRefs = ref<Map<string, HTMLElement>>(new Map());

interface Line {
    id: string;
    d: string;
    color: string;
}

const lines = ref<Line[]>([]);

const setPodRef = (el, podId: string) => {
    if (el) {
        podRefs.value.set(podId, el);
    } else {
        podRefs.value.delete(podId);
    }
};

const updateLines = () => {
    if (!containerRef.value) return;

    const containerRect = containerRef.value.getBoundingClientRect();
    const newLines: Line[] = [];

    const serviceColors = [
        "#FF6B6B",
        "#4ECDC4",
        "#45B7D1",
        "#96CEB4",
        "#FFEEAD",
        "#D4A5A5",
    ];

    props.nodes.services.forEach((service, index) => {
        const lbId = service.load_balancer_pod;
        const lbEl = podRefs.value.get(lbId);

        if (!lbEl) return;

        const lbRect = lbEl.getBoundingClientRect();
        // Calculate center relative to container
        const startX = lbRect.left + lbRect.width / 2 - containerRect.left;
        const startY = lbRect.top + lbRect.height / 2 - containerRect.top;

        const color = serviceColors[index % serviceColors.length];

        const servicePods = props.nodes.pods.filter(
            (p) => p.service === service.id && p.id !== lbId,
        );

        const curvatureDirection = index % 2 === 0 ? 1 : -1;
        const curvatureIntensity = 0.3; // 20% of the distance

        servicePods.forEach((pod) => {
            const podEl = podRefs.value.get(pod.id);
            if (podEl) {
                const podRect = podEl.getBoundingClientRect();
                const endX =
                    podRect.left + podRect.width / 2 - containerRect.left;
                const endY =
                    podRect.top + podRect.height / 2 - containerRect.top;

                // Calculate Quadratic Bezier Control Point
                const dx = endX - startX;
                const dy = endY - startY;

                // Calculate perpendicular offset
                // The control point is the midpoint + a perpendicular vector scaled by curvature
                const midX = (startX + endX) / 2;
                const midY = (startY + endY) / 2;

                const cx = midX - dy * curvatureIntensity * curvatureDirection;
                const cy = midY + dx * curvatureIntensity * curvatureDirection;

                newLines.push({
                    id: `${lbId}-${pod.id}`,
                    d: `M ${startX} ${startY} Q ${cx} ${cy} ${endX} ${endY}`,
                    color: color!,
                });
            }
        });
    });

    lines.value = newLines;
};

watch(
    () => props.nodes,
    () => {
        nextTick(updateLines);
    },
    { deep: true },
);

onMounted(() => {
    window.addEventListener("resize", updateLines);
    setTimeout(updateLines, 200);
});

onUnmounted(() => {
    window.removeEventListener("resize", updateLines);
});
</script>

<template>
    <div class="nodes-layout">
        <div ref="containerRef" class="node-grid">
            <svg class="connections-overlay">
                <path
                    v-for="line in lines"
                    :key="line.id"
                    :d="line.d"
                    :stroke="line.color"
                    stroke-width="2"
                    stroke-opacity="1"
                    stroke-dasharray="4 4"
                    fill="none"
                />
            </svg>
            <div
                v-for="node in props.nodes.nodes"
                :key="node.id"
                class="node-container"
            >
                <div class="node-header">
                    <h2 class="node-title">Node {{ node.id }}</h2>
                    <UButton
                        size="xs"
                        :color="
                            props.outageNodes?.has(node.id)
                                ? 'success'
                                : 'error'
                        "
                        variant="soft"
                        :icon="
                            props.outageNodes?.has(node.id)
                                ? 'i-heroicons-play'
                                : 'i-heroicons-stop'
                        "
                        @click="emit('toggle-outage', node.id)"
                    >
                        {{
                            props.outageNodes?.has(node.id) ? "Restore" : "Kill"
                        }}
                    </UButton>
                </div>
                <div class="node-body">
                    <div class="node-pressure-container">
                        <KytosProgress
                            :label="`CPU: ${getNodeStats(node).cpu_capacity}コア`"
                            :progress="getNodeStats(node).cpu"
                        />
                        <KytosProgress
                            :label="`メモリ: ${getNodeStats(node).mem_capacity}MB`"
                            :progress="getNodeStats(node).memory"
                        />
                    </div>
                    <div class="node-services-container">
                        <div class="node-services-list">
                            <div
                                v-for="pod in getPodsForNode(node.id)"
                                :key="pod.id"
                                :ref="(el) => setPodRef(el, pod.id)"
                                class="node-service-item"
                                :class="{ 'is-lb': isLoadBalancer(pod) }"
                            >
                                <UIcon
                                    v-if="isLoadBalancer(pod)"
                                    name="i-heroicons-globe-alt"
                                    class="node-service-icon"
                                />
                                <UIcon
                                    v-else
                                    name="i-heroicons-server"
                                    class="node-service-icon"
                                />
                                <div class="node-service-name">
                                    {{ pod.id }}
                                </div>
                                <div class="node-service-cpu">
                                    CPU: {{ getPodCpuPercentage(pod) }}%
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="getPodsForNode(null).length > 0" class="queue-container">
            <div class="queue-header">
                <h2 class="queue-title">Pending Pods Queue</h2>
            </div>
            <div class="queue-list">
                <div
                    v-for="pod in getPodsForNode(null)"
                    :key="pod.id"
                    class="queue-item"
                >
                    <UIcon name="i-heroicons-clock" class="queue-icon" />
                    <div class="queue-name">{{ pod.id }}</div>
                    <div class="queue-service">{{ pod.service }}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.nodes-layout {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}
.node-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 4rem;
    justify-content: center;
    width: 100%;
    max-width: 1200px;
    padding: 1rem;
    position: relative;
}
.connections-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 10;
}
.node-container {
    width: 100%;
    max-width: 400px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: $surface;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-color: $primary;
    border-width: 1px;
    transition: all 0.3s ease;

    &.is-outage {
        opacity: 0.7;
        border-color: #ef4444;
        background-color: rgba(#ef4444, 0.05);
        filter: grayscale(0.8);
    }
}
.node-header {
    width: 100%;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    .node-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: $on-surface-variant;
    }
}
.node-body {
    width: 100%;
    .node-pressure-container {
        width: 100%;
        .node-pressure-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
            .node-pressure-label-text {
                font-size: 1rem;
                color: $on-surface;
            }
            .node-pressure-value {
                font-size: 1rem;
                font-weight: 600;
                color: $on-surface-variant;
            }
        }
        .node-pressure-bar {
            width: 100%;
        }
    }
    .node-pressure-container {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .node-services-container {
        width: 100%;
        margin-top: 1rem;

        .node-services-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
            gap: 0.5rem;
        }

        .node-service-item {
            aspect-ratio: 1;
            border: 1px solid $on-surface-variant;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 4px;
            background-color: $surface;

            .node-service-icon {
                font-size: 1.5rem;
                margin-bottom: 4px;
                color: $on-surface;
            }

            .node-service-name {
                font-size: 0.75rem;
                color: $on-surface-variant;
                text-align: center;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                width: 100%;
            }
            .node-service-cpu {
                font-size: 0.7rem;
                color: $on-surface-variant;
                margin-top: 2px;
            }
        }
    }
}
.queue-container {
    margin-top: 2rem;
    width: 100%;
    max-width: 800px;
    background-color: $surface;
    border: 1px dashed $on-surface-variant;
    border-radius: 12px;
    padding: 1rem;

    .queue-header {
        margin-bottom: 1rem;
        .queue-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: $on-surface-variant;
            text-align: center;
        }
    }

    .queue-list {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;

        .queue-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 0.5rem;
            background-color: rgba($on-surface, 0.05);
            border-radius: 8px;
            min-width: 80px;

            .queue-icon {
                font-size: 1.5rem;
                color: $caution;
                margin-bottom: 4px;
            }

            .queue-name {
                font-size: 0.8rem;
                font-weight: 500;
                color: $on-surface;
            }

            .queue-service {
                font-size: 0.7rem;
                color: $on-surface-variant;
            }
        }
    }
}
</style>
