<script setup lang="ts">
defineProps<{
    label: string;
    progress: number;
}>();

type ProgressColor =
    | "primary"
    | "secondary"
    | "success"
    | "info"
    | "warning"
    | "error"
    | "neutral"
    | undefined;

const getColor = (progress: number): ProgressColor => {
    if (progress < 50) {
        return "primary";
    } else if (progress < 80) {
        return "warning";
    } else {
        return "error";
    }
};
</script>

<template>
    <div class="node-pressure-wrapper">
        <div class="node-pressure-label">
            <div class="node-pressure-label-text">{{ label }}</div>
            <div class="node-pressure-value">{{ progress }}%</div>
        </div>
        <div class="node-pressure-bar">
            <UProgress :model-value="progress" :color="getColor(progress)" />
        </div>
    </div>
</template>

<style scoped lang="scss">
.node-pressure-wrapper {
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
</style>
