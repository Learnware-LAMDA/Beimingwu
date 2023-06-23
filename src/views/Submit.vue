<script setup>
import { ref, onMounted, computed } from "vue";
import { useDisplay } from "vuetify";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { useField, useForm } from "vee-validate";
import { getRole } from "../request/auth";
import { addLearnware } from "../request/user";
import VStepperTitle from "../components/Public/VStepperTitle.vue";
import FileUpload from "../components/Specification/FileUpload.vue";
import SpecTag from "../components/Specification/SpecTag.vue";
import SubmitingDialog from "../components/Dialogs/SubmitingDialog.vue";

const route = useRoute();
const router = useRouter();

const display = useDisplay();

const store = useStore();

const { handleSubmit, meta } = useForm({
  initialValues: {
    name: "",
    dataType: "",
    taskType: "",
    libraryType: "",
    tagList: [],
    description: "",
    files: [],
  },
  validationSchema: {
    name(value) {
      if (value?.length >= 5) {
        return true;
      }
      return "Learnware name needs to be at least 5 characters.";
    },
    dataType(value) {
      if (value?.length > 0) {
        return true;
      }
      return "Data type must not be empty.";
    },
    taskType(value) {
      if (value?.length > 0) {
        return true;
      }
      return "Task type must not be empty.";
    },
    libraryType(value) {
      if (value?.length > 0) {
        return true;
      }
      return "Library type must not be empty.";
    },
    tagList() {
      return true;
    },
    description(value) {
      if (value?.length >= 10) {
        return true;
      }
      return "Description needs to be at least 10 characters.";
    },
    files(value) {
      if (value?.length > 0) {
        if (value[0].name.endsWith(".zip")) {
          return true;
        }
        return "You must upload a zip file.";
      }
      return "Please upload your model & statistical specification.";
    },
  },
});

const name = useField("name");
const dataType = useField("dataType");
const taskType = useField("taskType");
const libraryType = useField("libraryType");
const tagList = useField("tagList");
const description = useField("description");
const files = useField("files");

const currentStep = ref(0);
const submiting = ref(false);
const success = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const errorTimer = ref(null);

const steps = [
  {
    title: "Type the name of your learnware",
    subtitle: "Name",
    icon: "mdi-rename",
  },
  {
    title: "Choose the tags (semantic specification)",
    subtitle: "Tag",
    icon: "mdi-label-multiple",
  },
  {
    title: "Type the description (semantic specification)",
    subtitle: "Description",
    icon: "mdi-image-text",
  },
  {
    title: "Upload your model & statistical specification",
    subtitle: "File",
    icon: "mdi-paperclip-plus",
  },
];

const valid = computed(() => meta.value.valid);
const allowChangePage = computed(() => {
  switch (currentStep.value) {
    case 0: {
      return name.meta.valid;
    }
    case 1: {
      return (
        dataType.meta.valid && taskType.meta.valid && libraryType.meta.valid && tagList.meta.valid
      );
    }
    case 2: {
      return description.meta.valid;
    }
    case 3: {
      return files.meta.valid;
    }
    default: {
      return false;
    }
  }
});

function activeStep(index) {
  if (
    valid.value ||
    index < currentStep.value ||
    (allowChangePage.value && index <= currentStep.value + 1)
  ) {
    currentStep.value = index;
  }
}

function nextStep() {
  if (currentStep.value < steps.length - 1) {
    activeStep(currentStep.value + 1);
  }
}

function PrevStep() {
  if (currentStep.value > 0) {
    activeStep(currentStep.value - 1);
  }
}

const submit = handleSubmit((values) => {
  submiting.value = true;
  success.value = false;
  showError.value = false;

  addLearnware({
    name: values.name,
    dataType: values.dataType,
    taskType: values.taskType,
    libraryType: values.libraryType,
    tagList: values.tagList,
    description: values.description,
    files: values.files,
  })
    .then((res) => {
      console.log(res.code);
      console.log(typeof res.code);
      console.log(res.code === 0);
      switch (res.code) {
        case 0: {
          success.value = true;

          setTimeout(() => {
            success.value = false;
            router.go();
          }, 1000);
          return;
        }
        case 11: {
          store.commit("setLoggedIn", false);
          store.commit("setShowGlobalError", true);
          store.commit("setGlobalErrorMsg", "Please login first");
          setTimeout(() => {
            router.push("/login");
          }, 1000);
          return;
        }
        default: {
          throw new Error(res.msg);
        }
      }
    })
    .catch((err) => {
      console.log(err);
      showError.value = true;
      errorMsg.value = err.message;
      clearTimeout(errorTimer.value);
      errorTimer.value = setTimeout(() => {
        showError.value = false;
      }, 3000);
    })
    .finally(() => {
      submiting.value = false;
    });
});

