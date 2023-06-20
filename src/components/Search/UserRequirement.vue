<script setup>
import { ref, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import DataType from '@/components/Specification/SpecTag/DataType.vue';
import TaskType from '@/components/Specification/SpecTag/TaskType.vue';
import LibraryType from '@/components/Specification/SpecTag/LibraryType.vue';
import FileUpload from '@/components/Specification/FileUpload.vue';
import TagList from '@/components/Specification/SpecTag/TagList.vue';

const emits = defineEmits(['update:value']);

const props = defineProps({
  value: {
    type: Object,
    default: () => ({}),
  },
});

const route = useRoute();

const search = ref(route.query.search || '');
const dataType = ref(route.query.dataType || '');
const taskType = ref(route.query.taskType || '');
const libraryType = ref(route.query.libraryType || '');
let _tagList;
try {
  _taglist = JSON.parse(route.query.tagList);
} catch {
  _tagList = [];
}
const tagList = ref(_tagList);

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
    emits('update:value', requirement.value);
  },
);
</script>

<template>
  <div class="flex flex-col w-1/1 md:max-w-460px sm:border-r-1">
    <div class="filter">
      <div class="my-3 text-h6">
        <v-icon class="!mt-0 mr-3" icon="mdi-tag-text" color="black" size="small" />Choose semantic requirement
      </div>

      <div>
        <div class="mt-7 mb-3 text-h6 !text-1rem">Search by name</div>
        <v-text-field v-model="search" label="Learnware name" hide-details append-inner-icon="mdi-close"
          @click:append-inner="search = ''" />
      </div>

      <data-type :cols="3" :md="2" :sm="2" :xs="2" v-model:value="dataType" />
      <task-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="taskType" />
      <library-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="libraryType" />
      <tag-list class="bg-transparent !text-1rem" v-model:value="tagList" :cols="2" :md="2" :sm="2" :xs="2" />
    </div>

    <div class="p-5 pt-0 border-t-1 border-gray-300">
      <div ref="anchorRef" class="mt-3 mb-5 w-1/1 text-h6 transition-all truncate">
        <v-icon class="mr-3" icon="mdi-upload" color="black" size="small" />Upload statistical requirement
      </div>

      <file-upload v-model:files="files" :height="28" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.filter {
  @apply p-2 w-1/1 md: (h-1/1 overflow-y-scroll) sm:px-5;

  * {
    @apply mt-2;
  }
}
</style>
