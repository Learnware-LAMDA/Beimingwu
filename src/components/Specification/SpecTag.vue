<script setup>
import { ref, computed } from 'vue'
import DataType from '@/components/Specification/SpecTag/DataType.vue'
import TaskType from '@/components/Specification/SpecTag/TaskType.vue'
import LibraryType from '@/components/Specification/SpecTag/LibraryType.vue'
import TagList from '@/components/Specification/SpecTag/TagList.vue'

const emits = defineEmits(['update:dataType', 'update:taskType', 'update:libraryType', 'update:tagList'])

const props = defineProps({
  dataType: {
    type: String,
    required: true,
  },
  taskType: {
    type: String,
    required: true,
  },
  libraryType: {
    type: String,
    required: true,
  },
  tagList: {
    type: Array,
    required: true,
  },
  errorMessages: {
    type: String,
    required: false
  }
})

const dataType = computed({
  get: () => props.dataType,
  set: (val) => emits('update:dataType', val)
})
const taskType = computed({
  get: () => props.taskType,
  set: (val) => emits('update:taskType', val)
})
const libraryType = computed({
  get: () => props.libraryType,
  set: (val) => emits('update:libraryType', val)
})
const tagList = computed({
  get: () => props.tagList,
  set: (val) => emits('update:tagList', val)
})
</script>

<template>
  <div class="spec-tag">
    <v-scroll-y-transition class="fixed left-0 right-0 z-index-10" style="top: var(--v-layout-top)">
      <v-card-actions v-if="errorMessages">
        <v-alert class="w-1/1 max-w-900px mx-auto" closable :text="errorMessages" type="error" />
      </v-card-actions>
    </v-scroll-y-transition>
    <data-type v-model:value="dataType"/>
    <task-type v-model:value="taskType"/>
    <library-type v-model:value="libraryType"/>
    <tag-list v-model:value="tagList" />
  </div>
</template>