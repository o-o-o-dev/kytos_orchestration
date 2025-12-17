<script setup lang="ts">
import type { default as KatexType } from 'katex';

const props = defineProps<{
  tex: string;
  block?: boolean;
}>();

const rendered = ref('');
const katexModule = ref<typeof KatexType | null>(null);

const renderMath = () => {
  if (!katexModule.value) return;
  try {
    rendered.value = katexModule.value.renderToString(props.tex, {
      displayMode: props.block ?? false,
      throwOnError: false,
      strict: false,
    });
  } catch (e) {
    console.error('KaTeX rendering error:', e);
    rendered.value = props.tex;
  }
};

onMounted(async () => {
  katexModule.value = (await import('katex')).default;
  renderMath();
});

watch(() => props.tex, renderMath);
watch(() => props.block, renderMath);
</script>

<template>
  <span v-if="!block" v-html="rendered" class="katex-inline"></span>
  <div v-else v-html="rendered" class="katex-block"></div>
</template>

<style scoped>
.katex-block {
  text-align: center;
  margin: 0.5rem 0;
}
</style>
