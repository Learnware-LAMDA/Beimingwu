<script setup>
import { ref, watch } from 'vue'
import DataType from './SemanticSpec/DataType.vue'
import TaskType from './SemanticSpec/TaskType.vue'
import HardwareType from './SemanticSpec/HardwareType.vue'
import TagList from './SemanticSpec/TagList.vue'

const emit = defineEmits(['update:dataType', 'update:taskType', 'update:hardwareType', 'update:tagList'])

const props = defineProps({
  dataType: {
    type: String,
    required: true,
  },
  taskType: {
    type: String,
    required: true,
  },
  hardwareType: {
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
const _hardwareType = ref(props.hardwareType)
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
  () => _hardwareType.value,
  (newVal) => emit('update:hardwareType', newVal)
)
watch(
  () => _tagList.value,
  (newVal) => emit('update:tagList', newVal)
)
</script>

<template>
  <div class="semantic-spec">
    <data-type v-model:value="_dataType"/>
    <task-type v-model:value="_taskType"/>
    <hardware-type v-model:value="_hardwareType"/>
    <tag-list v-model:value="_tagList" />
  </div>
</template>

<style scoped lang="scss">
.semantic-spec {
}
</style>