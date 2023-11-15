<script setup lang="ts">
import { ref, computed } from "vue";

const props = defineProps({
  progress: {
    type: Number,
    default: 0,
  },
});

const progress = computed<number>({
  get() {
    return props.progress;
  },
  set() {},
});

const dialog = ref(true);
</script>

<template>
  <v-dialog v-model="dialog" persistent class="dialog">
    <v-card class="p-2">
      <v-card-title class="main">
        <slot name="title" />
      </v-card-title>
      <v-progress-linear
        v-model="progress"
        color="primary"
        rounded
        height="5"
        class="mb-4"
      ></v-progress-linear>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">
.dialog {
  @apply w-full max-w-[600px];
  .main {
    @apply mb-4 text-center;
    .svg {
      @apply m-auto w-1/5;
    }
  }
}
</style>
