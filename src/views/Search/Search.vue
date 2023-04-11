<script setup>
import { ref, computed, watch, onMounted, nextTick, onActivated } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DataType from '@/components/Specification/SpecTag/DataType.vue'
import TaskType from '@/components/Specification/SpecTag/TaskType.vue'
import DeviceType from '@/components/Specification/SpecTag/DeviceType.vue'
import FileUpload from '@/components/Specification/FileUpload.vue'
import TagList from '@/components/Specification/SpecTag/TagList.vue'
import PageLearnwareList from '@/components/Learnware/PageLearnwareList.vue'

const route = useRoute()
const router = useRouter()

const search = ref(route.query.search || '')
const dataType = ref(route.query.dataType || '')
const taskType = ref(route.query.taskType || '')
const deviceType = ref(route.query.deviceType || '')
let _tagList
try {
  _taglist = JSON.parse(route.query.tagList)
}
catch {
  _tagList = []
}
const tagList = ref(_tagList)

const files = ref([])

const multiRecommendedLearnwarePage = ref(1)
const multiRecommendedLearnwarePageNum = ref(1)
const multiRecommendedLearnwarePageSize = ref(4)
const multiRecommendedLearnwareItems = ref([])
const singleRecommendedLearnwarePage = ref(1)
const singleRecommendedLearnwarePageNum = ref(10)
const singleRecommendedLearnwarePageSize = ref(10)
const singleRecommendedLearnwareItems = ref([])
const loading = ref(false)

const contentRef = ref(null)

const scrollTop = ref(0)

const showMultiRecommended = computed(() => {
  return files.value.length > 0 && (singleRecommendedLearnwarePage.value === 1)
})
const multiRecommendedTips = ref(true)
const singleRecommendedTips = ref(true)

const filters = computed(() => ({
  name: search.value,
  dataType: dataType.value,
  taskType: taskType.value,
  deviceType: deviceType.value,
  tagList: tagList.value,
  files: files.value
}))

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
  if (route.query.deviceType) {
    deviceType.value = route.query.deviceType
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
      deviceType: deviceType.value,
      tagList: JSON.stringify(tagList.value),
    }
  })
}

function pageChange(newPage) {
  singleRecommendedLearnwarePage.value = newPage
  contentRef.value && (contentRef.value.scrollTop = 0)
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
    const allDeviceType = ['CPU', 'GPU']
    const allTagList = ['Business', 'Financial', 'Health', 'Politics', 'Computer', 'Internet', 'Traffic', 'Nature', 'Fashion', 'Industry', 'Agriculture', 'Education']

    return {
      id: Array(32).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
      name: `Learnware ${i + 1}`,
      description: `This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. This is the description of learnware ${i + 1}. `,
      dataType: filters.dataType || allDataType[Math.floor(Math.random() * allDataType.length)],
      taskType: filters.taskType || allTaskType[Math.floor(Math.random() * allTaskType.length)],
      deviceType: filters.deviceType || allDeviceType[Math.floor(Math.random() * allDeviceType.length)],
      tagList: filters.tagList || Array.from(new Set(Array(Math.ceil(Math.random() * 5)).fill(0).map(() => allTagList[Math.floor(Math.random() * allTagList.length)]))),
      matchScore: files.value.length > 0 ? Math.floor(Math.random() * 100) : null,
    }
  }).sort((a, b) => b.matchScore - a.matchScore)
}

function fetchByFilterAndPage(filters, page) {
  console.log('fetching ...')
  loading.value = true
  delay(1000)
    .then(() => {
      multiRecommendedLearnwareItems.value = generateLearnwareItems(filters, multiRecommendedLearnwarePageSize.value)
      singleRecommendedLearnwareItems.value = generateLearnwareItems(filters, singleRecommendedLearnwarePageSize.value)
      loading.value = false
    })
}

watch(
  () => filters.value,
  () => singleRecommendedLearnwarePage.value = 1,
  { deep: true }
)

watch(
  () => [filters.value, singleRecommendedLearnwarePage.value],
  (newVal) => {
    const [newFilters, newPage] = newVal

    if (contentRef.value) {
      contentRef.value.scrollTop = 0
    }

    saveQuery()

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

    fetchByFilterAndPage(filters.value, singleRecommendedLearnwarePage.value)
  })
})
</script>

<template>
  <div class="search-container">
    <div class="flex flex-col w-1/1 md:max-w-460px bg-white">
      <div class="filter px-5">
        <div class="my-3 text-h6">
          <v-icon class="!mt-0 mr-3" icon="mdi-tag-text" color="black" size="small" />Choose semantic specification
        </div>
        <div>
          <div class="mt-7 mb-3 text-h6 !text-1rem">Search by name</div>
          <v-text-field v-model="search" label="Search by name" hide-details append-inner-icon="mdi-close"
            @click:append-inner="search = ''" />
        </div>
        <data-type :cols="3" :md="2" :sm="2" :xs="2" v-model:value="dataType" />
        <task-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="taskType" />
        <device-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="deviceType" />
        <tag-list class="bg-transparent text-h6 !text-1rem" v-model:value="tagList" :cols="2" :md="1" :sm="1" />
      </div>
      <v-hover>
        <template v-slot:default="{ isHovering, props }">
          <div class="p-5 pt-0 border-t-2 border-gray-300 bg-white" v-bind="props">
            <div class="mt-3 w-1/1 text-h6 transition-all" :class="files.length || isHovering ? ['mb-5'] : []">
              <v-icon class="mr-3" icon="mdi-upload" color="black" size="small" />Upload statistical specification
            </div>

            <v-expand-transition>
              <file-upload v-show="files.length || isHovering" v-model:files="files" />
            </v-expand-transition>
          </div>
        </template>
      </v-hover>
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
        <page-learnware-list :show-pagination="false" :items="multiRecommendedLearnwareItems" :filters="filters"
          @page-change="pageChange" :page="multiRecommendedLearnwarePage" :page-num="multiRecommendedLearnwarePageNum"
          :page-size="multiRecommendedLearnwarePageSize" :loading="loading" />
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
        <page-learnware-list :items="singleRecommendedLearnwareItems" :filters="filters" @page-change="pageChange"
          :page="singleRecommendedLearnwarePage" :page-num="singleRecommendedLearnwarePageNum"
          :page-size="singleRecommendedLearnwarePageSize" :loading="loading" />
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