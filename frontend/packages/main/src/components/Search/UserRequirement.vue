<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick } from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";
import { useDisplay } from "vuetify";
import { driver } from "driver.js";
import DataTypeBtns from "../Specification/SpecTag/DataType.vue";
import TaskTypeBtns from "../Specification/SpecTag/TaskType.vue";
import LibraryTypeBtns from "../Specification/SpecTag/LibraryType.vue";
import FileUpload from "../Specification/FileUpload.vue";
import ScenarioListBtns from "../Specification/SpecTag/ScenarioList.vue";
import LicenseTypeBtns from "../Specification/SpecTag/LicenseType.vue";
import DescriptionInput from "../Specification/DescriptionInput.vue";
import { saveContentToFile } from "../../utils";
import type { Filter } from "@beiming-system/types/learnware";
import TextBtn from "../../assets/images/specification/dataType/text.svg?component";
import ImageBtn from "../../assets/images/specification/dataType/image.svg?component";
import TableBtn from "../../assets/images/specification/dataType/table.svg?component";

export interface Props {
  modelValue: Filter;
  isAdmin?: boolean;
  allowHetero?: boolean;
  isHetero?: boolean;
  heteroDialog?: boolean;
  showExample?: boolean;
}

const { t } = useI18n();

const store = useStore();

const display = useDisplay();

const emits = defineEmits(["update:modelValue", "update:isHetero", "update:heteroDialog"]);

const props = withDefaults(defineProps<Props>(), {
  isAdmin: false,
  allowHetero: false,
  isHetero: false,
  heteroDialog: false,
  showExample: true,
});

const modelValue = computed<Filter>({
  get: () => props.modelValue,
  set: (val) => {
    emits("update:modelValue", val);
  },
});

const heteroDialog = computed({
  get: () => props.heteroDialog,
  set: (val) => {
    emits("update:heteroDialog", val);
  },
});
const heteroTab = ref<"dataType" | "taskType">("dataType");

const tempDataTypeDescription = ref(
  modelValue.value.dataTypeDescription ?? {
    Dimension: 7,
    Description: {
      0: "gender",
      1: "age",
      2: "the description of feature 2",
      5: "the description of feature 5",
    },
  },
);
const tempTaskTypeDescription = ref(
  modelValue.value.taskTypeDescription ?? {
    Dimension: 2,
    Description: {
      0: "the description of label 0",
      1: "the description of label 1",
    },
  },
);

const filterElement = ref<HTMLDivElement | null>(null);

