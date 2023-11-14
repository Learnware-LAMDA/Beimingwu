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
    <v-sheet elevation="12" max-width="600" rounded="lg" width="100%" class="p-4 mx-auto">
      <slot name="title">
        <svg class="m-auto w-[120px] h-[120px]" viewBox="0 0 200 200">
          <circle style="fill: rgb(var(--v-theme-success))" cx="100" cy="100" r="80" />
          <path
            d="M50 100 L90 134 L152 64"
            stroke="white"
            stroke-width="16"
            fill="none"
            stroke-dasharray="146"
            :class="{ 'path-offset': dialog }"
          ></path>
        </svg>
      </slot>

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
    stroke-dashoffset: 146;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

.path-offset {
  animation: pathOffset 600ms ease-in-out forwards;
}
</style>
