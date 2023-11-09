<script lang="ts" setup>
import { ref, computed, watch } from "vue";
import { useElementBounding } from "@vueuse/core";

const emit = defineEmits(["progress"]);

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

watch(
  () => progress.value,
  (newProgress) => {
    emit("progress", newProgress);
  },
  { immediate: true },
);
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
