<script setup lang="ts">
import { ref, computed, onActivated, onMounted } from "vue";
import { useDisplay } from "vuetify";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { useI18n } from "vue-i18n";
import { getRole } from "../request/auth";
import { addLearnware } from "../request/user";
import { getLearnwareDetailById } from "../request/engine";
import { promiseReadFile, verifyLearnware, html2Markdown } from "../utils";
import type {
  Name,
  DataType,
  TaskType,
  LibraryType,
  ScenarioList,
  LicenseList,
  Description,
} from "@beiming-system/types/learnware";
import { useField } from "@beiming-system/hooks";
import VStepperTitle from "../components/Public/VStepperTitle.vue";
import FileUpload from "../components/Specification/FileUpload.vue";
import SpecTag from "../components/Specification/SpecTag.vue";
import SubmitingDialog from "../components/Dialogs/SubmitingDialog.vue";

const route = useRoute();
const router = useRouter();

const display = useDisplay();

const store = useStore();

const { t, locale } = useI18n();

const name = useField<Name>({
  defaultValue: "",
  validate: (value: Name): string => {
    if (value?.length < 5) {
      return t("Submit.Name.Error.FewerThan5Chars");
    }
    if (value?.length > 50) {
      return t("Submit.Name.Error.MoreThan50Chars");
    }
    return "";
  },
});
const dataType = useField<DataType | "">({
  defaultValue: "",
  validate: (value: DataType | ""): string => {
    if (value?.length > 0) {
      return "";
    }
    return t("Submit.SemanticSpecification.DataType.Error.NotEmpty");
  },
});
const taskType = useField<TaskType | "">({
  defaultValue: "",
  validate: (value: TaskType | ""): string => {
    if (value?.length > 0) {
      return "";
    }
    return t("Submit.SemanticSpecification.TaskType.Error.NotEmpty");
  },
});
const libraryType = useField<LibraryType | "">({
  defaultValue: "",
  validate: (value: LibraryType | ""): string => {
    if (value?.length > 0) {
      return "";
    }
    return t("Submit.SemanticSpecification.LibraryType.Error.NotEmpty");
  },
});
const scenarioList = useField<ScenarioList>({
  defaultValue: [],
  validate: (value: ScenarioList): string => {
    if (value.length > 0) {
      return "";
    }
    return t("Submit.SemanticSpecification.Scenario.Error.NotEmpty");
  },
});
const licenseList = useField<LicenseList>({
  defaultValue: [],
  validate: (value: LicenseList): string => {
    if (value.length > 0) {
      return "";
    }
    return t("Submit.SemanticSpecification.License.Error.NotEmpty");
  },
});
const dataTypeDescription = useField<string>({
  defaultValue: JSON.stringify({
    Dimension: 7,
    Description: {
      0: "gender",
      1: "age",
      2: "the description of feature 2",
      5: "the description of feature 5",
    },
  }),
});
const taskTypeDescriptionClassification = useField<string>({
  defaultValue: JSON.stringify({
    Dimension: 3,
    Description: {
      0: "cat",
      1: "dog",
      2: "bird",
    },
  }),
});
const taskTypeDescriptionRegression = useField<string>({
  defaultValue: JSON.stringify({
    Dimension: 1,
    Description: {
      0: "store sales for the day",
    },
  }),
});
const taskTypeDescription = computed(() => {
  if (taskType.value === "Classification") {
    return taskTypeDescriptionClassification.value;
  } else if (taskType.value === "Regression") {
    return taskTypeDescriptionRegression.value;
  } else {
    return JSON.stringify({
      Dimension: 1,
      Description: {
        0: "",
      },
    });
  }
});
const description = useField<Description>({
  defaultValue:
    "# Description\n## This is a learnware\n\nThis learnware has the following tree features:\n\n1. feature 1\n2. feature 2\n3. feature 3",
  validate: (value: Description): string => {
    if (value?.length < 10) {
      return t("Submit.Description.Error.FewerThan10Chars");
    }
    if (value?.length > 10000) {
      return t("Submit.Description.Error.MoreThan10000Chars");
    }
    return "";
  },
});
const files = useField<File[]>({
  defaultValue: [],
  validate: (value): string | Promise<string> => {
    if (route.query.edit && value[0]?.name === t("Submit.File.YourOldLearnware")) {
      return "";
    }
    if (!value.length || value.length === 0) {
      return t("Submit.File.Error.NoFile");
    }
    if (!value[0].name.endsWith(".zip")) {
      return t("Submit.File.Error.NotZipFile");
    }
    if (value[0].size > 1024 * 1024 * 1024) {
      return t("Submit.File.Error.GreaterThan1GB");
    }
    return promiseReadFile(value[0])
      .then((file) => verifyLearnware(file, t))
      .catch((err) => {
        console.log(err);
        return err.message;
      });
  },
});

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
    title: t("Submit.SemanticSpecification.Title"),
    subtitle: t("Submit.SemanticSpecification.Tag"),
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

