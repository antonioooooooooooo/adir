<script setup>
import { onMounted, watch } from 'vue';
import katex from 'katex';
import 'katex/dist/katex.min.css';

const props = defineProps({
  content: {
    type: String,
    required: true
  }
});

const renderLatex = () => {
  try {
    const element = document.getElementById('latex-content');
    if (element) {
      element.innerHTML = katex.renderToString(props.content, {
        throwOnError: false,
        displayMode: true
      });
    }
  } catch (error) {
    console.error('LaTeX rendering error:', error);
  }
};

onMounted(() => {
  renderLatex();
});

watch(() => props.content, () => {
  renderLatex();
});
</script>

<template>
  <div id="latex-content" class="latex-renderer"></div>
</template>

<style scoped>
.latex-renderer {
  overflow-x: auto;
  padding: 1rem;
  margin: 0.5rem 0;
}
</style> 