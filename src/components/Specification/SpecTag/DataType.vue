<script setup>
import { ref, watch, computed } from "vue";
import GridBtns from "./GridBtns.vue";
import AudioBtn from "../../../assets/images/specification/dataType/audio.svg?component";
import VideoBtn from "../../../assets/images/specification/dataType/video.svg?component";
import TextBtn from "../../../assets/images/specification/dataType/text.svg?component";
import ImageBtn from "../../../assets/images/specification/dataType/image.svg?component";
import TableBtn from "../../../assets/images/specification/dataType/table.svg?component";
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

const dataTypeBtns = computed(() => [
  {
    title: t("Submit.Tag.DataType.Type.Table"),
    icon: TableBtn,
    value: "Table",
  },
  {
    title: t("Submit.Tag.DataType.Type.Image"),
    icon: ImageBtn,
    value: "Image",
  },
  {
    title: t("Submit.Tag.DataType.Type.Text"),
    icon: TextBtn,
    value: "Text",
  },
  {
    title: t("Submit.Tag.DataType.Type.Video"),
    icon: VideoBtn,
    value: "Video",
  },
  {
    title: t("Submit.Tag.DataType.Type.Audio"),
    icon: AudioBtn,
    value: "Audio",
  },
]);
</script>

<template>
  <grid-btns
    v-model:value="value"
    :btns="dataTypeBtns"
    :title="t('Submit.Tag.DataType.DataType')"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  />
</template>
