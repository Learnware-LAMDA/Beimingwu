<script setup>
import { computed } from "vue";
import DataTypeBtns from "../Specification/SpecTag/DataType.vue";
import TaskTypeBtns from "../Specification/SpecTag/TaskType.vue";
import LibraryTypeBtns from "../Specification/SpecTag/LibraryType.vue";
import TagListBtns from "../Specification/SpecTag/TagList.vue";

const dataTypeDescriptionExample = `
{
  "Dimension": 10,
  "Description": {
    "0": "gender",
    "1": "age",
    "2": "f2",
    "5": "f5",
    ...
  }
}
`;
const taskTypeDescriptionExample = `
{
  "Dimension": 3,
  "Description": {
    "0": "the probability of being a cat",
    "1": "the probability of being a dog",
    "2": "the probability of being a bird"
  }
}
`;

const emits = defineEmits([
  "update:dataType",
  "update:taskType",
  "update:libraryType",
  "update:tagList",
  "update:dataTypeDescription",
  "update:taskTypeDescription",
]);

const props = defineProps({
  dataType: {
    type: String,
    required: true,
  },
  taskType: {
    type: String,
    required: true,
  },
  libraryType: {
    type: String,
    required: true,
  },
  tagList: {
    type: Array,
    required: true,
  },
  dataTypeDescription: {
    type: String,
    required: false,
    default: null,
  },
  taskTypeDescription: {
    type: String,
    required: false,
    default: null,
  },
  errorMessages: {
    type: String,
    required: false,
    default: null,
  },
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
const tagList = computed({
  get: () => props.tagList,
  set: (val) => emits("update:tagList", val),
});
const dataTypeDescription = computed({
  get: () => props.dataTypeDescription,
  set: (val) => emits("update:dataTypeDescription", val),
});
const taskTypeDescription = computed({
  get: () => props.taskTypeDescription,
  set: (val) => emits("update:taskTypeDescription", val),
});

emits("update:dataTypeDescription", dataTypeDescriptionExample);
emits("update:taskTypeDescription", taskTypeDescriptionExample);
</script>

<template>
  <div class="spec-tag">
    <v-scroll-y-transition class="fixed left-0 right-0 z-index-10" style="top: var(--v-layout-top)">
      <v-card-actions v-if="errorMessages">
        <v-alert class="w-1/1 max-w-900px mx-auto" closable :text="errorMessages" type="error" />
      </v-card-actions>
    </v-scroll-y-transition>
    <data-type-btns v-model:value="dataType" />
    <v-container v-if="dataType === 'Table'">
      <v-row>
        <v-col cols="12" md="6">
          <v-textarea v-model="dataTypeDescription" label="Table Description" rows="12">
          </v-textarea>
        </v-col>
        <v-col cols="12" md="6">
          Example:
          <pre>{{ dataTypeDescriptionExample }}</pre>
        </v-col>
      </v-row>
    </v-container>
    <task-type-btns v-model:value="taskType" />
    <v-container
      v-if="
        taskType === 'Classification' ||
        taskType === 'Regression' ||
        taskType === 'Feature Extraction'
      "
    >
      <v-row>
        <v-col cols="12" md="6">
          <v-textarea v-model="taskTypeDescription" label="Task Output Description" rows="12">
          </v-textarea>
        </v-col>
        <v-col cols="12" md="6">
          Example:
          <pre>{{ taskTypeDescriptionExample }}</pre>
        </v-col>
      </v-row>
    </v-container>
    <library-type-btns v-model:value="libraryType" />
    <tag-list-btns v-model:value="tagList" />
  </div>
</template>
