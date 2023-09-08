<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import VStepperTitle from '@main/components/Public/VStepperTitle.vue'
import FileUpload from '@main/components/Specification/FileUpload.vue'
import SpecTag from '@main/components/Specification/SpecTag.vue'

const route = useRoute()
const router = useRouter()

const currentStep = ref(0)
const files = ref([])
const name = ref('')
const dataType = ref('')
const taskType = ref('')
const libraryType = ref('')
const tagList = ref([])
const description = ref('')

const steps = [
  { 
    title: 'Type the name of your learnware',
    subtitle: 'Name',
    icon: 'mdi-rename'
  },
  {
    title: 'Choose the tags',
    subtitle: 'Tag',
    icon: 'mdi-label-multiple'
  },
  {
    title: 'Type the description',
    subtitle: 'Description',
    icon: 'mdi-image-text'
  },
  {
    title: 'Upload your model & statistical specification',
    subtitle: 'File',
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

onMounted(() => {
  if(route.query.name) {
    name.value = route.query.name
  }
  if(route.query.dataType) {
    dataType.value = route.query.dataType
  }
  if(route.query.taskType) {
    taskType.value = route.query.taskType
  }
  if(route.query.libraryType) {
    libraryType.value = route.query.libraryType
  }
  if(route.query.tagList) {
    tagList.value = JSON.parse(route.query.tagList)
  }
  if(route.query.description) {
    description.value = route.query.description
  }
})
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
              <v-text-field v-model="name" label="Name" placeholder="Awesome learnware" append-inner-icon="mdi-close" @click:append-inner="name = ''"></v-text-field>
              <span class="text-caption text-grey-darken-1">
                This is the name of the learnware you contribute.
              </span>
            </v-card-text>
          </v-window-item>
    
          <v-window-item :value="1">
            <v-card-text class="pt-0">
              <spec-tag v-model:data-type="dataType" v-model:task-type="taskType" v-model:library-type="libraryType" v-model:tag-list="tagList" />
            </v-card-text>
          </v-window-item>
    
          <v-window-item :value="2">
            <div class="pa-4 text-center">
              <v-textarea v-model="description" label="Description" placeholder="This is a description of the learnware"></v-textarea>
            </div>
          </v-window-item>
    
          <v-window-item :value="3">
            <div class="p-4 m-auto">
              <file-upload
                v-model:files="files"
              ></file-upload>
            </div>
            <v-card-text class="text-lg">
              <span class="cursor-pointer" @click="router.push('/instruction')"><u>Click here</u></span> for instructions on how to create the required zip file.
            </v-card-text>
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