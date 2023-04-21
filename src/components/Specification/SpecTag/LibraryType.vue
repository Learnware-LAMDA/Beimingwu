<script setup>
import { ref, watch } from 'vue'
import MultiSelectGridBtns from './MultiSelectGridBtns.vue'
import TensorflowBtn from './LibraryType/TensorflowBtn.vue'
import PyTorchBtn from './LibraryType/PyTorchBtn.vue'
import ScikitLearnBtn from './LibraryType/ScikitLearnBtn.vue'
import OthersBtn from './LibraryType/OthersBtn.vue'

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
    title: 'PyTorch',
    icon: PyTorchBtn,
  },
  {
    title: 'Tensorflow',
    icon: TensorflowBtn,
  },
  {
    title: 'Scikit-learn',
    icon: ScikitLearnBtn,
  },
  {
    title: 'Others',
    icon: OthersBtn,
  }
]
</script>

<template>
  <multi-select-grid-btns v-model:value="value" :btns="requirementTypeBtns" title="Library type" :cols="cols" :md="md" :sm="sm" :xs="xs" />
</template>

