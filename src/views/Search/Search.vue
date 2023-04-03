<script setup>
import { ref, computed, watch } from 'vue'
import DataType from '@/views/Submit/SemanticSpec/DataType.vue'
import TaskType from '@/views/Submit/SemanticSpec/TaskType.vue'
import HardwareType from '@/views/Submit/SemanticSpec/HardwareType.vue'
import FileUpload from '@/views/Submit/FileUpload.vue'
import TagList from '@/views/Submit/SemanticSpec/TagList.vue'
import LearnwareList from './LearnwareList.vue'

const dataType = ref('')
const taskType = ref('')
const hardwareType = ref('')
const tagList = ref([])
const files = ref([])

const learnwareItems = Array(100).fill(0).map((_, i) => {
  const allDataType = ['Audio', 'Video', 'Text', 'Image', 'Table']
  const allTaskType = ['Classification', 'Clustering', 'Detection', 'Extraction', 'Generation', 'Regression', 'Segmentation', 'Ranking']
  const allHardwareType = ['CPU', 'GPU']
  const allTagList = ['Business', 'Financial', 'Health', 'Politics', 'Computer', 'Internet', 'Traffic', 'Nature', 'Fashion', 'Industry', 'Agriculture', 'Education']

  return {
    id: Array(32).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
    name: `Learnware ${i + 1}`,
    description: `This is the description of learnware ${i + 1}`,
    dataType: allDataType[Math.floor(Math.random() * allDataType.length)],
    taskType: allTaskType[Math.floor(Math.random() * allTaskType.length)],
    hardwareType: allHardwareType[Math.floor(Math.random() * allHardwareType.length)],
    tagList: Array.from(new Set(Array(Math.ceil(Math.random() * 5)).fill(0).map(() => allTagList[Math.floor(Math.random() * allTagList.length)]))),
  }
})

const filters = computed(() => ({
  dataType: dataType.value,
  taskType: taskType.value,
  hardwareType: hardwareType.value,
  tagList: tagList.value,
  files: files.value
}))

const filteredLearnwareItems = computed(() => {
  return learnwareItems.filter((item) => {
    if (filters.value.dataType && filters.value.dataType !== item.dataType) {
      return false
    }
    if (filters.value.taskType && filters.value.taskType !== item.taskType) {
      return false
    }
    if (filters.value.hardwareType && filters.value.hardwareType !== item.hardwareType) {
      return false
    }
    if (filters.value.tagList.length > 0 && filters.value.tagList.filter((tag) => item.tagList.includes(tag)).length === 0) {
      return false
    }
    return true
  })
})

watch(
  () => filters.value,
  (newVal) => {
    console.log(newVal)
  }
)
</script>

<template>
  <div class="search-container">
    <div class="filter">
      <data-type :cols="3" :md="2" :sm="2" :xs="2" v-model:value="dataType" />
      <task-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="taskType" />
      <hardware-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="hardwareType" />
      <tag-list class="bg-transparent" v-model:value="tagList" :cols="2" :md="1" :sm="1" />
      <div>
        Upload statistical specification
        <file-upload />
      </div>
    </div>
    <div class="content">
      <learnware-list :items="filteredLearnwareItems" :filters="filters" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.search-container {
  @apply md: (fixed flex) mx-auto w-1/1;
  height: calc(100% - var(--v-layout-top));

  .filter {
    @apply p-2 w-1/1 md: (h-1/1 w-150 overflow-y-scroll);

    * {
      @apply mt-2;
    }
  }

  .filter.hide {
    @apply h-0;
  }

  .content {
    @apply w-1/1 md: h-1/1 overflow-y-scroll;
  }
}
</style>