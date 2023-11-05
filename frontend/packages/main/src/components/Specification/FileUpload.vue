<script setup lang="ts">
import { ref, computed } from "vue";

export interface Props {
  files: File[];
  tips: string;
  errorMessages?: string;
  height?: number;
}

const emit = defineEmits(["update:files"]);

const props = withDefaults(defineProps<Props>(), {
  files: () => [],
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
  get: () => props.files,
  set: (val) => {
    emit("update:files", val);
  },
});
</script>

<template>
  <div>
    <v-card
      class="bg-transparent"
      flat
      @dragover.prevent
      @dragenter.prevent="dragging = true"
      @dragleave.prevent="dragging = false"
      @drop.prevent="handleDrop"
      @click="chooseFile"
    >
      <v-card-text
        class="drag rounded-lg border-gray-500 border-2 border-dashed flex flex-column justify-center items-center"
        :class="{ 'drag-hover': dragging }"
        :style="{ height: Number(height) / 4 + 'rem' }"
      >
        <div class="flex justify-center items-center max-w-full md:text-xl text-base">
          <p v-if="files.length === 0">
            <v-icon class="mr-1" icon="mdi-paperclip"></v-icon>
            {{ tips }}
          </p>
          <div v-else class="w-full truncate">
            <v-icon class="mr-1" icon="mdi-paperclip"></v-icon>{{ files[0].name }}
            <span class="ml-2 text-sm">{{ computeFileSize(files[0].size) }}</span>
          </div>
          <v-btn
            v-if="files.length > 0"
            variant="flat"
            icon="mdi-close"
            @click.stop="() => (files = [])"
          ></v-btn>
        </div>
      </v-card-text>
      <v-file-input v-show="false" ref="fileInput" v-model="files" label="select a file">
      </v-file-input>
    </v-card>
    <v-scroll-y-transition>
      <v-card-text v-if="errorMessages" class="text-error">{{ errorMessages }}</v-card-text>
    </v-scroll-y-transition>
  </div>
</template>