function checkLoginStatus() {
  getRole()
    .then((res) => {
      switch (res.code) {
        case 0: {
          return;
        }
        case 11: {
          store.commit("setLoggedIn", false);
          store.commit("setShowGlobalError", true);
          store.commit("setGlobalErrorMsg", "Please login first");
          setTimeout(() => {
            router.push("/login");
          }, 1000);
          return;
        }
        default: {
          throw new Error(res.msg);
        }
      }
    })
    .catch((err) => {
      showError.value = true;
      errorMsg.value = err.message;
      clearTimeout(errorTimer.value);
      errorTimer.value = setTimeout(() => {
        showError.value = false;
      }, 3000);
    })
    .finally(() => {
      submiting.value = false;
    });
}

function loadQuery() {
  !!route.query.name && (name.value.value = route.query.name);
  !!route.query.dataType && (dataType.value.value = route.query.dataType);
  !!route.query.taskType && (taskType.value.value = route.query.taskType);
  !!route.query.libraryType && (libraryType.value.value = route.query.libraryType);
  !!route.query.tagList && (tagList.value.value = JSON.parse(route.query.tagList));
  !!route.query.description && (description.value.value = route.query.description);
}

onMounted(() => {
  checkLoginStatus();
  loadQuery();
});
</script>

<template>
  <v-container class="h-1/1 <sm:p-0">
    <v-card class="relative max-w-1000px w-1/1 m-auto" :flat="display.name.value === 'xs'">
      <v-scroll-y-transition>
        <v-card-actions v-if="success">
          <v-alert
            closable
            text="Submit successfully"
            type="success"
            @click:close="success = false"
          />
        </v-card-actions>
      </v-scroll-y-transition>
      <v-scroll-y-transition>
        <v-card-actions v-if="showError">
          <v-alert closable :text="errorMsg" type="error" @click:close="showError = false" />
        </v-card-actions>
      </v-scroll-y-transition>
      <v-stepper-title
        class="mt-2 mb-5 w-1/1"
        :steps="steps"
        :current-step="currentStep"
        @active-step="activeStep"
      />

      <v-divider class="border-black"></v-divider>

      <div class="w-1/1 mx-auto sm:px-2 pt-2 sm:pb-2">
        <v-card-title class="!md:text-2xl text-1.2rem <sm:pb-0">
          <span>{{ steps[currentStep].title }}</span>
        </v-card-title>

        <v-window v-model="currentStep" :touch="{ left: () => {}, right: () => {} }">
          <v-window-item :value="0">
            <v-card-text>
              <v-text-field
                v-model="name.value.value"
                label="Name"
                placeholder="Awesome learnware"
                append-inner-icon="mdi-close"
                :error-messages="name.errorMessage.value"
                counter="30"
                @click:append-inner="name.value.value = ''"
              ></v-text-field>
              <span class="text-caption text-grey-darken-1">
                This is the name of the learnware you contribute.
              </span>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="1">
            <v-card-text class="pt-0">
              <spec-tag
                v-model:data-type="dataType.value.value"
                v-model:task-type="taskType.value.value"
                v-model:library-type="libraryType.value.value"
                v-model:tag-list="tagList.value.value"
                :error-messages="
                  dataType.errorMessage.value ||
                  taskType.errorMessage.value ||
                  libraryType.errorMessage.value ||
                  tagList.errorMessage.value
                "
              />
            </v-card-text>
          </v-window-item>

          <v-window-item :value="2">
            <div class="pa-4">
              <v-textarea
                v-model="description.value.value"
                label="Description"
                placeholder="This is a description of the learnware"
                :error-messages="description.errorMessage.value"
                counter="200"
              ></v-textarea>
            </div>
          </v-window-item>

          <v-window-item :value="3">
            <div class="p-4 m-auto">
              <file-upload
                v-model:files="files.value.value"
                :error-messages="files.errorMessage.value"
              ></file-upload>
            </div>
            <v-card-text class="text-lg <sm:text-sm">
              <span class="cursor-pointer" @click="router.push('/instruction')"
                ><u>Click here</u></span
              >
              for instructions on how to create the required zip file.
            </v-card-text>
          </v-window-item>
        </v-window>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn v-if="currentStep > 0" variant="outlined" @click="PrevStep"> Back </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            v-if="currentStep < steps.length - 1"
            color="primary"
            variant="flat"
            :disabled="!allowChangePage"
            @click="nextStep"
          >
            Next
          </v-btn>
          <v-btn
            v-else
            color="primary"
            variant="flat"
            :disabled="submiting || !valid"
            @click="submit"
          >
            Finish
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
    <submiting-dialog v-if="submiting" />
  </v-container>
</template>
