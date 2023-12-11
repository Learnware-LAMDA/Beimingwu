<script setup lang="ts">
import { computed } from "vue";
interface Props {
  fragments: string[];
  progress: number;
}

const props = defineProps<Props>();

const html = computed(() => {
  return props.fragments
    .filter((_, i) => i < Math.floor(props.fragments.length * props.progress))
    .join("");
});
</script>

<template>
  <div
    class="after:bg-gray-200 after:text-gray-200"
    :class="progress < 1 ? `after:content-['|']` : `after:content-['']`"
    v-html="html"
  />
</template>
