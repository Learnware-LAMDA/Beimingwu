<script setup lang="ts">
import { ref, computed, onActivated, onMounted } from "vue";
import { useDisplay } from "vuetify";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { useField, useForm } from "vee-validate";
import { useI18n } from "vue-i18n";
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

const { t } = useI18n();

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
    name(value: string) {
      if (value?.length >= 5) {
        return true;
      }
      return t("Submit.Name.Error.AtLeast5Chars");
    },
    dataType(value: string) {
      if (value?.length > 0) {
        return true;
      }
      return t("Submit.Tag.DataType.Error.NotEmpty");
    },
    taskType(value: string) {
      if (value?.length > 0) {
        return true;
      }
      return t("Submit.Tag.TaskType.Error.NotEmpty");
    },
    libraryType(value: string) {
      if (value?.length > 0) {
        return true;
      }
      return t("Submit.Tag.LibraryType.Error.NotEmpty");
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
    description(value: string) {
      if (value?.length >= 10) {
        return true;
      }
      return t("Submit.Description.Error.AtLeast10Chars");
    },
    files(value: File[]) {
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
const dataType = useField<string>("dataType");
const taskType = useField<string>("taskType");
const libraryType = useField<string>("libraryType");
const tagList = useField<string[]>("tagList");
const dataTypeDescription = useField<string>("dataTypeDescription");
const taskTypeDescription = useField<string>("taskTypeDescription");
const description = useField<string>("description");
const files = useField<File[]>("files");

const currentStep = ref(0);
const submiting = ref(false);
const success = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const errorTimer = ref<number>();
const uploadProgress = ref(0);

const steps = computed(() => [
  {
    title: t("Submit.Name.Title"),
    subtitle: t("Submit.Name.Name"),
    icon: "mdi-rename",
  },
  {
    title: t("Submit.Tag.Title"),
    subtitle: t("Submit.Tag.Tag"),
    icon: "mdi-label-multiple",
  },
  {
    title: t("Submit.Description.Title"),
    subtitle: t("Submit.Description.Description"),
    icon: "mdi-image-text",
  },
  {
    title: t("Submit.File.Title"),
    subtitle: t("Submit.File.File"),
    icon: "mdi-paperclip-plus",
  },
]);

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

function activeStep(index: number): void {
  if (
    valid.value ||
    index < currentStep.value ||
    (allowChangePage.value && index <= currentStep.value + 1)
  ) {
    currentStep.value = index;
  }
}

function nextStep(): void {
  if (currentStep.value < steps.value.length - 1) {
    activeStep(currentStep.value + 1);
  }
}

function PrevStep(): void {
  if (currentStep.value > 0) {
    activeStep(currentStep.value - 1);
  }
}

function onProgress(progress: number): void {
  uploadProgress.value = progress * 100;
}

const submit = handleSubmit((values) => {
  submiting.value = true;
  success.value = false;
  showError.value = false;
  uploadProgress.value = 0;

  addLearnware({
    edit: Boolean(route.query.edit),
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
    onProgress,
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
      errorTimer.value = Number(
        setTimeout(() => {
          showError.value = false;
        }, 3000),
      );
    })
    .finally(() => {
      submiting.value = false;
    });
});

function checkLoginStatus(): Promise<void> {
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
      errorTimer.value = Number(
        setTimeout(() => {
          showError.value = false;
        }, 3000),
      );
    })
    .finally(() => {
      submiting.value = false;
    });
}

function checkIsEditMode(): undefined | Promise<void> {
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

function init(): void {
  store.commit("setIsEditing", !!route.query.edit);
  checkLoginStatus().then(checkIsEditMode);
}

onMounted(init);

onActivated(init);
</script>

<template>
  <v-container class="h-1/1 <sm:p-0">
    <v-card class="relative max-w-1000px w-1/1 m-auto" :flat="display.name.value === 'xs'">
      <v-scroll-y-transition>
        <v-card-actions v-if="success">
          <v-alert
            closable
            :text="t('Submit.Success')"
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
        :step-title="t('Submit.Step')"
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
                :label="t('Submit.Name.Name')"
                :placeholder="t('Submit.Name.Placeholder')"
                append-inner-icon="mdi-close"
                :error-messages="name.errorMessage.value"
                counter="30"
                @click:append-inner="name.value.value = ''"
              ></v-text-field>
              <span class="text-caption text-grey-darken-1">
                {{ t("Submit.Name.Description") }}
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
                :label="t('Submit.Description.Description')"
                :placeholder="t('Submit.Description.Placeholder')"
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
              >
                {{ t("Submit.File.ClickHere") }}
              </a>
              {{ t("Submit.File.ForInstructionsOnHowToCreateTheRequiredZipFile") }}
            </v-card-text>
          </v-window-item>
        </v-window>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn v-if="currentStep > 0" variant="outlined" @click="PrevStep">
            {{ t("Submit.Navigation.PreviousStep") }}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            v-if="currentStep < steps.length - 1"
            color="primary"
            variant="flat"
            :disabled="!allowChangePage"
            @click="nextStep"
          >
            {{ t("Submit.Navigation.NextStep") }}
          </v-btn>
          <v-btn
            v-else
            color="primary"
            variant="flat"
            :disabled="submiting || !valid"
            @click="submit"
          >
            {{ t("Submit.Navigation.Finish") }}
          </v-btn>
        </v-card-actions>
      </div>
    </v-card>
    <submiting-dialog v-if="submiting" :progress="uploadProgress">
      <template #title>
        <span>{{ t("Submit.Submiting") }}</span>
      </template>
    </submiting-dialog>
  </v-container>
</template>
