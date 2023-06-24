<script setup>
import { ref, watch } from "vue";
import GridBtns from "./GridBtns.vue";
import AudioBtn from "../../../assets/images/specification/dataType/audio.svg?component";
import VideoBtn from "../../../assets/images/specification/dataType/video.svg?component";
import TextBtn from "../../../assets/images/specification/dataType/text.svg?component";
import ImageBtn from "../../../assets/images/specification/dataType/image.svg?component";
import TableBtn from "../../../assets/images/specification/dataType/table.svg?component";

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

const dataTypeBtns = [
  {
    title: "Table",
    icon: TableBtn,
  },
  {
    title: "Image",
    icon: ImageBtn,
  },
  {
    title: "Text",
    icon: TextBtn,
  },
  {
    title: "Video",
    icon: VideoBtn,
  },
  {
    title: "Audio",
    icon: AudioBtn,
  },
];
</script>

<template>
  <grid-btns
    v-model:value="value"
    :btns="dataTypeBtns"
    title="Data type"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  />
</template>
