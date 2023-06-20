<script setup>
import { ref, watch } from "vue";
import GridBtns from "./GridBtns.vue";
import ClassificationBtn from "./TaskTypeBtn/ClassificationBtn.vue";
import ClusteringBtn from "./TaskTypeBtn/ClusteringBtn.vue";
import DetectionBtn from "./TaskTypeBtn/DetectionBtn.vue";
import ExtractionBtn from "./TaskTypeBtn/ExtractionBtn.vue";
import RegressionBtn from "./TaskTypeBtn/RegressionBtn.vue";
import SegmantationBtn from "./TaskTypeBtn/SegmentationBtn.vue";
import RankingBtn from "./TaskTypeBtn/RankingBtn.vue";
import OthersBtn from "./TaskTypeBtn/OthersBtn.vue";

const emit = defineEmits(["update:value"]);

const props = defineProps({
  value: {
    type: String,
    required: true,
  },
  cols: {
    type: Number,
    default: 5,
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
});

const value = ref(props.value);

watch(
  () => value.value,
  (newVal) => emit("update:value", newVal),
);

const taskTypeBtns = [
  {
    title: "Classification",
    icon: ClassificationBtn,
  },
  {
    title: "Regression",
    icon: RegressionBtn,
  },
  {
    title: "Clustering",
    icon: ClusteringBtn,
  },
  {
    title: "Ranking",
    icon: RankingBtn,
  },
  {
    title: "Object Detection",
    icon: DetectionBtn,
  },
  {
    title: "Feature Extraction",
    icon: ExtractionBtn,
  },
  {
    title: "Segmentation",
    icon: SegmantationBtn,
  },
  {
    title: "Others",
    icon: OthersBtn,
  },
];
</script>

<template>
  <grid-btns
    v-model:value="value"
    :btns="taskTypeBtns"
    title="Task type"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  />
</template>