const exampleDialog = ref<boolean>(false);
const exampleDialogPersistent = ref<boolean>(store.getters.getShowExampleTips);
const exampleLoading = ref(false);
const exampleGroups = computed(() => [
  {
    name: t("Search.Example.TableExamplesHomogeneous"),
    examples: [
      {
        icon: TableBtn,
        name: t("Search.Example.TableExampleHomogeneous1"),
        onClick: (): Promise<void> => {
          return downloadAndLoadRKME("./static/table_homo.json", "table_homo.json").then(() => {
            emits("update:isHetero", false);
            modelValue.value.dataType = "Table";
            modelValue.value.taskType = "";
            modelValue.value.libraryType = "";
            modelValue.value.scenarioList = [];
            modelValue.value.licenseList = [];
          });
        },
        onClickDownload: (): Promise<void> => {
          return fetch("./static/table_homo.json")
            .then((res) => res.text())
            .then((text) => {
              saveContentToFile(text, "application/json", "table_homo.json");
            });
        },
      },
    ],
  },
  {
    name: t("Search.Example.TableExamplesHeterogeneous"),
    examples: [
      {
        icon: TableBtn,
        name: t("Search.Example.TableExampleHeterogeneous1"),
        onClick: (): Promise<any> => {
          return downloadAndLoadRKME("./static/table_hetero.json", "table_hetero.json")
            .then(() => fetch("./static/table_hetero_input.json"))
            .then((res) => res.text())
            .then((text) => {
              modelValue.value.dataType = "Table";
              modelValue.value.taskType = "";
              modelValue.value.libraryType = "";
              modelValue.value.scenarioList = [];
              modelValue.value.licenseList = [];
              modelValue.value.dataTypeDescription = JSON.parse(text);
              tempDataTypeDescription.value = JSON.parse(text);
              heteroDialog.value = false;
              emits("update:isHetero", true);
            });
        },
        onClickDownload: (): Promise<void> => {
          return fetch("./static/table_hetero.json")
            .then((res) => res.text())
            .then((text) => {
              saveContentToFile(text, "application/json", "table_hetero.json");
            })
            .then(() => {
              return fetch("./static/table_hetero_input.json");
            })
            .then((res) => res.text())
            .then((text) => {
              saveContentToFile(text, "application/json", "table_hetero_input.json");
            });
        },
      },
    ],
  },
  {
    name: t("Search.Example.ImageExamples"),
    examples: [
      {
        icon: ImageBtn,
        name: t("Search.Example.ImageExample1"),
        onClick: (): Promise<void> => {
          return downloadAndLoadRKME("./static/image.json", "image.json").then(() => {
            emits("update:isHetero", false);
            modelValue.value.dataType = "Image";
            modelValue.value.taskType = "";
            modelValue.value.libraryType = "";
            modelValue.value.scenarioList = [];
            modelValue.value.licenseList = [];
          });
        },
        onClickDownload: (): Promise<void> => {
          return fetch("./static/image.json")
            .then((res) => res.text())
            .then((text) => {
              saveContentToFile(text, "application/json", "image.json");
            });
        },
      },
    ],
  },
  {
    name: t("Search.Example.TextExamples"),
    examples: [
      {
        icon: TextBtn,
        name: t("Search.Example.TextExample1"),
        onClick: (): Promise<void> => {
          return downloadAndLoadRKME("./static/text.json", "text.json").then(() => {
            emits("update:isHetero", false);
            modelValue.value.dataType = "Text";
            modelValue.value.taskType = "";
            modelValue.value.libraryType = "";
            modelValue.value.scenarioList = [];
            modelValue.value.licenseList = [];
          });
        },
        onClickDownload: (): Promise<void> => {
          return fetch("./static/text.json")
            .then((res) => res.text())
            .then((text) => {
              saveContentToFile(text, "application/json", "text.json");
            });
        },
      },
    ],
  },
]);
function reset(): void {
  modelValue.value.id = "";
  modelValue.value.name = "";
  modelValue.value.dataType = "";
  modelValue.value.taskType = "";
  modelValue.value.libraryType = "";
  modelValue.value.scenarioList = [];
  modelValue.value.licenseList = [];
  modelValue.value.dataTypeDescription = undefined;
  modelValue.value.taskTypeDescription = undefined;
  modelValue.value.files = [];

  if (filterElement.value) {
    filterElement.value.scrollTo({ top: 0, behavior: "smooth" });
  }
}
function handleClickShowExample(): void {
  if (driverObj.isActive()) {
    setTimeout(() => {
      driverObj.moveNext();
    }, 500);
  }
}
function useExampleOnClick(onClick: () => Promise<void>): () => Promise<void> {
  return () => {
    if (driverObj.isActive()) {
      driverObj.moveNext();
    }
    exampleLoading.value = true;
    return onClick().finally(() => {
      exampleLoading.value = false;
    });
  };
}
function downloadAndLoadRKME(url: string, name: string): Promise<void> {
  return fetch(url)
    .then((res) => res.text())
    .then((text) => {
      const file = new File([text], name, { type: "application/json" });
      modelValue.value.files = [file];
    });
}

watch(
  () => heteroDialog.value,
  (val) => {
    if (!val) {
      emits("update:isHetero", true);
      modelValue.value.dataTypeDescription = tempDataTypeDescription.value;
      modelValue.value.taskTypeDescription = tempTaskTypeDescription.value;
    }
  },
);

const driverObj = driver({
  showButtons: ["close", "next", "previous"],
  nextBtnText: t("Search.Example.Next"),
  prevBtnText: t("Search.Example.Previous"),
  doneBtnText: t("Search.Example.Done"),
  onDestroyed: () => {
    exampleDialogPersistent.value = false;
  },
});

onMounted(() => {
  nextTick(() => {
    if (props.showExample && store.getters.getShowExampleTips) {
      store.dispatch("showExampleTips");
      driverObj.setSteps([
        {
          element: "#example-btn",
          popover: {
            side: "bottom",
            title: t("Search.Example.Examples"),
            description: t("Search.Example.ClickHereForExamples"),
            onNextClick(): void {
              exampleDialog.value = true;

              setTimeout(() => {
                driverObj.moveNext();
              }, 500);
            },
          },
        },
        {
          element: "#example-card-0-0",
          popover: {
            side: "bottom",
            title: t("Search.Example.Examples"),
            description: t("Search.Example.ClickHereForHomogeneousTableExample"),
            onNextClick(): void {
              exampleDialog.value = false;
              useExampleOnClick(exampleGroups.value[0].examples[0].onClick)();
              driverObj.moveNext();
            },
            onPrevClick(): void {
              exampleDialog.value = false;
              driverObj.movePrevious();
            },
          },
        },
      ]);

      driverObj.drive();
    }
  });
});
</script>

