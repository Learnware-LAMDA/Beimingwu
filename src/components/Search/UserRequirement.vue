<script setup>
import { ref, computed, watch } from "vue";
import { useRoute } from "vue-router";
import DataTypeBtns from "../Specification/SpecTag/DataType.vue";
import TaskTypeBtns from "../Specification/SpecTag/TaskType.vue";
import LibraryTypeBtns from "../Specification/SpecTag/LibraryType.vue";
import FileUpload from "../Specification/FileUpload.vue";
import TagListBtns from "../Specification/SpecTag/TagList.vue";

const emits = defineEmits(["update:value"]);

defineProps({
  value: {
    type: Object,
    default: () => ({}),
  },
});

const route = useRoute();

const search = ref(route.query.search || "");
const dataType = ref(route.query.dataType || "");
const taskType = ref(route.query.taskType || "");
const libraryType = ref(route.query.libraryType || "");
let tryTagList;
try {
  tryTagList = JSON.parse(route.query.tagList);
} catch {
  tryTagList = [];
}
const tagList = ref(tryTagList);

const files = ref([]);

const requirement = computed(() => ({
  name: search.value,
  dataType: dataType.value,
  taskType: taskType.value,
  libraryType: libraryType.value,
  tagList: tagList.value,
  files: files.value,
}));

watch(
  () => requirement.value,
  () => {
    emits("update:value", requirement.value);
  },
);
</script>

<template>
  <div class="flex flex-col w-1/1 md:max-w-460px sm:border-r-1">
    <div class="filter">
      <div class="my-3 text-h6">
        <v-icon class="!mt-0 mr-3" icon="mdi-tag-text" color="black" size="small"></v-icon>
        Choose semantic requirement
      </div>

      <div>
        <div class="mt-7 mb-3 text-h6 !text-1rem">Search by name</div>
        <v-text-field
          v-model="search"
          label="Learnware name"
          hide-details
          append-inner-icon="mdi-close"
          @click:append-inner="search = ''"
        ></v-text-field>
      </div>

      <data-type-btns v-model:value="dataType" :cols="3" :md="2" :sm="2" :xs="2"></data-type-btns>
      <task-type-btns v-model:value="taskType" :cols="2" :md="2" :sm="2" :xs="2"></task-type-btns>
      <library-type-btns
        v-model:value="libraryType"
        :cols="2"
        :md="2"
        :sm="2"
        :xs="2"
      ></library-type-btns>
      <tag-list-btns
        v-model:value="tagList"
        :cols="2"
        :md="2"
        :sm="2"
        :xs="2"
        class="bg-transparent !text-1rem"
      ></tag-list-btns>
    </div>

    <div class="p-5 pt-0 border-t-1 border-gray-300">
      <div ref="anchorRef" class="mt-3 mb-5 w-1/1 text-h6 transition-all truncate">
        <v-icon class="mr-3" icon="mdi-upload" color="black" size="small"></v-icon>
        Upload statistical requirement
      </div>

      <file-upload v-model:files="files" :height="28"></file-upload>
    </div>
  </div>
</template>

<style scoped lang="scss">
.filter {
  @apply p-2 w-1/1 md:(h-1/1 overflow-y-scroll) sm:px-5;

  * {
    @apply mt-2;
  }
}
</style>
