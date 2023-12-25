<script setup lang="ts">
import { ref, computed } from "vue";

export interface Props {
  modelValue: File[];
  tips: string;
  errorMessages?: string;
  height?: number;
}

const emit = defineEmits(["update:modelValue"]);

const props = withDefaults(defineProps<Props>(), {
  errorMessages: "",
  height: 40,
});

const dragging = ref(false);
const fileInput = ref<HTMLInputElement>();

const handleDrop = (event: DragEvent): void => {
  dragging.value = false;
  if (event.dataTransfer?.files) {
    files.value = Array.from(event.dataTransfer.files);
  }
};

const chooseFile = (): void => {
  fileInput.value && fileInput.value.click();
};

const computeFileSize = (byte: number): string => {
  const unit = ["B", "KB", "MB", "GB"];
  let k = 0;
  while (k < 4) {
    if (byte / 1000 ** k < 1000) {
      break;
    }
    k++;
  }
  return Math.round(byte / 1000 ** k) + unit[k];
};

const files = computed({
  get: () => props.modelValue,
  set: (val) => {
    emit("update:modelValue", val);
  },
});
</script>

<template>
  <div
    v-ripple
    class="flex-column hover:bg-active-light dark:hover:bg-active-dark relative flex cursor-pointer items-center justify-center rounded-lg border-2 border-dashed border-gray-500 transition"
    :class="{ 'border-dashed': dragging }"
    :style="{ height: Number(height) / 4 + 'rem' }"
    @dragover.prevent
    @dragenter.prevent="dragging = true"
    @dragleave.prevent="dragging = false"
    @drop.prevent="handleDrop"
    @click="chooseFile"
  >
    <div
      v-if="dragging"
      class="pointer-events-none absolute inset-0 rounded-lg bg-gray-500 opacity-25"
    />

    <div class="pointer-events-none flex max-w-full items-center justify-center">
      <p v-if="files.length === 0">
        <v-icon
          class="mr-1"
          icon="mdi-paperclip"
        />
        {{ tips }}
      </p>
      <div
        v-else
        class="w-full truncate"
      >
        <v-icon
          class="mr-1"
          icon="mdi-paperclip"
        />{{ files[0].name }}
        <span
          v-if="files[0].size > 0"
          class="ml-2 text-sm"
          >{{ computeFileSize(files[0].size) }}</span
        >
      </div>
      <v-btn
        v-if="files.length > 0"
        class="pointer-events-auto"
        variant="flat"
        icon="mdi-close"
        color="transparent"
        @click.stop="() => (files = [])"
      />
    </div>

    <v-file-input
      v-show="false"
      ref="fileInput"
      v-model="files"
      label="select a file"
    />
  </div>
  <v-scroll-y-transition>
    <v-card-text
      v-if="errorMessages"
      class="text-error"
    >
      {{ errorMessages }}
    </v-card-text>
  </v-scroll-y-transition>
</template>
