<script setup>
import { ref, computed, onMounted, nextTick, onActivated } from 'vue'
import DataType from '@/components/Specification/SpecTag/DataType.vue'
import TaskType from '@/components/Specification/SpecTag/TaskType.vue'
import HardwareType from '@/components/Specification/SpecTag/HardwareType.vue'
import FileUpload from '@/components/Specification/FileUpload.vue'
import TagList from '@/components/Specification/SpecTag/TagList.vue'
import LearnwareList from '@/components/Learnware/LearnwareList.vue'

const search = ref('')
const dataType = ref('')
const taskType = ref('')
const hardwareType = ref('')
const tagList = ref([])
const files = ref([])

const contentRef = ref(null)
const learnwareItems = ref([])

const scrollTop = ref(0)

const showRecommended = computed(() => files.value.length > 0)
const recommendedTips = ref(true)
const unrecommendedTips = ref(true)

function generateLearnwareItems() {
  return Array(100).fill(0).map((_, i) => {
    const allDataType = ['Audio', 'Video', 'Text', 'Image', 'Table']
    const allTaskType = ['Classification', 'Clustering', 'Detection', 'Extraction', 'Generation', 'Regression', 'Segmentation', 'Ranking']
    const allHardwareType = ['CPU', 'GPU']
    const allTagList = ['Business', 'Financial', 'Health', 'Politics', 'Computer', 'Internet', 'Traffic', 'Nature', 'Fashion', 'Industry', 'Agriculture', 'Education']

    return {
      id: Array(32).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
      name: `Learnware ${i + 1}`,
      description: `This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. `,
      dataType: allDataType[Math.floor(Math.random() * allDataType.length)],
      taskType: allTaskType[Math.floor(Math.random() * allTaskType.length)],
      hardwareType: allHardwareType[Math.floor(Math.random() * allHardwareType.length)],
      tagList: Array.from(new Set(Array(Math.ceil(Math.random() * 5)).fill(0).map(() => allTagList[Math.floor(Math.random() * allTagList.length)]))),
      matchScore: Math.floor(Math.random() * 100),
    }
  }).sort((a, b) => b.matchScore - a.matchScore)
}

const filters = computed(() => ({
  name: search.value,
  dataType: dataType.value,
  taskType: taskType.value,
  hardwareType: hardwareType.value,
  tagList: tagList.value,
  files: files.value
}))

const filteredLearnwareItems = computed(() => {
  return learnwareItems.value.filter((item) => {
    if (filters.value.name && !item.name.includes(filters.value.name)) {
      return false
    }
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

const recommendLearnwareItems = ref(Array(4).fill(0).map((_, i) => {
  const allDataType = ['Audio', 'Video', 'Text', 'Image', 'Table']
  const allTaskType = ['Classification', 'Clustering', 'Detection', 'Extraction', 'Generation', 'Regression', 'Segmentation', 'Ranking']
  const allHardwareType = ['CPU', 'GPU']
  const allTagList = ['Business', 'Financial', 'Health', 'Politics', 'Computer', 'Internet', 'Traffic', 'Nature', 'Fashion', 'Industry', 'Agriculture', 'Education']

  return {
    id: Array(32).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
    name: `Learnware ${i + 1}`,
    description: `This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. `,
    dataType: allDataType[Math.floor(Math.random() * allDataType.length)],
    taskType: allTaskType[Math.floor(Math.random() * allTaskType.length)],
    hardwareType: allHardwareType[Math.floor(Math.random() * allHardwareType.length)],
    tagList: Array.from(new Set(Array(Math.ceil(Math.random() * 5)).fill(0).map(() => allTagList[Math.floor(Math.random() * allTagList.length)]))),
    matchScore: Math.floor(Math.random() * 100),
  }
}).sort((a, b) => b.matchScore - a.matchScore))

onActivated(() => {
  contentRef.value.scrollTop = scrollTop.value
})

onMounted(() => {
  learnwareItems.value = generateLearnwareItems()
  nextTick(() => {
    contentRef.value.addEventListener('scroll', () => {
      scrollTop.value = contentRef.value.scrollTop
    })
  })
})
</script>

<template>
  <div class="search-container">
    <div class="flex flex-col w-1/1 md:max-w-460px">
      <div class="filter px-5">
        <div class="my-3 text-h6">Choose semantic specification</div>
        <div>
          <div class="mt-7 mb-3 text-h6 !text-1rem">Search by name</div>
          <v-text-field v-model="search" label="Search by name" hide-details append-inner-icon="mdi-close" @click:append-inner="search = ''" />
        </div>
        <data-type :cols="3" :md="2" :sm="2" :xs="2" v-model:value="dataType" />
        <task-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="taskType" />
        <hardware-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="hardwareType" />
        <tag-list class="bg-transparent text-h6 !text-1rem" v-model:value="tagList" :cols="2" :md="1" :sm="1" />
      </div>
      <div class="p-5 pt-0">
        <div class="mt-3 mb-5 text-h6 text-sm">
          Upload statistical specification
        </div>
        <file-upload v-model:files="files" />
      </div>
    </div>
    <div ref="contentRef" class="content">
      <v-card v-if="showRecommended" flat class="m-2 mt-4 bg-transparent">
        <v-card-title v-if="!recommendedTips">Recommended multiple learnwares</v-card-title>
        <v-card-text v-if="recommendedTips" class="!p-2">
          <v-alert v-model="recommendedTips" title="Recommended multiple learnwares"
            text="The learnwares listed below are highly recommended as they have the highest statistical specification similarity to your tasks. Combining these learnwares can lead to great effectiveness." closable color="success">
            <template #prepend>
              <v-icon icon="mdi-hexagon-multiple" size="x-large"></v-icon>
            </template>
          </v-alert>
        </v-card-text>
        <learnware-list :items="recommendLearnwareItems" />
      </v-card>
      <v-card flat class="m-2 mt-4 bg-transparent">
        <v-card-title v-if="showRecommended && !unrecommendedTips">Recommended single learnwares</v-card-title>
        <v-card-text v-if="showRecommended && unrecommendedTips" class="!p-2">
          <v-alert v-model="unrecommendedTips" title="Recommended single learnware"
            text="The listed learnwares are not highly recommended as they may not precisely match your task requirements in terms of statistical specifications. However, they are still available for your use." closable color="info">
            <template #prepend>
              <v-icon icon="mdi-hexagon" size="x-large"></v-icon>
            </template>
          </v-alert>
        </v-card-text>
        <learnware-list :items="filteredLearnwareItems" :filters="filters" />
      </v-card>
    </div>
  </div>
</template>

<style scoped lang="scss">
.search-container {
  @apply md: (fixed flex) mx-auto w-1/1;
  height: calc(100% - var(--v-layout-top));

  .filter {
    @apply p-2 w-1/1 md: (h-1/1 overflow-y-scroll);

    * {
      @apply mt-2;
    }
  }

  .filter.hide {
    @apply h-0;
  }

  .content {
    @apply w-1/1 overflow-y-scroll;
  }
}
</style>