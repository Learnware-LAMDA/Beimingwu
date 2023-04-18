<script setup>
import { ref, watch } from 'vue'

const emit = defineEmits(['update:files'])

const props = defineProps({
  files: {
    type: Array,
    default: () => []
  },
  errorMessages: {
    type: String,
  }
})

const _files = ref([])
const dragging = ref(false)
const fileInput = ref(null)

const handleDrop = (event) => {
  dragging.value = false
  _files.value = Array.from(event.dataTransfer.files)
  uploadFile()
}

const chooseFile = () => {
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

watch(() => _files.value, (val) => {
  emit('update:files', val)
})
</script>

<template>
  <div>
    <v-card class="bg-transparent" @dragover.prevent @dragenter.prevent="dragging = true"
      @dragleave.prevent="dragging = false" @drop.prevent="handleDrop" @click="chooseFile" flat>
      <v-card-text
        class="h-40 drag rounded-lg border-gray-500 border-2 border-dashed flex flex-column justify-center items-center md:text-xl text-1.1rem"
        :class="{ 'drag-hover': dragging }">
        <div class="flex justify-center items-center max-w-1/1">
          <p v-if="_files.length === 0">
            <v-icon class="mr-1" icon="mdi-paperclip"></v-icon>Drag your file here
          </p>
          <div v-else class="w-1/1 truncate">
            <v-icon class="mr-1" icon="mdi-paperclip"></v-icon>{{ _files[0].name }} <span class="ml-2 text-sm">{{
              computeFileSize(_files[0].size) }}</span>
          </div>
          <v-btn flat v-if="_files.length > 0" icon="mdi-close" @click.stop="() => _files = []"></v-btn>
        </div>
      </v-card-text>
      <v-file-input ref="fileInput" v-show="false" v-model="_files" label="select a file">
      </v-file-input>
    </v-card>
    <v-scroll-y-transition>
      <v-card-text v-if="errorMessages" class="text-error">{{ errorMessages }}</v-card-text>
    </v-scroll-y-transition>
  </div>
</template>