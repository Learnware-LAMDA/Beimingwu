<script setup lang="ts">
import { computed } from "vue";
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

export interface TaskTypeProps {
  modelValue: string;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const props = withDefaults(defineProps<TaskTypeProps>(), {
  cols: 5,
  md: 4,
  sm: 4,
  xs: 2,
});

const { t } = useI18n();

const emit = defineEmits(["update:modelValue"]);

const modelValue = computed({
  get() {
    return props.modelValue;
  },
  set(val) {
    emit("update:modelValue", val);
  },
});

const taskTypeBtns = computed(() => [
  {
    title: t("Submit.SemanticSpecification.TaskType.Type.Classification"),
    icon: ClassificationBtn,
    value: "Classification",
  },
  {
    title: t("Submit.SemanticSpecification.TaskType.Type.Regression"),
    icon: RegressionBtn,
    value: "Regression",
  },
  {
    title: t("Submit.SemanticSpecification.TaskType.Type.Clustering"),
    icon: ClusteringBtn,
    value: "Clustering",
  },
  {
    title: t("Submit.SemanticSpecification.TaskType.Type.Ranking"),
    icon: RankingBtn,
    value: "Ranking",
  },
  {
    title: t("Submit.SemanticSpecification.TaskType.Type.ObjectDetection"),
    icon: DetectionBtn,
    value: "Object Detection",
  },
  {
    title: t("Submit.SemanticSpecification.TaskType.Type.FeatureExtraction"),
    icon: ExtractionBtn,
    value: "Feature Extraction",
  },
  {
    title: t("Submit.SemanticSpecification.TaskType.Type.Segmentation"),
    icon: SegmantationBtn,
    value: "Segmentation",
  },
  {
    title: t("Submit.SemanticSpecification.TaskType.Type.Others"),
    icon: OthersBtn,
    value: "Others",
  },
]);
</script>

<template>
  <grid-btns
    v-model="modelValue"
    :btns="taskTypeBtns"
    :title="t('Submit.SemanticSpecification.TaskType.TaskType')"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  />
</template>
