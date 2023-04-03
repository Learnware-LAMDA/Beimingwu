<script setup>
import { ref } from 'vue'
import VStepperTitle from './VStepperTitle.vue'
import FileUpload from './FileUpload.vue'
import SemanticSpec from './SemanticSpec.vue'

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

function nextStep() {
  if (currentStep.value < steps.length - 1) {
    activeStep(currentStep.value + 1)
  }
}

function PrevStep() {
  if (currentStep.value > 0) {
    activeStep(currentStep.value - 1)
  }
}
</script>

<template>
  <v-container class="h-1/1">
    <v-card class="max-w-1000px w-1/1 m-auto">
      <v-stepper-title
        class="mt-2 mb-5 w-1/1"
        :steps="steps"
        :current-step="currentStep"
        @active-step="activeStep"
      />
      
      <v-divider class="border-black"></v-divider>
      
      <div class="w-1/1 mx-auto p-2">
        <v-card-title class="!md:text-2xl text-1rem">
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
            <v-card-text class="pt-0">
              <semantic-spec />
            </v-card-text>
          </v-window-item>
    
          <v-window-item :value="2">
            <div class="pa-4 text-center">
              <v-textarea label="Description" placeholder="This is a description of the learnware"></v-textarea>
            </div>
          </v-window-item>
    
          <v-window-item :value="3">
            <div class="p-4 m-auto">
              <file-upload
                v-model:files="files"
              ></file-upload>
            </div>
          </v-window-item>
        </v-window>
    
        <v-divider></v-divider>
    
        <v-card-actions>
          <v-btn v-if="currentStep > 0" variant="outlined" @click="PrevStep">
            Back
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn v-if="currentStep < steps.length - 1" color="primary" variant="flat" @click="nextStep">
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