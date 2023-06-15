<script setup>
import { ref, computed, watch, onMounted, nextTick, onActivated } from 'vue'
import { useDisplay } from 'vuetify'
import UserRequirement from '@/components/Search/UserRequirement.vue'
import PageLearnwareList from '@/components/Learnware/PageLearnwareList.vue'
import MultiRecommendedLearnwareList from '@/components/Learnware/MultiRecommendedLearnwareList.vue'

const display = useDisplay()

const filters = ref({
  name: '',
  dataType: '',
  taskType: '',
  libraryType: '',
  tagList: [],
  files: [],
})

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
  return multiRecommendedLearnwareItems.value.length > 1 && singleRecommendedLearnwarePage.value === 1
})
const multiRecommendedTips = ref(true)
const singleRecommendedTips = ref(true)

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
      semanticSpec.Name.Values = filters.name ? filters.name : ''
      semanticSpec.Data.Values = filters.dataType ? [filters.dataType] : []
      semanticSpec.Task.Values = filters.taskType ? [filters.taskType] : []
      semanticSpec.Library.Values = filters.libraryType ? [filters.libraryType] : []
      semanticSpec.Scenario.Values = filters.tagList ? filters.tagList : []
      semanticSpec.Description.Values = ''

      const fd = new FormData()
      fd.append('semantic_specification', JSON.stringify(semanticSpec))
      fd.append('statistical_specification', filters.files?.length > 0 ? filters.files[0] : null)
      fd.append('limit', singleRecommendedLearnwarePageSize.value)
      fd.append('page', page)
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
          if (res.data.learnware_list_multi.length > 0) {
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
            matchScore: filters.files?.length > 0 ? Math.floor(item.matching * 100) : null
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

    fetchByFilterAndPage(newFilters, newPage - 1)

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
  fetchByFilterAndPage(filters.value, singleRecommendedLearnwarePage.value - 1)
})

onMounted(() => {
  nextTick(() => {
    contentRef.value.addEventListener('scroll', () => {
      scrollTop.value = contentRef.value.scrollTop
    })
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

    <user-requirement v-model:value="filters" />
    
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

  .content {
    @apply w-1/1 overflow-y-scroll;
  }
}
</style>