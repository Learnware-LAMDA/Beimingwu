<script setup>
import { ref, computed, watch } from 'vue'
import DataType from '@/views/Submit/SemanticSpec/DataType.vue'
import TaskType from '@/views/Submit/SemanticSpec/TaskType.vue'
import HardwareType from '@/views/Submit/SemanticSpec/HardwareType.vue'
import FileUpload from '@/views/Submit/FileUpload.vue'
import LearnwareList from './LearnwareList.vue'

const dataType = ref('')
const taskType = ref('')
const hardwareType = ref('')
const files = ref([])

const learnwareItems = Array(100).fill(0).map((_, i) => {
  const allDataType = ['Audio', 'Video', 'Text', 'Image', 'Table']
  const allTaskType = ['Classification', 'Clustering', 'Detection', 'Extraction', 'Generation', 'Regression', 'Segmentation', 'Ranking']
  const allRequirementType = ['CPU', 'GPU']

  return {
    title: `Learnware ${i + 1}`,
    description: `This is the description of learnware ${i + 1}`,
    dataType: allDataType[Math.floor(Math.random() * allDataType.length)],
    taskType: allTaskType[Math.floor(Math.random() * allTaskType.length)],
    requirementType: allRequirementType[Math.floor(Math.random() * allRequirementType.length)],
  }
})

const filters = computed(() => ({
  dataType: dataType.value,
  taskType: taskType.value,
  hardwareType: hardwareType.value,
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
    if (filters.value.hardwareType && filters.value.hardwareType !== item.requirementType) {
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
      <div class="h-40">
        Upload statistical specification
        <file-upload />
      </div>
    </div>
    <div class="content">
      <learnware-list :items="filteredLearnwareItems" />
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