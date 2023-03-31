<script setup>
import { advancePositionWithClone } from '@vue/compiler-core';
import { ref, watch } from 'vue'

const emit = defineEmits(['update:files'])

const props = defineProps({
  files: {
    type: Array,
    default: () => []
  }
})

const files = ref([])
const dragging = ref(false)
const fileInput = ref(null)

const handleDrop = (event) => {
  dragging.value = false
  files.value = Array.from(event.dataTransfer.files)
  uploadFile()
}

const uploadFile = () => {
  console.log(files.value);
}

const chooseFile = () => {
  console.log(fileInput.value)
  fileInput.value.click()
}

const computeFileSize = (byte) => {
  const unit = ['B', 'KB', 'MB', 'GB']
  let k = 0
  while (k < 4) {
    if (byte / Math.pow(1000, k) < 1000) {
      break
    }
    k++
  }
  return Math.round(byte / Math.pow(1000, k)) + unit[k]
}

watch(() => files.value, (val) => {
  emit('update:files', val)
})
</script>

<template>
  <v-card class="fill-height" @dragover.prevent @dragenter.prevent="dragging = true" @dragleave.prevent="dragging = false"
    @drop.prevent="handleDrop" @click="chooseFile" flat>
    <v-card-text
      class="fill-height drag rounded-lg border-gray-500 border-2 border-dashed flex flex-column justify-center items-center text-xl"
      :class="{ 'drag-hover': dragging }">
      <p v-if="files.length === 0" class="md:text-xl text-sm">
        <v-icon class="mr-1" icon="mdi-paperclip"></v-icon>Drag your file here
      </p>
      <div v-else>
        <div>
          <v-icon class="mr-1" icon="mdi-paperclip"></v-icon>{{ files[0].name }} <span class="ml-2 text-sm">{{
            computeFileSize(files[0].size) }}</span>
        </div>
      </div>
    </v-card-text>
    <v-file-input ref="fileInput" v-show="false" v-model="files" label="select a file">
    </v-file-input>
  </v-card>
</template>