<script setup>
import { ref, computed, watch } from 'vue'
import { useDisplay } from 'vuetify'
import UserList from './UserList.vue'
import { VSkeletonLoader } from 'vuetify/labs/VSkeletonLoader'

const display = useDisplay()

const emits = defineEmits(['click:reset', 'click:delete', 'click:export', 'pageChange'])

const props = defineProps({
  items: {
    type: Array,
  },
  page: {
    type: Number,
  },
  pageSize: {
    type: Number,
    default: 10,
  },
  pageNum: {
    type: Number,
    default: 10,
  },
  loading: {
    type: Boolean,
  },
  showPagination: {
    type: Boolean,
    default: true,
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
  if (props.page < props.pageNum) {
    jumpPage(props.page + 1)
  }
}

function formerPage() {
  if (props.page > 1) {
    jumpPage(props.page - 1)
  }
}

function jumpPage(newPage) {
  if (newPage >= 1 && newPage <= props.pageNum) {
    emits('pageChange', newPage)
  }
}

function handleClickReset(id) { 
  emits('click:reset', id)
}

function handleClickDelete(id) { 
  emits('click:delete', id)
}

function handleClickExport(id) { 
  emits('click:export', id)
}
</script>

<template>
  <div>
    <user-list
      v-if="!loading"
      :items="items"
      :cols="cols"
      :md="md"
      :sm="sm"
      :xs="xs"
      @click:delete="handleClickDelete"
      @click:reset="handleClickReset"
      @click:export="handleClickExport"
    />

    <div v-else class="grid p-2 gap-3" :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }">
      <v-skeleton-loader
        v-for="i in pageSize"
        class="w-1/1"
        type="table-tfoot"
      ></v-skeleton-loader>
    </div>
    
    <div v-if="showPagination" class="my-5 flex justify-center items-center">
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
  </div>
</template>