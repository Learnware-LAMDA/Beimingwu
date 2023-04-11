<script setup>
import { ref, watch } from 'vue'
import MultiSelectGridBtns from './MultiSelectGridBtns.vue'
import CPUBtn from './DeviceType/CPUBtn.vue'
import GPUBtn from './DeviceType/GPUBtn.vue'

const emit = defineEmits(['update:value'])

const props = defineProps({
  value: {
    type: Array,
    required: true,
  },
  cols: {
    type: Number,
    default: 4,
  },
  md: {
    type: Number,
    default: 4,
  },
  sm: {
    type: Number,
    default: 4,
  },
  xs: {
    type: Number,
    default: 2,
  },
})

const value = ref(props.value)

watch(
  () => value.value,
  (newVal) => emit('update:value', newVal),
  { deep: true }
)

const requirementTypeBtns = [
  {
    title: 'CPU',
    icon: CPUBtn,
  },
  {
    title: 'GPU',
    icon: GPUBtn,
  },
]
</script>

<template>
  <multi-select-grid-btns v-model:value="value" :btns="requirementTypeBtns" title="Device type" :cols="cols" :md="md" :sm="sm" :xs="xs" />
</template>

