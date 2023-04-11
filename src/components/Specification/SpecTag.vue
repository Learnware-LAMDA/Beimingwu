<script setup>
import { ref, watch } from 'vue'
import DataType from '@/components/Specification/SpecTag/DataType.vue'
import TaskType from '@/components/Specification/SpecTag/TaskType.vue'
import DeviceType from '@/components/Specification/SpecTag/DeviceType.vue'
import TagList from '@/components/Specification/SpecTag/TagList.vue'

const emit = defineEmits(['update:dataType', 'update:taskType', 'update:deviceType', 'update:tagList'])

const props = defineProps({
  dataType: {
    type: String,
    required: true,
  },
  taskType: {
    type: String,
    required: true,
  },
  deviceType: {
    type: String,
    required: true,
  },
  tagList: {
    type: Array,
    required: true,
  },
})

const _dataType = ref(props.dataType)
const _taskType = ref(props.taskType)
const _deviceType = ref(props.deviceType)
const _tagList = ref(props.tagList)

watch(
  () => _dataType.value,
  (newVal) => emit('update:dataType', newVal)
)
watch(
  () => _taskType.value,
  (newVal) => emit('update:taskType', newVal)
)
watch(
  () => _deviceType.value,
  (newVal) => emit('update:deviceType', newVal)
)
watch(
  () => _tagList.value,
  (newVal) => emit('update:tagList', newVal)
)
</script>

<template>
  <div class="spec-tag">
    <data-type v-model:value="_dataType"/>
    <task-type v-model:value="_taskType"/>
    <device-type v-model:value="_deviceType"/>
    <tag-list v-model:value="_tagList" />
  </div>
</template>