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
  <v-dialog
    v-model="dialog"
    persistent
    class="w-full max-w-[600px]"
  >
    <div class="bg-surface-light dark:bg-surface-dark p-2">
      <v-card-title class="mb-4 text-center text-black dark:text-white">
        <slot name="title" />
      </v-card-title>
      <v-progress-linear
        v-model="progress"
        color="primary"
        rounded
        height="5"
        class="mb-4"
      />
    </div>
  </v-dialog>
</template>
