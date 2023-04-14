<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useField, useForm } from 'vee-validate'
import VStepperTitle from '@/components/Public/VStepperTitle.vue'
import FileUpload from '@/components/Specification/FileUpload.vue'
import SpecTag from '@/components/Specification/SpecTag.vue'

const route = useRoute()
const router = useRouter()

const store = useStore()

const { handleSubmit, meta } = useForm({
  initialValues: {
    name: '',
    dataType: '',
    taskType: '',
    deviceType: [],
    tagList: [],
    description: '',
    files: []
  },
  validationSchema: {
    name(value) {
      if (value?.length >= 5) {
        return true
      }
      return 'Learnware name needs to be at least 5 characters.'
    },
    dataType(value) {
      if (value?.length > 0) {
        return true
      }
      return 'Data type must not be empty.'
    },
    taskType(value) {
      if (value?.length > 0) {
        return true
      }
      return 'Task type must not be empty.'
    },
    deviceType(value) {
      if (value?.length > 0) {
        return true
      }
      return 'Device type must not be empty.'
    },
    tagList() {
      return true
    },
    description(value) {
      if (value?.length >= 10) {
        return true
      }
      return 'Description needs to be at least 10 characters.'
    },
    files(value) {
      if (value?.length > 0) {
        return true
      }
      return 'Please upload your model & statistical specification.'
    }
  }
})

const name = useField('name')
const dataType = useField('dataType')
const taskType = useField('taskType')
const deviceType = useField('deviceType')
const tagList = useField('tagList')
const description = useField('description')
const files = useField('files')

const currentStep = ref(0)
const submiting = ref(false)
const success = ref(false)
const showError = ref(false)
const errorMsg = ref('')
const errorTimer = ref(null)

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

const valid = computed(() => {
  return meta.value.valid
})
const allowChangePage = computed(() => {
  switch (currentStep.value) {
    case 0: {
      return name.meta.valid
    }
    case 1: {
      return dataType.meta.valid && taskType.meta.valid && deviceType.meta.valid && tagList.meta.valid
    }
    case 2: {
      return description.meta.valid
    }
    case 3: {
      return files.meta.valid
    }
  }
})

