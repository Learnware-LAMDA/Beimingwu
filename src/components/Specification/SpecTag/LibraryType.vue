<script setup>
import { ref, watch } from "vue";
import GridBtns from "./GridBtns.vue";
import TensorFlowBtn from "../../../assets/images/specification/libraryType/tensorflow.svg?component";
import PyTorchBtn from "../../../assets/images/specification/libraryType/pytorch.svg?component";
import ScikitLearnBtn from "../../../assets/images/specification/libraryType/scikit-learn.svg?component";
import OthersBtn from "../../../assets/images/specification/libraryType/others.svg?component";

const emit = defineEmits(["update:value"]);

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
});

const value = ref(props.value);

watch(
  () => value.value,
  (newVal) => emit("update:value", newVal),
  { deep: true },
);

const libraryTypeBtns = [
  {
    title: "PyTorch",
    icon: PyTorchBtn,
  },
  {
    title: "TensorFlow",
    icon: TensorFlowBtn,
  },
  {
    title: "Scikit-learn",
    icon: ScikitLearnBtn,
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
    :btns="libraryTypeBtns"
    title="Library type"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  />
</template>
