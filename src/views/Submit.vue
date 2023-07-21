<script setup>
import { ref, computed, onActivated, onMounted } from "vue";
import { useDisplay } from "vuetify";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { useField, useForm } from "vee-validate";
import { getRole } from "../request/auth";
import { addLearnware } from "../request/user";
import { getLearnwareDetailById } from "../request/engine";
import { promiseReadFile, verifyLearnware } from "../utils";
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
    dataTypeDescription: JSON.stringify({
      Dimension: 7,
      Description: {
        0: "gender",
        1: "age",
        2: "f2",
        5: "f5",
      },
    }),
    taskTypeDescription: JSON.stringify({
      Dimension: 3,
      Description: {
        0: "the probability of being a cat",
        1: "the probability of being a dog",
        2: "the probability of being a bird",
      },
    }),
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
    dataTypeDescription() {
      // try {
      //   JSON.parse(value);
      // } catch (err) {
      //   return "Data type description must be a valid JSON string.";
      // }
      return true;
    },
    taskTypeDescription() {
      return true;
    },
    description(value) {
      if (value?.length >= 10) {
        return true;
      }
      return "Description needs to be at least 10 characters.";
    },
    files(value) {
      if (route.query.edit && value[0]?.name === "Your old learnware") {
        return true;
      }
      if (!value.length || value.length === 0) {
        return "Please upload your model & statistical specification.";
      }
      if (!value[0].name.endsWith(".zip")) {
        return "You must upload a zip file.";
      }
      if (value[0].size > 1024 * 1024 * 1024) {
        return "File size must be less than 1GB.";
      }
      return promiseReadFile(value[0]).then(verifyLearnware);
    },
  },
});

const name = useField("name");
const dataType = useField("dataType");
const taskType = useField("taskType");
const libraryType = useField("libraryType");
const tagList = useField("tagList");
const dataTypeDescription = useField("dataTypeDescription");
const taskTypeDescription = useField("taskTypeDescription");
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
    edit: route.query.edit,
    name: values.name,
    dataType: values.dataType,
    taskType: values.taskType,
    libraryType: values.libraryType,
    tagList: values.tagList,
    dataTypeDescription: values.dataTypeDescription,
    taskTypeDescription: values.taskTypeDescription,
    description: values.description,
    files: values.files,
    learnwareId: route.query.id,
  })
    .then((res) => {
      switch (res.code) {
        case 0: {
          success.value = true;

          setTimeout(() => {
            success.value = false;
            router.push("/submit");
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
  return getRole()
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

function checkIsEditMode() {
  if (!!route.query.edit && !!route.query.id) {
    return getLearnwareDetailById({ id: route.query.id })
      .then((res) => {
        switch (res.code) {
          case 0: {
            if (!res.data || !res.data.learnware_info) {
              throw new Error("Learnware not found");
            }
            if (!res.data.learnware_info.semantic_specification) {
              throw new Error("Learnware semantic specification not found");
            }
            currentStep.value = 0;
            const semanticSpec = res.data.learnware_info.semantic_specification;
            name.value.value = semanticSpec.Name.Values;
            description.value.value = semanticSpec.Description.Values;
            dataType.value.value = semanticSpec.Data.Values[0];
            taskType.value.value = semanticSpec.Task.Values[0];
            libraryType.value.value = semanticSpec.Library.Values[0];
            tagList.value.value = semanticSpec.Scenario.Values;
            if (semanticSpec.Input) {
              dataTypeDescription.value.value = JSON.stringify(semanticSpec.Input);
            } else {
              dataTypeDescription.value.value = JSON.stringify({
                Dimension: 2,
                Description: {
                  0: "You have not provided a description of the input data",
                  1: "Please read the tips and provide a description of the input data",
                },
              });
            }
            if (semanticSpec.Output) {
              taskTypeDescription.value.value = JSON.stringify(semanticSpec.Output);
            } else {
              taskTypeDescription.value.value = JSON.stringify({
                Dimension: 2,
                Description: {
                  0: "You have not provided a description of the output data",
                  1: "Please read the tips and provide a description of the output data",
                },
              });
            }
            files.value.value = [new File([], "Your old learnware")];
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
      });
  }
}

onMounted(() => {
  store.commit("setIsEditing", !!route.query.edit);
});

onActivated(() => {
  checkLoginStatus().then(checkIsEditMode);
  console.log(`hello from submit page: ${!!route.query.edit}`);
  store.commit("setIsEditing", !!route.query.edit);
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
                v-model:data-type-description="dataTypeDescription.value.value"
                v-model:task-type-description="taskTypeDescription.value.value"
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
              <a
                class="underline"
                href="http://36.111.128.21:30006/workflow/submit.html"
                target="_blank"
                >Click here</a
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
