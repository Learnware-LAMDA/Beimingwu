<script setup>
import { ref, watch } from "vue";
import GridBtns from "./GridBtns.vue";
import TensorFlowBtn from "../../../assets/images/specification/libraryType/tensorflow.svg?component";
import PyTorchBtn from "../../../assets/images/specification/libraryType/pytorch.svg?component";
import ScikitLearnBtn from "../../../assets/images/specification/libraryType/scikit-learn.svg?component";
import OthersBtn from "../../../assets/images/specification/libraryType/others.svg?component";
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
    title: t("Submit.Tag.LibraryType.Type.PyTorch"),
    icon: PyTorchBtn,
    value: "PyTorch",
  },
  {
    title: t("Submit.Tag.LibraryType.Type.TensorFlow"),
    icon: TensorFlowBtn,
    value: "TensorFlow",
  },
  {
    title: t("Submit.Tag.LibraryType.Type.Scikit-learn"),
    icon: ScikitLearnBtn,
    value: "Scikit-learn",
  },
  {
    title: t("Submit.Tag.LibraryType.Type.Others"),
    icon: OthersBtn,
    value: "Others",
  },
];
</script>

<template>
  <grid-btns
    v-model:value="value"
    :btns="libraryTypeBtns"
    :title="t('Submit.Tag.LibraryType.LibraryType')"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  />
</template>
