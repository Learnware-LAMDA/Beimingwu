<script setup lang="ts">
import { ref, nextTick } from "vue";

const start = ref(false);
const dialog = ref(false);

defineExpose({
  show: () => {
    start.value = false;
    dialog.value = true;
    nextTick(() => (start.value = true));
  },
});
</script>

<template>
  <v-dialog v-model="dialog" class="mx-auto w-full max-w-[600px]">
    <v-card class="mx-2">
      <v-card-title class="flex m-2">
        <v-icon class="mr-2" icon="mdi-check-circle" color="success"></v-icon>
        <slot name="title" />
      </v-card-title>
      <svg class="m-auto w-120px h-120px" viewBox="0 0 200 200">
        <circle style="fill: rgb(var(--v-theme-success))" cx="100" cy="100" r="80" />
        <path
          d="M50 100 L90 134 L152 64"
          stroke="white"
          stroke-width="16"
          fill="none"
          stroke-dasharray="146"
          stroke-dashoffset="146"
          class="transition-all duration-800"
          :class="start ? ['offset-animate'] : null"
        ></path>
      </svg>
      <v-card-text>
        <slot name="text" />
      </v-card-text>
      <v-card-actions>
        <v-spacer class="flex-1"></v-spacer>
        <v-btn class="bg-success" @click="dialog = false"> OK </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