function activeStep(index) {
  console.log(valid.value)
  if (valid.value || index < currentStep.value || allowChangePage.value && index <= currentStep.value + 1) {
    currentStep.value = index
  }
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

const submit = handleSubmit((values) => {
  submiting.value = true
  success.value = false
  showError.value = false

  const semanticSpec = {
    "Data": {
      "Values": dataType.value.value,
      "Type": "Class"
    },
    "Task": {
      "Values": taskType.value.value,
      "Type": "Class"
    },
    "Device": {
      "Values": deviceType.value.value,
      "Type": "Tag"
    },
    "Scenario": {
      "Values": tagList.value.value,
      "Type": "Tag"
    },
    "Description": {
      "Values": description.value.value,
      "Type": "Description"
    },
    "Name": {
      "Values": name.value.value,
      "Type": "Name"
    }
  }
  const fd = new FormData()
  fd.append('learnware_file', files.value.value[0])
  fd.append('semantic_specification', JSON.stringify(semanticSpec))

  fetch('/api/user/add_learnware', {
    method: 'POST',
    body: fd,
  })
    .then((res) => {
      if (res.status === 200) {
        return res
      }
      throw new Error('Network error')
    })
    .then((res) => res.json())
    .then((res) => {
      switch (res.code) {
        case 0: {
          submiting.value = false
          success.value = true

          setTimeout(() => {
            success.value = false
            router.go()
          }, 1000)
          return
        }
        case 11: {
          submiting.value = false
          store.commit('setLoggedIn', false)
          store.commit('setShowGlobalError', true)
          store.commit('setGlobalError', 'Please login first')
          setTimeout(() => { router.push('/login') }, 1000)
          return
        }
        default: {
          throw new Error(res.msg)
        }
      }
    })
    .catch((err) => {
      submiting.value = false
      showError.value = true
      errorMsg.value = err.message
      clearTimeout(errorTimer.value)
      errorTimer.value = setTimeout(() => { showError.value = false }, 3000)
    })
})

watch(
  () => currentStep.value,
  (_, oldStep) => {
    if (oldStep === 0) {

    }
  }
)

onMounted(() => {
  if (route.query.name) {
    name.value.value = route.query.name
  }
  if (route.query.dataType) {
    dataType.value.value = route.query.dataType
  }
  if (route.query.taskType) {
    taskType.value.value = route.query.taskType
  }
  if (route.query.deviceType) {
    deviceType.value.value = JSON.parse(route.query.deviceType)
  }
  if (route.query.tagList) {
    tagList.value.value = JSON.parse(route.query.tagList)
  }
  if (route.query.description) {
    description.value.value = route.query.description
  }
})
</script>

<template>
  <v-container class="h-1/1">
    <v-card class="relative max-w-1000px w-1/1 m-auto">
      <v-scroll-y-transition>
        <v-card-actions v-if="success">
          <v-alert closable text="Submit successfully" type="success" @click:close="success = false" />
        </v-card-actions>
      </v-scroll-y-transition>
      <v-scroll-y-transition>
        <v-card-actions v-if="showError">
          <v-alert closable :text="errorMsg" type="error" @click:close="showError = false" />
        </v-card-actions>
      </v-scroll-y-transition>
      <v-stepper-title class="mt-2 mb-5 w-1/1" :steps="steps" :current-step="currentStep" @active-step="activeStep" />

      <v-divider class="border-black"></v-divider>

      <div class="w-1/1 mx-auto p-2">
        <v-card-title class="!md:text-2xl text-1rem">
          <span>{{ steps[currentStep].title }}</span>
        </v-card-title>

        <v-window v-model="currentStep">
          <v-window-item :value="0">
            <v-card-text>
              <v-text-field v-model="name.value.value" label="Name" placeholder="Awesome learnware"
                append-inner-icon="mdi-close" @click:append-inner="name.value.value = ''"
                :error-messages="name.errorMessage.value" counter="30"></v-text-field>
              <span class="text-caption text-grey-darken-1">
                This is the name of the learnware you contribute.
              </span>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="1">
            <v-card-text class="pt-0">
              <spec-tag v-model:data-type="dataType.value.value" v-model:task-type="taskType.value.value" v-model:device-type="deviceType.value.value" v-model:tag-list="tagList.value.value" :error-messages="dataType.errorMessage.value || taskType.errorMessage.value || deviceType.errorMessage.value || tagList.errorMessage.value" />
            </v-card-text>
          </v-window-item>

          <v-window-item :value="2">
            <div class="pa-4">
              <v-textarea v-model="description.value.value" label="Description"
                placeholder="This is a description of the learnware" :error-messages="description.errorMessage.value" counter="200"></v-textarea>
            </div>
          </v-window-item>

          <v-window-item :value="3">
            <div class="p-4 m-auto">
              <file-upload v-model:files="files.value.value"></file-upload>
            </div>
            <v-card-text class="text-lg">
              <span class="cursor-pointer" @click="router.push('/instruction')"><u>Click here</u></span> for
              instructions
              on how to create the required zip file.
            </v-card-text>
          </v-window-item>
        </v-window>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn v-if="currentStep > 0" variant="outlined" @click="PrevStep">
            Back
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn v-if="currentStep < steps.length - 1" color="primary" variant="flat" @click="nextStep" :disabled="!allowChangePage">
            Next
          </v-btn>
          <v-btn v-else color="primary" variant="flat" @click="submit" :disabled="submiting || !valid">
            Finish
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
    <v-dialog v-model="submiting" persistent class="max-w-600px w-1/1">
      <v-card class="p-2">
        <v-card-title class="my-4 text-center">
          <svg class="m-auto w-1/3" version="1.1" id="L1" xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 100 100"
            enable-background="new 0 0 100 100" xml:space="preserve">
            <circle fill="none" stroke-width="6" stroke-miterlimit="15" stroke-dasharray="14.2472,14.2472" cx="50" cy="50"
              r="47" style="stroke: rgb(var(--v-theme-primary))">
              <animateTransform attributeName="transform" attributeType="XML" type="rotate" dur="5s" from="0 50 50"
                to="360 50 50" repeatCount="indefinite" />
            </circle>
            <circle fill="none" stroke-width="1" stroke-miterlimit="10" stroke-dasharray="10,10" cx="50" cy="50" r="39"
              style="stroke: rgb(var(--v-theme-primary))">
              <animateTransform attributeName="transform" attributeType="XML" type="rotate" dur="5s" from="0 50 50"
                to="-360 50 50" repeatCount="indefinite" />
            </circle>
            <g style="fill: rgb(var(--v-theme-primary))">
              <rect x="30" y="35" width="5" height="30">
                <animateTransform attributeName="transform" dur="1s" type="translate" values="0 5 ; 0 -5; 0 5"
                  repeatCount="indefinite" begin="0.1" />
              </rect>
              <rect x="40" y="35" width="5" height="30">
                <animateTransform attributeName="transform" dur="1s" type="translate" values="0 5 ; 0 -5; 0 5"
                  repeatCount="indefinite" begin="0.2" />
              </rect>
              <rect x="50" y="35" width="5" height="30">
                <animateTransform attributeName="transform" dur="1s" type="translate" values="0 5 ; 0 -5; 0 5"
                  repeatCount="indefinite" begin="0.3" />
              </rect>
              <rect x="60" y="35" width="5" height="30">
                <animateTransform attributeName="transform" dur="1s" type="translate" values="0 5 ; 0 -5; 0 5"
                  repeatCount="indefinite" begin="0.4" />
              </rect>
              <rect x="70" y="35" width="5" height="30">
                <animateTransform attributeName="transform" dur="1s" type="translate" values="0 5 ; 0 -5; 0 5"
                  repeatCount="indefinite" begin="0.5" />
              </rect>
            </g>
          </svg>
        </v-card-title>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
.drag-hover {
  border: 2px dashed blue;
}
</style>