<script setup>
import { ref, computed } from 'vue'

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

const step = ref(1)

const currentTitle = computed(() => {
  switch (step.value) {
    case 1: return 'Type the name of your learnware'
    case 2: return 'Choose the semantic specification'
    case 3: return 'Type the description'
    case 4: return 'Upload your statistical specification'
  }
})
</script>

<template>
  <v-container class="fill-height flex justify-center items-center">

    <v-card class="w-1/1 mx-auto p-2 elevation-10" max-width="600">
      <v-card-title class="text-h6 font-weight-regular flex justify-space-between">
        <span>{{ currentTitle }}</span>
      </v-card-title>

      <v-window v-model="step">
        <v-window-item :value="1">
          <v-card-text>
            <v-text-field label="Name" placeholder="Awesome learnware"></v-text-field>
            <span class="text-caption text-grey-darken-1">
              This is the name of the learnware you contribute.
            </span>
          </v-card-text>
        </v-window-item>

        <v-window-item :value="2">
          <v-card-text>

          </v-card-text>
        </v-window-item>

        <v-window-item :value="3">
          <div class="pa-4 text-center">
            <v-textarea label="Description" placeholder="This is a description of the learnware"></v-textarea>
          </div>
        </v-window-item>

        <v-window-item :value="4">
          <v-responsive class="p-4 m-auto" :aspect-ratio="4/1">
            <v-card class="fill-height" @dragover.prevent @dragenter.prevent="dragging = true"
              @dragleave.prevent="dragging = false" @drop.prevent="handleDrop" @click="chooseFile" flat>
              <v-card-text class="fill-height drag rounded-lg border-gray-500 border-2 border-dashed flex flex-column justify-center items-center text-xl" :class="{ 'drag-hover': dragging }">
                <p v-if="files.length === 0">
                  <v-icon class="mr-1" icon="mdi-paperclip"></v-icon>Drag your file here
                </p>
                <div v-else>
                  <div>
                    <v-icon class="mr-1" icon="mdi-paperclip"></v-icon>{{ files[0].name }} <span class="ml-2 text-sm">{{ computeFileSize(files[0].size) }}</span>
                  </div>
                </div>
              </v-card-text>
              <v-file-input ref="fileInput" v-show="false" v-model="files" label="select a file">
              </v-file-input>
            </v-card>
          </v-responsive>
        </v-window-item>
      </v-window>

      <v-divider></v-divider>

      <v-card-actions>
        <v-btn v-if="step > 1" variant="text" @click="step--">
          Back
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn v-if="step < 4" color="primary" variant="flat" @click="step++">
          Next
        </v-btn>
        <v-btn v-else color="primary" variant="flat" @click="submit">
          Finish
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<style scoped>
.drag-hover {
  border: 2px dashed blue;
}
</style>