<script setup>
import { ref, computed, watch } from 'vue'
import { useDisplay } from 'vuetify'
import LearnwareList from './LearnwareList.vue'
import { VSkeletonLoader } from 'vuetify/labs/VSkeletonLoader'

const display = useDisplay()

const emit = defineEmits(['delete', 'pageChange'])

defineExpose({
  getPage: () => page.value
})

const props = defineProps({
  filters: {
    type: Object,
  },
  showActions: {
    type: Boolean,
    default: false,
  },
  pageSize: {
    type: Number,
    default: 10,
  },
  pageNum: {
    type: Number,
    default: 10,
  },
  cols: {
    type: Number,
    default: 2,
  },
  md: {
    type: Number,
    default: 1,
  },
  sm: {
    type: Number,
    default: 1,
  },
  xs: {
    type: Number,
    default: 1,
  }
})

const page = ref(1)
const loading = ref(false)

function generateLearnwareItems() {
  return Array(props.pageSize).fill(0).map((_, i) => {
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

const realCols = computed(() => {
  switch (display.name.value) {
    case 'md': if (props.md) return props.md
    case 'sm': if (props.sm) return props.sm
    case 'xs': if (props.xs) return props.xs
    default: return props.cols
  }
})

const greaterThanXs = computed(() => {
  return display.name.value !== 'xs'
})

function nextPage() {
  if (page.value < props.pageNum) {
    page.value += 1
  }
}

function formerPage() {
  if (page.value > 1) {
    page.value -= 1
  }
}

function jumpPage(newPage) {
  if (newPage >= 1 && newPage <= props.pageNum) {
    page.value = newPage
  }
}

const items = ref(generateLearnwareItems())

function deleteLearnware(id) {
  emit('delete', id)
}

function delay(ms) {
  return new Promise((res) => {
    setTimeout(res, ms)
  })
}

watch(
  [() => props.filters, () => page.value],
  () => {
    loading.value = true
    emit('pageChange')
    
    delay(1000)
      .then(() => {
        items.value = generateLearnwareItems()
        loading.value = false
      })
  }
)
</script>

<template>
  <learnware-list
    v-if="!loading"
    :items="items"
    :filters="filters"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
    :show-actions="showActions"
    @delete="deleteLearnware"
  />

  <div v-else class="grid p-2 gap-3" :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }">
    <v-skeleton-loader
      v-for="i in pageSize"
      class="w-1/1"
      type="article"
    ></v-skeleton-loader>
  </div>
  
  <div class="mt-5 flex justify-center items-center">
    <div v-if="pageNum <= 7">
      <v-btn icon="mdi-arrow-left" color="primary" @click="formerPage"></v-btn>
      <v-btn v-for="i in pageNum" :key="i" class="mx-1 !px-2 !min-w-0" :color="i === page ? 'primary' : 'default'" @click="() => jumpPage(i)" flat>{{ i }}</v-btn>
      <v-btn icon="mdi-arrow-right" color="primary" @click="nextPage"></v-btn>
    </div>
    <div v-else>
      <v-btn icon="mdi-arrow-left" color="primary" @click="formerPage"></v-btn>
      <v-btn v-if="greaterThanXs && page > 2" class="mx-2 !px-2 !min-w-0" variant="text" @click="jumpPage(1)">1</v-btn>
      <v-btn v-if="greaterThanXs && page === 4" class="mx-2 !px-2 !min-w-0" variant="text" @click="jumpPage(2)">2</v-btn>
      <v-btn v-if="greaterThanXs && page > 4" class="mx-2 !px-2 !min-w-0" variant="text">...</v-btn>
      <v-btn v-if="greaterThanXs && page > pageNum - 1" class="mx-2 !px-2 !min-w-0" variant="text" @click="() => jumpPage(page - 4)">{{ page - 4 }}</v-btn>
      <v-btn v-if="greaterThanXs &&page > pageNum - 2" class="mx-2 !px-2 !min-w-0" variant="text" @click="() => jumpPage(page - 3)">{{ page - 3 }}</v-btn>
      <v-btn v-if="greaterThanXs && page > pageNum - 3" class="mx-2 !px-2 !min-w-0" variant="text" @click="() => jumpPage(page - 2)">{{ page - 2 }}</v-btn>
      <v-btn v-if="page > 1" class="mx-2 !px-2 !min-w-0" variant="text" @click="() => jumpPage(page - 1)">{{ page - 1 }}</v-btn>
      <v-btn class="mx-2 !px-2 !min-w-0" color="primary">{{ page }}</v-btn>
      <v-btn v-if="page < pageNum" class="mx-2 !px-2 !min-w-0" variant="text" @click="() => jumpPage(page + 1)">{{ page + 1 }}</v-btn>
      <v-btn v-if="greaterThanXs && page < 4" class="mx-2 !px-2 !min-w-0" variant="text" @click="() => jumpPage(page + 2)">{{ page + 2 }}</v-btn>
      <v-btn v-if="greaterThanXs && page < 3" class="mx-2 !px-2 !min-w-0" variant="text" @click="() => jumpPage(page + 3)">{{ page + 3 }}</v-btn>
      <v-btn v-if="greaterThanXs && page < 2" class="mx-2 !px-2 !min-w-0" variant="text" @click="() => jumpPage(page + 4)">{{ page + 4 }}</v-btn>
      <v-btn v-if="greaterThanXs && page < pageNum - 3" class="mx-2 !px-2 !min-w-0" variant="text">...</v-btn>
      <v-btn v-if="greaterThanXs && page === pageNum - 3" class="mx-2 !px-2 !min-w-0" variant="text" @click="() => jumpPage(pageNum - 1)">{{ pageNum - 1 }}</v-btn>
      <v-btn v-if="greaterThanXs && page < pageNum - 1" class="mx-2 !px-2 !min-w-0" variant="text" @click="() => jumpPage(pageNum)">{{ pageNum }}</v-btn>
      <v-btn icon="mdi-arrow-right" color="primary" @click="nextPage"></v-btn>
    </div>
  </div>
</template>
