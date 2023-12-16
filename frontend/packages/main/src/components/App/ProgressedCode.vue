<script setup lang="ts">
import { computed } from "vue";
import { CODE_COLOR } from "@main/constants";
interface Props {
  fragments: string[];
  progress: number;
}

const props = defineProps<Props>();

const html = computed(() => {
  let html = props.fragments
    .filter((_, i) => i < Math.floor(props.fragments.length * props.progress))
    .join("");
  html = Object.values(CODE_COLOR).reduce((acc, color) => {
    const regex = new RegExp(`(?<=${color}">.)</span><span style="color: ${color}">`, "g");
    return acc.replace(regex, "");
  }, html);
  return html;
});
</script>

<template>
  <div
    class="after:bg-gray-200 after:text-gray-200"
    :class="progress < 1 ? `after:content-['|']` : `after:content-['']`"
    v-html="html"
  />
</template>
