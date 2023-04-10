<script setup>
import { ref, onMounted, nextTick, watch, onActivated } from 'vue'
import PageLearnwareList from '@/components/Learnware/PageLearnwareList.vue'

const learnwareItems = ref([])
const page = ref(1)
const pageNum = ref(10)
const pageSize = ref(10)

const loading = ref(false)

const contentRef = ref(null)

const scrollTop = ref(0)

function deleteLearnware(id) {
  learnwareItems.value.splice(learnwareItems.value.findIndex((item) => item.id === id), 1)
}


function pageChange(newPage) {
  page.value = newPage
}

function delay(ms) {
  return new Promise((res) => {
    setTimeout(res, ms)
  })
}

function generateLearnwareItems(num) {
  return Array(num).fill(0).map((_, i) => {
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

function fetchByFilterAndPage(page) {
  if (contentRef.value) {
    contentRef.value.scrollTop = 0
  }

  loading.value = true
  delay(Math.random() * 2000)
    .then(() => {
      learnwareItems.value = generateLearnwareItems(pageSize.value)
      loading.value = false
    })
}

watch(
  () => page.value,
  (newPage) => {
    fetchByFilterAndPage(newPage)
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
  })

  fetchByFilterAndPage(page.value)
})
</script>

<template>
  <div ref="contentRef" class="fixed flex flex-col w-1/1 overflow-y-scroll justify-start items-center">
    <div class="w-1/1 max-w-900px">
      <page-learnware-list :show-pagination="true" :items="learnwareItems" @page-change="pageChange" :page="page"
        :page-num="pageNum" :page-size="pageSize" :loading="loading" @delete="(id) => deleteLearnware(id)" :cols="1"
        :show-actions="true" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.fixed {
  height: calc(100% - var(--v-layout-top));
}
</style>