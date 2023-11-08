<script lang="ts" setup>
import { ref, computed } from "vue";
import { useElementBounding } from "@vueuse/core";

const anchorElement = ref<HTMLElement>();
const stickyElement = ref<HTMLElement>();
const animateElement = ref<HTMLElement>();

const { y } = useElementBounding(anchorElement);
const { height: stickyHeight } = useElementBounding(stickyElement);
const { height: animateHeight } = useElementBounding(animateElement);

const progress = computed(() => {
  if (stickyHeight.value === animateHeight.value) {
    return 0;
  }
  return Math.max(0, Math.min(1, -y.value / (stickyHeight.value - animateHeight.value)));
});
</script>

<template>
  <div ref="stickyElement">
    <div ref="anchorElement" />
    <div
      class="sticky"
      :style="{
        top: 'var(--v-layout-top)',
      }"
    >
      <div ref="animateElement">
        <slot :progress="progress" />
      </div>
    </div>
  </div>
</template>
