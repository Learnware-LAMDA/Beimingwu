<script setup lang="ts">
import { computed } from "vue";
import GridBtns from "./GridBtns.vue";
import TensorFlowBtn from "../../../assets/images/specification/libraryType/tensorflow.svg?component";
import PyTorchBtn from "../../../assets/images/specification/libraryType/pytorch.svg?component";
import ScikitLearnBtn from "../../../assets/images/specification/libraryType/scikit-learn.svg?component";
import OthersBtn from "../../../assets/images/specification/libraryType/others.svg?component";
import { useI18n } from "vue-i18n";

export interface LibraryTypeProps {
  modelValue: string;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const props = withDefaults(defineProps<LibraryTypeProps>(), {
  cols: 4,
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

const libraryTypeBtns = computed(() => [
  {
    title: t("Submit.SemanticSpecification.LibraryType.Type.PyTorch"),
    icon: PyTorchBtn,
    value: "PyTorch",
  },
  {
    title: t("Submit.SemanticSpecification.LibraryType.Type.TensorFlow"),
    icon: TensorFlowBtn,
    value: "TensorFlow",
  },
  {
    title: t("Submit.SemanticSpecification.LibraryType.Type.Scikit-learn"),
    icon: ScikitLearnBtn,
    value: "Scikit-learn",
  },
  {
    title: t("Submit.SemanticSpecification.LibraryType.Type.Others"),
    icon: OthersBtn,
    value: "Others",
  },
]);
</script>

<template>
  <grid-btns
    v-model="modelValue"
    :btns="libraryTypeBtns"
    :title="t('Submit.SemanticSpecification.LibraryType.LibraryType')"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  />
</template>
