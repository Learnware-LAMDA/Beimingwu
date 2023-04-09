<script setup>
import { ref, computed, watch, onMounted, nextTick, onActivated } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import DataType from '@/components/Specification/SpecTag/DataType.vue'
import TaskType from '@/components/Specification/SpecTag/TaskType.vue'
import HardwareType from '@/components/Specification/SpecTag/HardwareType.vue'
import FileUpload from '@/components/Specification/FileUpload.vue'
import TagList from '@/components/Specification/SpecTag/TagList.vue'
import LearnwareList from '@/components/Learnware/LearnwareList.vue'
import PageLearnwareList from '@/components/Learnware/PageLearnwareList.vue'

const route = useRoute()
const router = useRouter()

const search = ref(route.query.search || '')
const dataType = ref(route.query.dataType || '')
const taskType = ref(route.query.taskType || '')
const hardwareType = ref(route.query.hardwareType || '')
let _tagList
try {
  _taglist = JSON.parse(route.query.tagList)
}
catch {
  _tagList = []
}
const tagList = ref(_tagList)

const files = ref([])

const page = ref(1)
const pageNum = ref(10)
const pageSize = ref(10)
const loading = ref(false)

const pageLearnwareListRef = ref(null)
const contentRef = ref(null)

const scrollTop = ref(0)

const showMultiRecommended = computed(() => {
  return files.value.length > 0 && (!pageLearnwareListRef.value || pageLearnwareListRef.value.getPage() === 1)
})
const multiRecommendedTips = ref(true)
const singleRecommendedTips = ref(true)

const filters = computed(() => ({
  name: search.value,
  dataType: dataType.value,
  taskType: taskType.value,
  hardwareType: hardwareType.value,
  tagList: tagList.value,
  files: files.value
}))

const multiRecommendedLearnwareItems = ref([])

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

function loadQuery() {
  if (route.query.search) {
    search.value = route.query.search
  }
  if (route.query.dataType) {
    dataType.value = route.query.dataType
  }
  if (route.query.taskType) {
    taskType.value = route.query.taskType
  }
  if (route.query.hardwareType) {
    hardwareType.value = route.query.hardwareType
  }
  if (route.query.tagList) {
    tagList.value = JSON.parse(route.query.tagList)
  }
}

function saveQuery() {
  router.replace({
    query: {
      search: search.value,
      dataType: dataType.value,
      taskType: taskType.value,
      hardwareType: hardwareType.value,
      tagList: JSON.stringify(tagList.value),
    }
  })
}

function pageChange(newPage) {
  page.value = newPage
  contentRef.value.scrollTop = 0
}

function delay(ms) {
  return new Promise((res) => {
    setTimeout(res, ms)
  })
}

function generateLearnwareItems(filters, num) {
  return Array(num).fill(0).map((_, i) => {
    const allDataType = ['Audio', 'Video', 'Text', 'Image', 'Table']
    const allTaskType = ['Classification', 'Clustering', 'Detection', 'Extraction', 'Generation', 'Regression', 'Segmentation', 'Ranking']
    const allHardwareType = ['CPU', 'GPU']
    const allTagList = ['Business', 'Financial', 'Health', 'Politics', 'Computer', 'Internet', 'Traffic', 'Nature', 'Fashion', 'Industry', 'Agriculture', 'Education']

    return {
      id: Array(32).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
      name: `Learnware ${i + 1}`,
      description: `This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. `,
      dataType: filters.dataType || allDataType[Math.floor(Math.random() * allDataType.length)],
      taskType: filters.taskType || allTaskType[Math.floor(Math.random() * allTaskType.length)],
      hardwareType: filters.hardwareType || allHardwareType[Math.floor(Math.random() * allHardwareType.length)],
      tagList: filters.tagList || Array.from(new Set(Array(Math.ceil(Math.random() * 5)).fill(0).map(() => allTagList[Math.floor(Math.random() * allTagList.length)]))),
      matchScore: Math.floor(Math.random() * 100),
    }
  }).sort((a, b) => b.matchScore - a.matchScore)
}

function fetchByFilterAndPage(filters, page) {
  delay(1000)
    .then(() => {
      multiRecommendedLearnwareItems.value = generateLearnwareItems(filters, pageSize.value)
      loading.value = false
    })
}

watch(
  () => [filters.value, page.value],
  (newVal) => {
    const [newFilters, newPage] = newVal

    if (contentRef.value) {
      contentRef.value.scrollTop = 0
    }

    saveQuery()

    loading.value = true
    fetchByFilterAndPage(newFilters, newPage)
  },
  { deep: true }
)


onActivated(() => {
  contentRef.value.scrollTop = scrollTop.value
})

onMounted(() => {
  nextTick(() => {
    contentRef.value.addEventListener('scroll', () => {
      scrollTop.value = contentRef.value.scrollTop
    })

    loadQuery()
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
          <v-text-field v-model="search" label="Search by name" hide-details append-inner-icon="mdi-close"
            @click:append-inner="search = ''" />
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
      <v-card v-if="showMultiRecommended" flat class="m-2 mt-4 bg-transparent">
        <v-card-title v-if="!multiRecommendedTips">Recommended multiple learnwares</v-card-title>
        <v-card-text v-if="multiRecommendedTips" class="!p-2">
          <v-alert v-model="multiRecommendedTips" title="Recommended multiple learnwares"
            text="The learnwares listed below are highly recommended as they have the highest statistical specification similarity to your tasks. Combining these learnwares can lead to great effectiveness."
            closable color="success">
            <template #prepend>
              <v-icon icon="mdi-hexagon-multiple" size="x-large"></v-icon>
            </template>
          </v-alert>
        </v-card-text>
        <learnware-list :items="recommendLearnwareItems" :filters="filters" />
      </v-card>
      <v-card flat class="m-2 mt-4 bg-transparent">
        <v-card-title v-if="showMultiRecommended && !singleRecommendedTips">Recommended single learnwares</v-card-title>
        <v-card-text v-if="showMultiRecommended && singleRecommendedTips" class="!p-2">
          <v-alert v-model="singleRecommendedTips" title="Recommended single learnware"
            text="The listed learnwares are not highly recommended as they may not precisely match your task requirements in terms of statistical specifications. However, they are still available for your use."
            closable color="info">
            <template #prepend>
              <v-icon icon="mdi-hexagon" size="x-large"></v-icon>
            </template>
          </v-alert>
        </v-card-text>
        <page-learnware-list ref="pageLearnwareListRef" :items="multiRecommendedLearnwareItems" :filters="filters" @page-change="pageChange" :page="page" :page-num="pageNum" :page-size="pageSize" :loading="loading" />
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
}</style>