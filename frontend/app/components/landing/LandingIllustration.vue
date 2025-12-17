<script setup lang="ts">
const props = defineProps<{
    kind: "datacenter" | "tradeoff" | "qubo";
}>();
</script>

<template>
    <div class="illus" aria-hidden="true">
        <svg v-if="props.kind === 'datacenter'" viewBox="0 0 420 240">
            <defs>
                <linearGradient id="dc-bg" x1="0" x2="1" y1="0" y2="1">
                    <stop offset="0" stop-color="currentColor" stop-opacity="0.08" />
                    <stop offset="1" stop-color="currentColor" stop-opacity="0.02" />
                </linearGradient>
            </defs>
            <rect x="10" y="14" width="400" height="212" rx="18" fill="url(#dc-bg)" />
            <g fill="none" stroke="currentColor" stroke-opacity="0.35" stroke-width="2">
                <rect x="40" y="44" width="120" height="150" rx="12" />
                <rect x="180" y="44" width="120" height="150" rx="12" />
                <rect x="320" y="44" width="60" height="150" rx="12" />
            </g>
            <g fill="currentColor" fill-opacity="0.35">
                <circle cx="70" cy="78" r="6" />
                <circle cx="70" cy="108" r="6" />
                <circle cx="70" cy="138" r="6" />
                <circle cx="70" cy="168" r="6" />
                <circle cx="210" cy="78" r="6" />
                <circle cx="210" cy="108" r="6" />
                <circle cx="210" cy="138" r="6" />
                <circle cx="210" cy="168" r="6" />
                <circle cx="350" cy="78" r="6" />
                <circle cx="350" cy="108" r="6" />
                <circle cx="350" cy="138" r="6" />
                <circle cx="350" cy="168" r="6" />
            </g>
            <g stroke="currentColor" stroke-opacity="0.25" stroke-width="3" fill="none">
                <path d="M70 205 C120 188, 160 188, 210 205" />
                <path d="M210 205 C260 188, 300 188, 350 205" />
            </g>
        </svg>

        <svg v-else-if="props.kind === 'tradeoff'" viewBox="0 0 420 240">
            <defs>
                <linearGradient id="tr-bg" x1="0" x2="1" y1="0" y2="0">
                    <stop offset="0" stop-color="currentColor" stop-opacity="0.08" />
                    <stop offset="1" stop-color="currentColor" stop-opacity="0.02" />
                </linearGradient>
            </defs>
            <rect x="10" y="14" width="400" height="212" rx="18" fill="url(#tr-bg)" />
            <g fill="none" stroke="currentColor" stroke-opacity="0.35" stroke-width="2">
                <path d="M60 170 L210 70 L360 170" />
                <circle cx="210" cy="70" r="14" />
            </g>
            <g fill="currentColor" fill-opacity="0.35">
                <rect x="52" y="170" width="16" height="16" rx="4" />
                <rect x="202" y="170" width="16" height="16" rx="4" />
                <rect x="352" y="170" width="16" height="16" rx="4" />
            </g>
            <g stroke="currentColor" stroke-opacity="0.25" stroke-width="2" fill="none">
                <path d="M60 170 C110 130, 160 120, 210 110" />
                <path d="M360 170 C310 130, 260 120, 210 110" />
            </g>
        </svg>

        <svg v-else viewBox="0 0 420 240">
            <defs>
                <linearGradient id="q-bg" x1="0" x2="1" y1="0" y2="1">
                    <stop offset="0" stop-color="currentColor" stop-opacity="0.08" />
                    <stop offset="1" stop-color="currentColor" stop-opacity="0.02" />
                </linearGradient>
            </defs>
            <rect x="10" y="14" width="400" height="212" rx="18" fill="url(#q-bg)" />
            <g stroke="currentColor" stroke-opacity="0.35" stroke-width="2" fill="none">
                <circle cx="110" cy="85" r="18" />
                <circle cx="210" cy="60" r="18" />
                <circle cx="300" cy="95" r="18" />
                <circle cx="150" cy="160" r="18" />
                <circle cx="260" cy="165" r="18" />
                <path d="M128 78 L192 67" />
                <path d="M226 72 L284 88" />
                <path d="M120 100 L144 145" />
                <path d="M292 110 L270 148" />
                <path d="M168 162 L242 164" />
                <path d="M210 78 L160 145" />
                <path d="M210 78 L252 148" />
            </g>
            <g fill="currentColor" fill-opacity="0.35">
                <circle cx="110" cy="85" r="6" />
                <circle cx="210" cy="60" r="6" />
                <circle cx="300" cy="95" r="6" />
                <circle cx="150" cy="160" r="6" />
                <circle cx="260" cy="165" r="6" />
            </g>
        </svg>
    </div>
</template>

<style scoped lang="scss">
.illus {
    width: 100%;
    height: auto;
    color: $secondary;
}

svg {
    width: 100%;
    height: auto;
    display: block;
}
</style>
