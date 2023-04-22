<script setup>
import { ref, computed, watch, onMounted, nextTick, onActivated } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'
import DataType from '@/components/Specification/SpecTag/DataType.vue'
import TaskType from '@/components/Specification/SpecTag/TaskType.vue'
import LibraryType from '@/components/Specification/SpecTag/LibraryType.vue'
import FileUpload from '@/components/Specification/FileUpload.vue'
import TagList from '@/components/Specification/SpecTag/TagList.vue'
import PageLearnwareList from '@/components/Learnware/PageLearnwareList.vue'
import MultiRecommendedLearnwareList from '@/components/Learnware/MultiRecommendedLearnwareList.vue'

const route = useRoute()
const router = useRouter()

const display = useDisplay()

const search = ref(route.query.search || '')
const dataType = ref(route.query.dataType || '')
const taskType = ref(route.query.taskType || '')
const libraryType = ref(route.query.libraryType || '')
let _tagList
try {
  _taglist = JSON.parse(route.query.tagList)
}
catch {
  _tagList = []
}
const tagList = ref(_tagList)

const files = ref([])

const multiRecommendedLearnwareSize = ref(4)
const multiRecommendedLearnwareItems = ref([])
const multiRecommendedMatchScore = ref(null)
const singleRecommendedLearnwarePage = ref(1)
const singleRecommendedLearnwarePageNum = ref(1)
const singleRecommendedLearnwarePageSize = ref(10)
const singleRecommendedLearnwareItems = ref([])
const loading = ref(false)

const contentRef = ref(null)
const anchorRef = ref(null)

const scrollTop = ref(0)

const showError = ref(false)
const errorMsg = ref('')
const errorTimer = ref(null)

const showMultiRecommended = computed(() => {
  return multiRecommendedLearnwareItems.value.length > 1
})
const multiRecommendedTips = ref(true)
const singleRecommendedTips = ref(true)

const filters = computed(() => ({
  name: search.value,
  dataType: dataType.value,
  taskType: taskType.value,
  libraryType: libraryType.value,
  tagList: tagList.value,
  files: files.value
}))

function handleDrop(event) {
  files.value = Array.from(event.dataTransfer.files)
}

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
  if (route.query.libraryType) {
    libraryType.value = route.query.libraryType
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
      libraryType: JSON.stringify(libraryType.value),
      tagList: JSON.stringify(tagList.value),
    }
  })
}

function pageChange(newPage) {
  singleRecommendedLearnwarePage.value = newPage
}

function fetchByFilterAndPage(filters, page) {
  showError.value = false
  loading.value = true

  fetch('/api/engine/get_semantic_specification')
    .then((res) => res.json())
    .then((res) => {
      const semanticSpec = res.data.semantic_specification
      semanticSpec.Name.Values = filters.name
      semanticSpec.Data.Values = filters.dataType ? [filters.dataType] : []
      semanticSpec.Task.Values = filters.taskType ? [filters.taskType] : []
      semanticSpec.Library.Values = filters.libraryType ? [filters.libraryType] : []
      semanticSpec.Scenario.Values = filters.tagList
      semanticSpec.Description.Values = ''

      const fd = new FormData()
      fd.append('semantic_specification', JSON.stringify(semanticSpec))
      fd.append('statistical_specification', files.value.length > 0 ? files.value[0] : null)
      fd.append('limit', singleRecommendedLearnwarePageSize.value)
      fd.append('page', singleRecommendedLearnwarePage.value - 1)
      return fd
    })
    .then((fd) => {
      return fetch('/api/engine/search_learnware', {
        method: 'POST',
        body: fd,
      })
    })
    .then((res) => {
        if (res.status === 200) {
          return res
        }
        throw new Error('Network error')
      })
    .then((res) => res.json())
    .then((res) => {
      switch (res.code) {
        case 0: {
          loading.value = false
          if (res.data.learnware_list_multi.length > 1) {
            multiRecommendedLearnwareItems.value = res.data.learnware_list_multi.map((item) => ({
              id: item.learnware_id,
              username: item.username,
              name: item.semantic_specification.Name.Values,
              description: item.semantic_specification.Description.Values,
              dataType: item.semantic_specification.Data.Values[0],
              taskType: item.semantic_specification.Task.Values[0],
              libraryType: item.semantic_specification.Library.Values[0],
              tagList: item.semantic_specification.Scenario.Values
            }))
            multiRecommendedMatchScore.value = Math.floor(res.data.learnware_list_multi[0].matching * 100)
          }
          
          singleRecommendedLearnwareItems.value = res.data.learnware_list_single.map((item) => ({
            id: item.learnware_id,
            username: item.username,
            name: item.semantic_specification.Name.Values,
            description: item.semantic_specification.Description.Values,
            dataType: item.semantic_specification.Data.Values[0],
            taskType: item.semantic_specification.Task.Values[0],
            libraryType: item.semantic_specification.Library.Values[0],
            tagList: item.semantic_specification.Scenario.Values,
            matchScore: files.value.length > 0 ? Math.floor(item.matching * 100) : null
          }))
          singleRecommendedLearnwarePageNum.value = res.data.total_pages
          return
        }
        default: {
          throw new Error(res.msg)
        }
      }
    })
    .catch((err) => {
      console.error(err)
      loading.value = false
      showError.value = true
      clearTimeout(errorTimer.value)
      setTimeout(() => showError.value = false, 2000)
      errorMsg.value = err.message
    })
}

