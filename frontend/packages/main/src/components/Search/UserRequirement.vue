<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useRoute } from "vue-router";
import { useI18n } from "vue-i18n";
import DataTypeBtns from "../Specification/SpecTag/DataType.vue";
import TaskTypeBtns from "../Specification/SpecTag/TaskType.vue";
import LibraryTypeBtns from "../Specification/SpecTag/LibraryType.vue";
import FileUpload from "../Specification/FileUpload.vue";
import ScenarioListBtns from "../Specification/SpecTag/ScenarioList.vue";
import DescriptionInput from "../Specification/DescriptionInput.vue";
import { saveContentToFile } from "../../utils";
import type { DataType, TaskType, LibraryType, Filter } from "@beiming-system/types/learnware";

export interface Props {
  modelValue: Filter;
  isAdmin?: boolean;
  isHeterogeneous?: boolean;
}

const { t } = useI18n();

const emits = defineEmits(["update:modelValue"]);

withDefaults(defineProps<Props>(), {
  isAdmin: false,
  isHeterogeneous: false,
});

const route = useRoute();

const id = ref(route.query.id || "");
const search = ref(route.query.search || "");
const dataType = ref<DataType | "">((route.query.dataType?.toString() as DataType) || "");
const taskType = ref<TaskType | "">((route.query.taskType?.toString() as TaskType) || "");
const libraryType = ref<LibraryType | "">(
  (route.query.libraryType?.toString() as LibraryType) || "",
);
let tryScenarioList;
try {
  tryScenarioList = JSON.parse(route.query.scenarioList?.toString() as string);
} catch {
  tryScenarioList = [];
}
const scenarioList = ref(tryScenarioList);

const files = ref([]);

const heterDialog = ref(false);
const heterTab = ref<"dataType" | "taskType">("dataType");
const dataTypeDescription = ref({
  Dimension: 7,
  Description: {
    0: "gender",
    1: "age",
    2: "the description of feature 2",
    5: "the description of feature 5",
  },
});
const taskTypeDescription = ref({
  Dimension: 2,
  Description: {
    0: "the description of label 0",
    1: "the description of label 1",
  },
});
const tempDataTypeDescription = ref(dataTypeDescription.value);
const tempTaskTypeDescription = ref(taskTypeDescription.value);

const requirement = computed(() => ({
  id: id.value,
  name: search.value,
  dataType: dataType.value,
  taskType: taskType.value,
  libraryType: libraryType.value,
  scenarioList: scenarioList.value,
  files: files.value,
  dataTypeDescription: dataTypeDescription.value,
  taskTypeDescription: taskTypeDescription.value,
}));

watch(
  () => heterDialog.value,
  (val) => {
    if (!val) {
      dataTypeDescription.value = tempDataTypeDescription.value;
      taskTypeDescription.value = tempTaskTypeDescription.value;
    }
  },
);

watch(
  () => requirement.value,
  () => {
    emits("update:modelValue", requirement.value);
  },
);
</script>

<template>
  <div class="flex flex-col w-full sm:border-r-1">
    <div class="filter">
      <slot name="prepend" />
      <div class="my-3 text-h6">
        <v-icon class="!mt-0 mr-3" icon="mdi-tag-text" color="black" size="small"></v-icon>
        {{ t("Search.ChooseSemanticRequirement") }}
      </div>

      <div v-if="isAdmin">
        <div class="mt-7 mb-3 text-h6 !text-base">
          {{ t("Search.SearchById") }}
        </div>
        <v-text-field
          v-model="id"
          :label="t('Search.LearnwareId')"
          hide-details
          append-inner-icon="mdi-close"
          @click:append-inner="id = ''"
        ></v-text-field>
      </div>

      <div>
        <div class="mt-7 mb-3 text-h6 !text-base">
          {{ t("Search.SearchByName") }}
        </div>
        <v-text-field
          v-model="search"
          :label="t('Search.LearnwareName')"
          hide-details
          append-inner-icon="mdi-close"
          @click:append-inner="search = ''"
        ></v-text-field>
      </div>

      <data-type-btns v-model="dataType" :cols="3" :md="2" :sm="2" :xs="2"></data-type-btns>
      <task-type-btns v-model="taskType" :cols="2" :md="2" :sm="2" :xs="2"></task-type-btns>
      <library-type-btns
        v-model="libraryType"
        :cols="2"
        :md="2"
        :sm="2"
        :xs="2"
      ></library-type-btns>
      <scenario-list-btns
        v-model="scenarioList"
        :cols="2"
        :md="2"
        :sm="2"
        :xs="2"
        class="bg-transparent !text-base"
      />
      <slot name="append" />
    </div>

    <div class="p-4 pt-0 border-t-1 border-gray-300">
      <template v-if="isHeterogeneous">
        <div class="mt-3 mb-5 w-full text-h6 transition-all truncate">
          <v-icon class="mr-3" icon="mdi-vector-difference" color="black" size="small"></v-icon>
          {{ t("Search.UploadHeterogeneousRequirement") }}
        </div>

        <v-dialog v-model="heterDialog" width="1024">
          <template v-slot:activator="{ props }">
            <v-card v-bind="props" flat class="border-gray-500 bg-transparent">
              <v-btn block variant="outlined">
                {{ t("Search.StartHeterogeneousSearch") }}
              </v-btn>
            </v-card>
          </template>

          <v-card class="p-4 md:p-8 md:pt-4">
            <div>
              <v-tabs v-model="heterTab" align-tabs="center">
                <v-tab value="dataType">{{
                  t("Submit.SemanticSpecification.DataType.DescriptionInput.Name")
                }}</v-tab>
                <v-tab value="taskType">{{
                  t("Submit.SemanticSpecification.TaskType.DescriptionOutput.Name")
                }}</v-tab>
              </v-tabs>
            </div>

            <v-window v-model="heterTab">
              <v-window-item value="dataType">
                <div class="flex justify-between">
                  <div class="text-h4 font-semibold">
                    {{ t("Submit.SemanticSpecification.DataType.DescriptionInput.Name") }}
                  </div>
                  <v-btn
                    icon="mdi-download"
                    variant="flat"
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
                >
                </description-input>
              </v-window-item>

              <v-window-item value="taskType">
                <div class="flex justify-between">
                  <div class="mt-4 text-h4 font-semibold">
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
                >
                </description-input>
              </v-window-item>
            </v-window>

            <div class="flex justify-end mt-4">
              <v-btn color="primary" rounded variant="flat" @click="heterDialog = false">
                {{ t("Public.Finish") }}
              </v-btn>
            </div>
          </v-card>
        </v-dialog>
      </template>

      <div class="mt-3 mb-5 w-full text-h6 transition-all truncate">
        <v-icon class="mr-3" icon="mdi-upload" color="black" size="small"></v-icon>
        {{ t("Search.UploadStatisticalRequirement") }}
      </div>

      <file-upload
        v-model="files"
        :height="28"
        :tips="t('Submit.File.DragFileHere', { file: 'json' })"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.filter {
  @apply p-2 w-full md:h-full md:overflow-y-auto sm:px-5;

  * {
    @apply mt-2;
  }
}
</style>
