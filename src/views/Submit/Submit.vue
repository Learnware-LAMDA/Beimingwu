<script setup>
import VStepperTitle from './VStepperTitle.vue';
import FileUpload from './FileUpload.vue';
import { ref } from 'vue'

const currentStep = ref(0)

const files = ref([])

const steps = [
  { 
    title: 'Type the name of your learnware',
    subtitle: 'Name',
    icon: 'mdi-rename'
  },
  {
    title: 'Choose the semantic specification',
    subtitle: 'Semantic',
    icon: 'mdi-label-multiple'
  },
  {
    title: 'Type the description',
    subtitle: 'Description',
    icon: 'mdi-image-text'
  },
  {
    title: 'Upload your statistical specification',
    subtitle: 'Upload',
    icon: 'mdi-paperclip-plus'
  },
]

function activeStep(index) {
  currentStep.value = index
}
</script>

<template>
  <v-container class="fill-height flex flex-col justify-center items-center">
    <v-card class="max-w-800px w-1/1 elevation-10">
      <v-stepper-title
        class="mt-5 w-1/1"
        :steps="steps"
        :current-step="currentStep"
        @active-step="activeStep"
      />
      
      <div class="w-1/1 mx-auto p-2">
        <v-card-title class="text-h6 font-weight-regular flex justify-space-between !md:text-lg !text-sm">
          <span>{{ steps[currentStep].title }}</span>
        </v-card-title>
    
        <v-window v-model="currentStep">
          <v-window-item :value="0">
            <v-card-text>
              <v-text-field label="Name" placeholder="Awesome learnware"></v-text-field>
              <span class="text-caption text-grey-darken-1">
                This is the name of the learnware you contribute.
              </span>
            </v-card-text>
          </v-window-item>
    
          <v-window-item :value="1">
            <v-card-text>
    
            </v-card-text>
          </v-window-item>
    
          <v-window-item :value="2">
            <div class="pa-4 text-center">
              <v-textarea label="Description" placeholder="This is a description of the learnware"></v-textarea>
            </div>
          </v-window-item>
    
          <v-window-item :value="3">
            <v-responsive class="p-4 m-auto" :aspect-ratio="4 / 1">
              <file-upload
                v-model:files="files"
              ></file-upload>
            </v-responsive>
          </v-window-item>
        </v-window>
    
        <v-divider></v-divider>
    
        <v-card-actions>
          <v-btn v-if="currentStep > 0" variant="outlined" @click="currentStep > 0 ? currentStep-- : null">
            Back
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn v-if="currentStep < steps.length - 1" color="primary" variant="flat" @click="currentStep < steps.length - 1 ? currentStep++ : null">
            Next
          </v-btn>
          <v-btn v-else color="primary" variant="flat" @click="submit">
            Finish
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
  </v-container>
</template>

<style scoped>
.drag-hover {
  border: 2px dashed blue;
}
</style>