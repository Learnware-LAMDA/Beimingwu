<script setup>
import { ref, watch } from "vue";
import GridBtns from "./GridBtns.vue";
import ClassificationBtn from "../../../assets/images/specification/taskType/classification.svg?component";
import ClusteringBtn from "../../../assets/images/specification/taskType/clustering.svg?component";
import DetectionBtn from "../../../assets/images/specification/taskType/detection.svg?component";
import ExtractionBtn from "../../../assets/images/specification/taskType/extraction.svg?component";
import RegressionBtn from "../../../assets/images/specification/taskType/regression.svg?component";
import SegmantationBtn from "../../../assets/images/specification/taskType/segmantation.svg?component";
import RankingBtn from "../../../assets/images/specification/taskType/ranking.svg?component";
import OthersBtn from "../../../assets/images/specification/taskType/others.svg?component";

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
