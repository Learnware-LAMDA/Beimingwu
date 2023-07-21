<script setup>
import { ref, computed } from "vue";

const emit = defineEmits(["update:files"]);

const props = defineProps({
  files: {
    type: Array,
    default: () => [],
  },
  errorMessages: {
    type: String,
    default: "",
  },
  height: {
    type: Number,
    default: 40,
  },
});

const dragging = ref(false);
const fileInput = ref(null);

const handleDrop = (event) => {
  dragging.value = false;
  files.value = Array.from(event.dataTransfer.files);
};

const chooseFile = () => {
  fileInput.value.click();
};

const computeFileSize = (byte) => {
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
        class="drag rounded-lg border-gray-500 border-2 border-dashed flex flex-column justify-center items-center md:text-xl text-1.1rem"
        :class="{ 'drag-hover': dragging }"
        :style="{ height: Number(height) / 4 + 'rem' }"
      >
        <div class="flex justify-center items-center max-w-1/1">
          <p v-if="files.length === 0">
            <v-icon class="mr-1" icon="mdi-paperclip"></v-icon>Drag your file here
          </p>
          <div v-else class="w-1/1 truncate">
            <v-icon class="mr-1" icon="mdi-paperclip"></v-icon>{{ files[0].name }}
            <span v-if="files[0]?.name !== 'Your old learnware'" class="ml-2 text-sm">{{
              computeFileSize(files[0].size)
            }}</span>
          </div>
          <v-btn
            v-if="files.length > 0"
            flat
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
