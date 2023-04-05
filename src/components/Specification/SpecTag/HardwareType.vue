<script setup>
import { ref, watch } from 'vue'
import GridBtns from './GridBtns.vue'
import CPUBtn from './HardwareType/CPUBtn.vue'
import GPUBtn from './HardwareType/GPUBtn.vue'

const emit = defineEmits(['update:value'])

const props = defineProps({
  value: {
    type: String,
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
  (newVal) => emit('update:value', newVal)
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
  <grid-btns v-model:value="value" :btns="requirementTypeBtns" title="Hardware type" :cols="cols" :md="md" :sm="sm" :xs="xs" />
</template>

