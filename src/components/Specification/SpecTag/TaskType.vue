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
import { useI18n } from "vue-i18n";

const { t } = useI18n();

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
    title: t("Submit.Tag.TaskType.Type.Classification"),
    icon: ClassificationBtn,
    value: "Classification",
  },
  {
    title: t("Submit.Tag.TaskType.Type.Regression"),
    icon: RegressionBtn,
    value: "Regression",
  },
  {
    title: t("Submit.Tag.TaskType.Type.Clustering"),
    icon: ClusteringBtn,
    value: "Clustering",
  },
  {
    title: t("Submit.Tag.TaskType.Type.Ranking"),
    icon: RankingBtn,
    value: "Ranking",
  },
  {
    title: t("Submit.Tag.TaskType.Type.ObjectDetection"),
    icon: DetectionBtn,
    value: "Object Detection",
  },
  {
    title: t("Submit.Tag.TaskType.Type.FeatureExtraction"),
    icon: ExtractionBtn,
    value: "Feature Extraction",
  },
  {
    title: t("Submit.Tag.TaskType.Type.Segmentation"),
    icon: SegmantationBtn,
    value: "Segmentation",
  },
  {
    title: t("Submit.Tag.TaskType.Type.Others"),
    icon: OthersBtn,
    value: "Others",
  },
];
</script>

<template>
  <grid-btns
    v-model:value="value"
    :btns="taskTypeBtns"
    :title="t('Submit.Tag.TaskType.TaskType')"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  />
</template>