<template>
  <div class="sm:border-r-1 relative flex flex-col">
    <v-btn
      class="absolute right-4 top-2 z-20 bg-white opacity-40 transition-all hover:opacity-100"
      icon="mdi-close"
      variant="flat"
      @click="reset"
    />
    <div
      ref="filterElement"
      class="filter"
    >
      <slot name="prepend" />
      <div class="text-h6 mb-1 mt-2 md:my-2">
        <v-icon
          class="!mt-0 mr-3"
          icon="mdi-tag-text"
          color="black"
          size="small"
        />
        {{ t("Search.ChooseSemanticRequirement") }}
      </div>

      <div v-if="isAdmin">
        <div class="text-h6 mb-3 mt-7 !text-base">
          {{ t("Search.SearchById") }}
        </div>
        <v-text-field
          v-model="modelValue.id"
          :label="t('Search.LearnwareId')"
          hide-details
          append-inner-icon="mdi-close"
          @click:append-inner="modelValue.id = ''"
        />
      </div>

      <div>
        <div class="text-h6 mb-3 mt-4 !text-base">
          {{ t("Search.SearchByName") }}
        </div>
        <v-text-field
          v-model="modelValue.name"
          :label="t('Search.LearnwareName')"
          hide-details
          append-inner-icon="mdi-close"
          @click:append-inner="modelValue.name = ''"
        />
      </div>

      <data-type-btns
        v-model="modelValue.dataType"
        :cols="3"
        :md="2"
        :sm="2"
        :xs="2"
      />
      <task-type-btns
        v-model="modelValue.taskType"
        :cols="2"
        :md="2"
        :sm="2"
        :xs="2"
      />
      <library-type-btns
        v-model="modelValue.libraryType"
        :cols="2"
        :md="2"
        :sm="2"
        :xs="2"
      />
      <scenario-list-btns
        v-model="modelValue.scenarioList"
        :cols="2"
        :md="2"
        :sm="2"
        :xs="2"
        class="bg-transparent !text-base"
      />
      <license-type-btns
        v-model="modelValue.licenseList"
        :cols="2"
        :md="2"
        :sm="2"
        :xs="2"
        class="bg-transparent !text-base"
      />
      <slot name="append" />
    </div>

    <div class="border-t-1 border-gray-300 p-4 pt-0">
      <template v-if="allowHetero">
        <div class="text-h6 mb-5 mt-3 w-full truncate transition-all">
          <v-icon
            class="mr-3"
            icon="mdi-vector-difference"
            color="black"
            size="small"
          />
          {{ t("Search.UploadHeterogeneousRequirement") }}
        </div>

        <v-card
          flat
          class="border-gray-500 bg-transparent"
        >
          <v-btn
            block
            color="primary"
            variant="flat"
            @click="
              () => {
                heteroDialog = true;
              }
            "
          >
            {{
              isHetero
                ? t("Search.ChangeHeterogeneousRequirement")
                : t("Search.StartHeterogeneousSearch")
            }}
          </v-btn>
          <v-btn
            v-if="isHetero"
            block
            variant="outlined"
            class="mt-2"
            @click="() => emits('update:isHetero', false)"
          >
            {{ t("Search.TurnOffHeterogeneousSearch") }}
          </v-btn>
        </v-card>

        <v-dialog
          v-if="true"
          v-model="heteroDialog"
          width="1024"
        >
          <v-card class="p-4 md:p-8 md:pt-4">
            <div>
              <v-tabs
                v-model="heteroTab"
                align-tabs="center"
              >
                <v-tab value="dataType">
                  {{ t("Submit.SemanticSpecification.DataType.DescriptionInput.Name") }}
                </v-tab>
                <v-tab value="taskType">
                  {{ t("Submit.SemanticSpecification.TaskType.DescriptionOutput.Name") }}
                </v-tab>
              </v-tabs>
            </div>

            <v-window
              v-model="heteroTab"
              class="overflow-y-auto md:overflow-y-hidden"
            >
              <v-window-item value="dataType">
                <div class="flex justify-between">
                  <div class="text-h4 mt-2 text-2xl font-semibold md:text-3xl xl:text-4xl">
                    {{ t("Submit.SemanticSpecification.DataType.DescriptionInput.Name") }}
                  </div>
                  <v-btn
                    icon="mdi-download"
                    variant="flat"
                    :size="display.smAndUp.value ? 'default' : 'small'"
                    @click="
                      () =>
                        saveContentToFile(
                          JSON.stringify(tempDataTypeDescription, undefined, 2),
                          'text/json',
                          'dataTypeDescription.json',
                        )
                    "
                  />
                </div>
                <description-input
                  v-model="tempDataTypeDescription"
                  :name="t('Submit.SemanticSpecification.DataType.DescriptionInput.Name')"
                  class="mt-4"
                />
              </v-window-item>

              <v-window-item value="taskType">
                <div class="flex justify-between">
                  <div class="text-h4 mt-4 text-2xl font-semibold md:text-3xl xl:text-4xl">
                    {{ t("Submit.SemanticSpecification.TaskType.DescriptionOutput.Name") }}
                  </div>
                  <v-btn
                    icon="mdi-download"
                    variant="flat"
                    @click="
                      () =>
                        saveContentToFile(
                          JSON.stringify(tempTaskTypeDescription, undefined, 2),
                          'text/json',
                          'dataTypeDescription.json',
                        )
                    "
                  />
                </div>
                <description-input
                  v-model="tempTaskTypeDescription"
                  :name="t('Submit.SemanticSpecification.TaskType.DescriptionOutput.Name')"
                  class="mt-4"
                />
              </v-window-item>
            </v-window>

            <div class="mt-4 flex justify-end">
              <v-btn
                color="primary"
                rounded
                variant="flat"
                @click="heteroDialog = false"
              >
                {{ t("Public.Finish") }}
              </v-btn>
            </div>
          </v-card>
        </v-dialog>
      </template>

      <div class="text-h6 mb-5 mt-3 flex w-full items-center truncate transition-all">
        <v-icon
          class="mr-3"
          icon="mdi-upload"
          color="black"
          size="small"
        />
        {{ t("Search.UploadStatisticalRequirement") }}
        <v-spacer class="flex-1" />

        <v-dialog
          v-if="showExample"
          v-model="exampleDialog"
          :persistent="exampleDialogPersistent"
          class="mx-auto w-full max-w-2xl"
        >
          <template #activator="{ props: dialogProps }">
            <v-btn
              v-bind="dialogProps"
              id="example-btn"
              variant="flat"
              color="transparent"
              icon="mdi-list-box"
              @click="handleClickShowExample"
            />
          </template>

          <v-card
            id="example-dialog"
            flat
            class="p-4 md:p-6"
            :loading="exampleLoading"
          >
            <div class="flex items-start justify-between">
              <span class="text-xl md:text-4xl">
                {{ t("Search.Example.Examples") }}
              </span>
              <v-btn
                variant="flat"
                icon="mdi-close"
                :size="display.smAndUp.value ? 'default' : 'x-small'"
                @click="exampleDialog = false"
              />
            </div>
            <div class="my-1 text-xs text-gray-500 md:text-lg">
              {{ t("Search.Example.ExamplesDescription") }}
            </div>

            <template
              v-for="(group, i) in exampleGroups"
              :key="i"
            >
              <div class="text-h6 mt-2 text-sm md:my-2 md:text-xl">
                {{ group.name }}
              </div>
              <div
                v-for="(example, j) in group.examples"
                :key="example.name"
                class="flex items-center"
              >
                <v-card
                  :id="`example-card-${i}-${j}`"
                  flat
                  class="my-1 flex flex-1 items-center rounded-md border p-3 md:my-2 md:p-4"
                  @click="
                    () =>
                      useExampleOnClick(example.onClick)().finally(() => (exampleDialog = false))
                  "
                >
                  <div class="flex items-center">
                    <component
                      :is="example.icon"
                      class="w-4 md:w-8"
                    />
                    <div class="ml-2 text-center text-xs md:ml-3 md:text-lg">
                      {{ example.name }}
                    </div>
                  </div>
                </v-card>
                <div>
                  <v-btn
                    variant="flat"
                    icon="mdi-download"
                    color="transparent"
                    :size="display.smAndUp.value ? 'default' : 'x-small'"
                    @click.stop="() => useExampleOnClick(example.onClickDownload)()"
                  />
                </div>
              </div>
            </template>
          </v-card>
        </v-dialog>
      </div>

      <file-upload
        v-model="modelValue.files"
        :height="28"
        :tips="t('Submit.File.DragFileHere', { file: 'JSON' })"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.filter {
  @apply w-full p-2 sm:px-5 md:h-full md:overflow-y-auto;

  & > * {
    @apply mt-2;
  }
}
</style>
