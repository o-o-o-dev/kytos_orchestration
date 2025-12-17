<script setup lang="ts">
const props = defineProps<{
    id?: string;
    title: string;
    lead?: string;
}>();
</script>

<template>
    <section :id="props.id" class="section">
        <header class="section-header">
            <h2 class="section-title">{{ props.title }}</h2>
            <p v-if="props.lead" class="section-lead">{{ props.lead }}</p>
        </header>
        <div class="section-body">
            <slot />
        </div>
    </section>
</template>

<style scoped lang="scss">
.section {
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    padding: 3.5rem 1.25rem;
}

.section-header {
    margin-bottom: 1.25rem;
}

.section-title {
    font-size: clamp(1.5rem, 1.1rem + 1vw, 2rem);
    font-weight: 700;
    color: $on-surface-variant;
    letter-spacing: 0.01em;
}

.section-lead {
    margin-top: 0.5rem;
    color: $on-surface;
    font-size: 1rem;
    line-height: 1.75;
    max-width: 70ch;
}

.section-body {
    width: 100%;
}
</style>
