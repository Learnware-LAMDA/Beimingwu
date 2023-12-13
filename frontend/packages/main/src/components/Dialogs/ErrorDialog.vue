<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ modelValue: boolean }>();
const emit = defineEmits(["update:modelValue"]);

const dialog = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});
</script>

<template>
  <v-dialog v-model="dialog">
    <v-sheet class="mx-auto w-full max-w-[600px] rounded-lg p-4">
      <div class="text-center">
        <slot name="title">
          <svg
            class="mx-auto h-[120px] w-[120px]"
            viewBox="0 0 200 200"
          >
            <circle
              style="fill: rgb(var(--v-theme-error))"
              cx="100"
              cy="100"
              r="80"
            />
            <path
              d="M60 60 L140 140"
              stroke="white"
              stroke-width="16"
              stroke-dasharray="113"
              fill="none"
              :class="{ 'path-offset': dialog }"
            />
            <path
              d="M140 60 L60 140"
              stroke="white"
              stroke-width="16"
              fill="none"
              stroke-dasharray="113"
              stroke-dashoffset="113"
              :style="{ animationDelay: '200ms' }"
              :class="{ 'path-offset': dialog }"
            />
          </svg>
        </slot>
      </div>

      <slot name="msg" />

      <div class="text-end">
        <slot name="buttons" />
      </div>
    </v-sheet>
  </v-dialog>
</template>

<style scoped lang="scss">
@keyframes pathOffset {
  0% {
    stroke-dashoffset: 113;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

.path-offset {
  animation: pathOffset 200ms ease-in-out forwards;
}
</style>
