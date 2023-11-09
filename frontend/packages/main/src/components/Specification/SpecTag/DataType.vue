<script setup lang="ts">
import { computed } from "vue";
import GridBtns from "./GridBtns.vue";
import TextBtn from "../../../assets/images/specification/dataType/text.svg?component";
import ImageBtn from "../../../assets/images/specification/dataType/image.svg?component";
import TableBtn from "../../../assets/images/specification/dataType/table.svg?component";
import { useI18n } from "vue-i18n";

export interface DataTypeProps {
  modelValue: string;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const props = withDefaults(defineProps<DataTypeProps>(), {
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

const dataTypeBtns = computed(() => [
  {
    title: t("Submit.SemanticSpecification.DataType.Type.Table"),
    icon: TableBtn,
    value: "Table",
  },
  {
    title: t("Submit.SemanticSpecification.DataType.Type.Image"),
    icon: ImageBtn,
    value: "Image",
  },
  {
    title: t("Submit.SemanticSpecification.DataType.Type.Text"),
    icon: TextBtn,
    value: "Text",
  },
]);
</script>

<template>
  <grid-btns
    v-model="modelValue"
    :btns="dataTypeBtns"
    :title="t('Submit.SemanticSpecification.DataType.DataType')"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  />
</template>
