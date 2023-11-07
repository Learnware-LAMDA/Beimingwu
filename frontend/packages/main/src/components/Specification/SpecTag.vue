<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import DataTypeBtns from "../Specification/SpecTag/DataType.vue";
import TaskTypeBtns from "../Specification/SpecTag/TaskType.vue";
import LibraryTypeBtns from "../Specification/SpecTag/LibraryType.vue";
import ScenarioListBtns from "../Specification/SpecTag/ScenarioList.vue";
import DescriptionInput from "./DescriptionInput.vue";
import type {
  DataType,
  TaskType,
  LibraryType,
  ScenarioList,
} from "@beiming-system/types/learnware";

export interface Props {
  dataType: DataType | "";
  taskType: TaskType | "";
  libraryType: LibraryType | "";
  scenarioList: ScenarioList;
  dataTypeDescription: string;
  taskTypeDescription: string;
  errorMessages?: string;
}

const { t } = useI18n();

const emits = defineEmits([
  "update:dataType",
  "update:taskType",
  "update:libraryType",
  "update:scenarioList",
  "update:dataTypeDescription",
  "update:taskTypeDescription",
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
const dataTypeDescription = computed({
  get: () => JSON.parse(props.dataTypeDescription),
  set: (val) => emits("update:dataTypeDescription", JSON.stringify(val)),
});
const taskTypeDescription = computed({
  get: () => JSON.parse(props.taskTypeDescription),
  set: (val) => emits("update:taskTypeDescription", JSON.stringify(val)),
});
</script>

<template>
  <div class="spec-tag">
    <v-scroll-y-transition class="fixed left-0 right-0 z-index-10" style="top: var(--v-layout-top)">
      <v-card-actions v-if="errorMessages">
        <v-alert class="w-full max-w-[900px] mx-auto" closable :text="errorMessages" type="error" />
      </v-card-actions>
    </v-scroll-y-transition>
    <data-type-btns v-model="dataType" />
    <description-input
      v-if="dataType === 'Table'"
      v-model="dataTypeDescription"
      :name="t('Submit.SemanticSpecification.DataType.DescriptionInput.Name')"
    >
      <template #msg>
        {{ t("Submit.SemanticSpecification.DataType.DescriptionInput.FeatureTips") }}
      </template>
      <template #msg-small>
        {{ t("Submit.SemanticSpecification.DataType.DescriptionInput.FeatureTipsSmall") }}
      </template>
    </description-input>
    <task-type-btns v-model="taskType" />
    <description-input
      v-if="
        taskType === 'Classification' ||
        taskType === 'Regression' ||
        taskType === 'Feature Extraction'
      "
      v-model="taskTypeDescription"
      :name="t('Submit.SemanticSpecification.TaskType.DescriptionOutput.Name')"
    >
      <template #msg>
        {{ t("Submit.SemanticSpecification.TaskType.DescriptionOutput.LabelTips") }}
      </template>
      <template #msg-small>
        {{ t("Submit.SemanticSpecification.TaskType.DescriptionOutput.LabelTipsSmall") }}
      </template>
    </description-input>
    <library-type-btns v-model="libraryType" />
    <scenario-list-btns v-model="scenarioList" />
  </div>
</template>
