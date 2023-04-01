<script setup>
import { ref, watch } from 'vue'
import GridBtns from './GridBtns.vue'
import ClassificationBtn from './TaskTypeBtn/ClassificationBtn.vue'
import ClusteringBtn from './TaskTypeBtn/ClusteringBtn.vue'
import DetectionBtn from './TaskTypeBtn/DetectionBtn.vue'
import ExtractionBtn from './TaskTypeBtn/ExtractionBtn.vue'
import GenerationBtn from './TaskTypeBtn/GenerationBtn.vue'
import RegressionBtn from './TaskTypeBtn/RegressionBtn.vue'
import SegmantationBtn from './TaskTypeBtn/SegmentationBtn.vue'
import RankingBtn from './TaskTypeBtn/RankingBtn.vue'

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

const taskTypeBtns = [
  {
    title: 'Classification',
    icon: ClassificationBtn,
  },
  {
    title: 'Clustering',
    icon: ClusteringBtn,
  },
  {
    title: 'Detection',
    icon: DetectionBtn,
  },
  {
    title: 'Extraction',
    icon: ExtractionBtn,
  },
  {
    title: 'Generation',
    icon: GenerationBtn,
  },
  {
    title: 'Regression',
    icon: RegressionBtn,
  },
  {
    title: 'Segmentation',
    icon: SegmantationBtn,
  },
  {
    title: 'Ranking',
    icon: RankingBtn,
  },
]
</script>

<template>
  <grid-btns v-model:value="value" :btns="taskTypeBtns" title="Task Type" :cols="5" :md="4" :sm="4" :xs="2" />
</template>

