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
  <grid-btns v-model:value="value" :btns="requirementTypeBtns" title="Requirement" :cols="4" :md="4" :sm="4" :xs="2" />
</template>