const valid = computed(
  () =>
    name.valid &&
    dataType.valid &&
    taskType.valid &&
    libraryType.valid &&
    scenarioList.valid &&
    licenseList.valid &&
    description.valid &&
    files.valid,
);
const allowChangePage = computed(() => {
  switch (currentStep.value) {
    case 0: {
      return name.valid;
    }
    case 1: {
      return (
        dataType.valid &&
        taskType.valid &&
        libraryType.valid &&
        scenarioList.valid &&
        licenseList.valid
      );
    }
    case 2: {
      return description.valid;
    }
    case 3: {
      return files.valid;
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

function submit(): Promise<void> {
  if (!valid.value) {
    return Promise.reject(new Error("Invalid form"));
  }

  submiting.value = true;
  success.value = false;
  showError.value = false;
  uploadProgress.value = 0;

  function onProgress(progress: number): void {
    uploadProgress.value = progress * 100;
  }

  return addLearnware({
    edit: Boolean(route.query.edit),
    name: name.value,
    dataType: dataType.value as DataType,
    taskType: taskType.value as TaskType,
    libraryType: libraryType.value as LibraryType,
    scenarioList: scenarioList.value,
    licenseList: licenseList.value,
    dataTypeDescription: dataTypeDescription.value,
    taskTypeDescription: taskTypeDescription.value,
    description: description.value,
    files: files.value,
    learnwareId: String(route.query.id),
    onProgress,
  })
    .then((res) => {
      switch (res.code) {
        case 0: {
          success.value = true;

          setTimeout(() => {
            success.value = false;
            // set editing mode to remount submit page
            store.commit("setIsEditing", true);

            router.push({
              path: "/learnwaredetail",
              query: {
                id: res.data.learnware_id,
              },
            });
          }, 1000);
          return;
        }
        case 11: {
          store.dispatch("logout");
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
}

function checkLoginStatus(): Promise<void> {
  return getRole()
    .then((res) => {
      switch (res.code) {
        case 0: {
          return;
        }
        case 11: {
          store.dispatch("logout");
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
    return getLearnwareDetailById({ id: String(route.query.id) })
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
            name.value = semanticSpec.Name.Values;
            description.value = semanticSpec.Description.Values;
            dataType.value = semanticSpec.Data.Values[0];
            taskType.value = semanticSpec.Task.Values[0];
            libraryType.value = semanticSpec.Library.Values[0];
            scenarioList.value = semanticSpec.Scenario.Values;
            licenseList.value = semanticSpec.License.Values;
            if (semanticSpec.Input) {
              dataTypeDescription.value = JSON.stringify(semanticSpec.Input);
            } else {
              dataTypeDescription.value = JSON.stringify({
                Dimension: 2,
                Description: {
                  0: "You have not provided a description of the input data",
                  1: "Please read the tips and provide a description of the input data",
                },
              });
            }
            if (semanticSpec.Output.Dimension && semanticSpec.Output.Description) {
              taskTypeDescriptionClassification.value = taskTypeDescriptionRegression.value =
                JSON.stringify(semanticSpec.Output);
            } else {
              taskTypeDescriptionClassification.value = taskTypeDescriptionRegression.value =
                JSON.stringify({
                  Dimension: 2,
                  Description: {
                    0: "You have not provided a description of the output data",
                    1: "Please read the tips and provide a description of the output data",
                  },
                });
            }
            files.value = [new File([], t("Submit.File.YourOldLearnware"))];
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
  <v-container class="sm:p-none h-full p-0">
    <v-card
      class="relative m-auto w-full max-w-[1000px]"
      :flat="display.name.value === 'xs'"
    >
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
          <v-alert
            closable
            :text="errorMsg"
            type="error"
            @click:close="showError = false"
          />
        </v-card-actions>
      </v-scroll-y-transition>
      <v-stepper-title
        class="mb-5 mt-2 w-full"
        :step-title="t('Submit.Step')"
        :steps="steps"
        :current-step="currentStep"
        @active-step="activeStep"
      />

      <v-divider class="border-black" />

      <div class="mx-auto w-full pt-2 sm:px-2 sm:pb-2">
        <v-card-title class="text-1.2rem sm:pb-none pb-0 md:text-2xl">
          <span>{{ steps[currentStep].title }}</span>
        </v-card-title>

        <v-window
          v-model="currentStep"
          :touch="{ left: () => {}, right: () => {} }"
        >
          <v-window-item :value="0">
            <v-card-text>
              <v-text-field
                v-model="name.value"
                :label="t('Submit.Name.Name')"
                :placeholder="t('Submit.Name.Placeholder')"
                append-inner-icon="mdi-close"
                :error-messages="name.errorMessages"
                :counter="50"
                @click:append-inner="name.value = ''"
              />
              <span class="text-caption text-grey-darken-1">
                {{ t("Submit.Name.Description") }}
              </span>
            </v-card-text>
          </v-window-item>

          <v-window-item :value="1">
            <v-card-text class="pt-0">
              <spec-tag
                v-model:data-type="dataType.value"
                v-model:task-type="taskType.value"
                v-model:library-type="libraryType.value"
                v-model:scenario-list="scenarioList.value"
                v-model:license-list="licenseList.value"
                v-model:data-type-description="dataTypeDescription.value"
                v-model:task-type-description-classification="
                  taskTypeDescriptionClassification.value
                "
                v-model:task-type-description-regression="taskTypeDescriptionRegression.value"
                :error-messages="
                  dataType.errorMessages ||
                  taskType.errorMessages ||
                  libraryType.errorMessages ||
                  scenarioList.errorMessages ||
                  licenseList.errorMessages
                "
              />
            </v-card-text>
          </v-window-item>

          <v-window-item :value="2">
            <div class="grid h-[30rem] p-4 md:grid-cols-2 md:gap-4">
              <div class="flex-1 overflow-y-auto">
                <v-textarea
                  v-model="description.value"
                  auto-grow
                  :label="t('Submit.Description.Description')"
                  :placeholder="t('Submit.Description.Placeholder')"
                  :error-messages="description.errorMessages"
                  :counter="10000"
                />
              </div>
              <div
                class="markdown-content flex-1 overflow-y-auto"
                v-html="html2Markdown(description.value)"
              ></div>
            </div>
          </v-window-item>

          <v-window-item :value="3">
            <div class="m-auto p-4">
              <file-upload
                v-model="files.value"
                :error-messages="files.errorMessages"
                :tips="t('Submit.File.DragFileHere', { file: 'zip' })"
              />
            </div>
            <v-card-text class="py-2 text-sm sm:text-lg">
              <a
                class="text-black underline"
                :href="`https://docs.bmwu.cloud/${
                  locale === 'zh-cn' ? 'zh-CN' : 'en'
                }/user-guide/learnware-upload/prepare.html`"
                target="_blank"
              >
                {{ t("Submit.File.ClickHere") }}
              </a>
              {{ t("Submit.File.ForInstructionsOnHowToCreateTheRequiredZipFile") }}
            </v-card-text>
            <v-card-text class="pt-2 text-sm sm:text-lg">
              <a
                class="text-black underline"
                href="./static/learnware-template.zip"
                target="_blank"
              >
                {{ t("Submit.File.ClickHere") }}
              </a>
              {{ t("Submit.File.ToDownloadTemplate") }}
            </v-card-text>
          </v-window-item>
        </v-window>

        <v-divider />

        <v-card-actions>
          <v-btn
            v-if="currentStep > 0"
            variant="outlined"
            @click="PrevStep"
          >
            {{ t("Submit.Navigation.PreviousStep") }}
          </v-btn>
          <v-spacer class="flex-1" />
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
    <submiting-dialog
      v-if="submiting"
      :progress="uploadProgress"
    >
      <template #title>
        <span>{{ t("Submit.Submiting") }}</span>
      </template>
    </submiting-dialog>
  </v-container>
</template>

<style scoped lang="scss">
.markdown-content {
  :deep(ol),
  :deep(ul) {
    @apply list-inside;
  }

  :deep(h1),
  :deep(h2),
  :deep(h3),
  :deep(h4),
  :deep(h5),
  :deep(h6) {
    @apply mb-2 mt-4;
  }
}
</style>