watch(
  () => filters.value,
  () => {
    // saveQuery()
    singleRecommendedLearnwarePage.value = 1
  },
  { deep: true }
)

watch(
  () => singleRecommendedLearnwarePage.value,
  () => {
    if (anchorRef.value) {
      if (display.name.value === 'xs') {
        anchorRef.value.scrollIntoView()
      }
    }
  }
)

watch(
  () => [filters.value, singleRecommendedLearnwarePage.value],
  (newVal) => {
    const [newFilters, newPage] = newVal

    fetchByFilterAndPage(newFilters, newPage)

    if (contentRef.value) {
      if (display.name.value !== 'xs') {
        contentRef.value.scrollTop = 0
      }
    }
  },
  { deep: true }
)


onActivated(() => {
  contentRef.value.scrollTop = scrollTop.value
  fetchByFilterAndPage(filters.value, singleRecommendedLearnwarePage.value)
})

onMounted(() => {
  nextTick(() => {
    contentRef.value.addEventListener('scroll', () => {
      scrollTop.value = contentRef.value.scrollTop
    })

    // loadQuery()
  })
})
</script>

<template>
  <div class="search-container">
    <v-scroll-y-transition class="fixed w-1/1 z-index-10">
      <v-card-actions v-if="showError">
        <v-alert class="w-1/1 max-w-900px mx-auto" closable :text="errorMsg" type="error" @click:close="showError = false" />
      </v-card-actions>
    </v-scroll-y-transition>
    <div class="flex flex-col w-1/1 md:max-w-460px sm:border-r-1">
      <div class="filter">
        <div class="my-3 text-h6">
          <v-icon class="!mt-0 mr-3" icon="mdi-tag-text" color="black" size="small" />Choose semantic specification
        </div>
        <div>
          <div class="mt-7 mb-3 text-h6 !text-1rem">Search by name</div>
          <v-text-field v-model="search" label="Learnware name" hide-details append-inner-icon="mdi-close"
            @click:append-inner="search = ''" />
        </div>
        <data-type :cols="3" :md="2" :sm="2" :xs="2" v-model:value="dataType" />
        <task-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="taskType" />
        <library-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="libraryType" />
        <tag-list class="bg-transparent text-h6 !text-1rem" v-model:value="tagList" :cols="2" :md="2" :sm="2" :xs="2" />
      </div>
      <div class="p-5 pt-0 border-t-1 border-gray-300">
        <div ref="anchorRef" class="mt-3 mb-5 w-1/1 text-h6 transition-all truncate" :class="display.name.value === 'xs' || files.length || isHovering ? ['mb-5'] : []">
          <v-icon class="mr-3" icon="mdi-upload" color="black" size="small" />Upload statistical specification
        </div>

        <file-upload v-model:files="files" :height="28" />
      </div>
    </div>
    <div ref="contentRef" class="content">
      <v-card v-if="showMultiRecommended" flat class="sm:m-2 mt-4 bg-transparent">
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
        <multi-recommended-learnware-list :items="multiRecommendedLearnwareItems"
          :matchScore="multiRecommendedMatchScore" :filters="filters" @page-change="pageChange" :loading="loading" />
      </v-card>
      <v-card flat class="sm:m-2 mt-4 bg-transparent">
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
          :page-size="singleRecommendedLearnwarePageSize" :loading="loading" :show-pagination="singleRecommendedLearnwarePageNum > 1" />
      </v-card>
    </div>
  </div>
</template>

<style scoped lang="scss">
.search-container {
  @apply md: (fixed flex) mx-auto w-1/1;
  height: calc(100% - var(--v-layout-top));

  .filter {
    @apply p-2 w-1/1 md: (h-1/1 overflow-y-scroll) sm:px-5;

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