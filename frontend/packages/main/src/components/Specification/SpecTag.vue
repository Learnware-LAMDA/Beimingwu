<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import DataTypeBtns from "../Specification/SpecTag/DataType.vue";
import TaskTypeBtns from "../Specification/SpecTag/TaskType.vue";
import LibraryTypeBtns from "../Specification/SpecTag/LibraryType.vue";
import ScenarioListBtns from "../Specification/SpecTag/ScenarioList.vue";
import LicenseTypeBtns from "../Specification/SpecTag/LicenseType.vue";
import DescriptionInput from "./DescriptionInput.vue";
import type {
  DataType,
  TaskType,
  LibraryType,
  ScenarioList,
  LicenseList,
} from "@beiming-system/types/learnware";

export interface Props {
  dataType: DataType | "";
  taskType: TaskType | "";
  libraryType: LibraryType | "";
  scenarioList: ScenarioList;
  licenseList: LicenseList;
  inputDescription: string;
  outputDescriptionClassification: string;
  outputDescriptionRegression: string;
  errorMessages?: string;
}

const { t } = useI18n();

const emits = defineEmits([
  "update:dataType",
  "update:taskType",
  "update:libraryType",
  "update:scenarioList",
  "update:licenseList",
  "update:inputDescription",
  "update:outputDescriptionClassification",
  "update:outputDescriptionRegression",
]);

const props = withDefaults(defineProps<Props>(), {
  errorMessages: "",
});

const dataType = computed({
  get: () => props.dataType,
  set: (val) => emits("update:dataType", val),
});
const taskType = computed({
  get: () => props.taskType,
  set: (val) => emits("update:taskType", val),
});
const libraryType = computed({
  get: () => props.libraryType,
  set: (val) => emits("update:libraryType", val),
});
const scenarioList = computed({
  get: () => props.scenarioList,
  set: (val) => emits("update:scenarioList", val),
});
const licenseList = computed({
  get: () => props.licenseList,
  set: (val) => emits("update:licenseList", val),
});
const inputDescription = computed({
  get: () => JSON.parse(props.inputDescription),
  set: (val) => emits("update:inputDescription", JSON.stringify(val)),
});
const outputDescriptionClassification = computed({
  get: () => JSON.parse(props.outputDescriptionClassification),
  set: (val) => emits("update:outputDescriptionClassification", JSON.stringify(val)),
});
const outputDescriptionRegression = computed({
  get: () => JSON.parse(props.outputDescriptionRegression),
  set: (val) => emits("update:outputDescriptionRegression", JSON.stringify(val)),
});
</script>

<template>
  <div class="spec-tag">
    <v-scroll-y-transition
      class="fixed left-0 right-0 z-10"
      style="top: var(--v-layout-top)"
    >
      <v-card-actions v-if="errorMessages">
        <v-alert
          class="mx-auto w-full max-w-[900px]"
          closable
          :text="errorMessages"
          type="error"
        />
      </v-card-actions>
    </v-scroll-y-transition>
    <data-type-btns
      v-model="dataType"
      :cols="4"
    />

    <template v-if="dataType === 'Table'">
      <v-alert
        class="mt-3 text-xs sm:text-sm"
        type="info"
        color="primary"
        closable
      >
        <span class="hidden sm:inline">{{
          t("Submit.SemanticSpecification.DataType.DescriptionInput.InputTips")
        }}</span>
        <span class="sm:hidden">{{
          t("Submit.SemanticSpecification.DataType.DescriptionInput.InputTipsSmall")
        }}</span>
      </v-alert>
      <description-input
        v-model="inputDescription"
        :name="t('Submit.SemanticSpecification.DataType.DescriptionInput.Name')"
        class="mt-3"
      />
    </template>

    <task-type-btns
      v-model="taskType"
      :cols="4"
    />

    <template v-if="taskType === 'Classification'">
      <v-alert
        class="mt-3 text-xs sm:text-sm"
        type="info"
        color="primary"
        closable
      >
        <span class="hidden sm:inline">{{
          t("Submit.SemanticSpecification.TaskType.DescriptionOutput.OutputTipsClassification")
        }}</span>
        <span class="sm:hidden">{{
          t("Submit.SemanticSpecification.TaskType.DescriptionOutput.OutputTipsSmallClassification")
        }}</span>
      </v-alert>
      <description-input
        v-model="outputDescriptionClassification"
        :name="t('Submit.SemanticSpecification.TaskType.DescriptionOutput.Name')"
        class="mt-3"
      />
    </template>

    <template v-if="taskType === 'Regression'">
      <v-alert
        class="mt-3 text-xs sm:text-sm"
        type="info"
        color="primary"
        closable
      >
        <span class="hidden sm:inline">{{
          t("Submit.SemanticSpecification.TaskType.DescriptionOutput.OutputTipsRegression")
        }}</span>
        <span class="sm:hidden">{{
          t("Submit.SemanticSpecification.TaskType.DescriptionOutput.OutputTipsSmallRegression")
        }}</span>
      </v-alert>
      <description-input
        v-model="outputDescriptionRegression"
        :name="t('Submit.SemanticSpecification.TaskType.DescriptionOutput.Name')"
        class="mt-3"
      />
    </template>

    <library-type-btns v-model="libraryType" />
    <scenario-list-btns v-model="scenarioList" />
    <license-type-btns
      v-model="licenseList"
      :single="true"
    />
  </div>
</template>
