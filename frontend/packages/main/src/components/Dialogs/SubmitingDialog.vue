<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  progress: {
    type: Number,
    default: 0,
  },
});

const progress = computed({
  get() {
    return props.progress;
  },
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
  @apply max-w-600px w-1/1;
  .main {
    @apply mb-4 text-center;
    .svg {
      @apply m-auto w-1/5;
    }
  }
}
</style>
