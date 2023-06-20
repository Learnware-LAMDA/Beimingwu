<script setup>
import { ref, watch } from "vue";
import GridBtns from "./GridBtns.vue";
import AudioBtn from "./DataTypeBtn/AudioBtn.vue";
import VideoBtn from "./DataTypeBtn/VideoBtn.vue";
import TextBtn from "./DataTypeBtn/TextBtn.vue";
import ImageBtn from "./DataTypeBtn/ImageBtn.vue";
import TableBtn from "./DataTypeBtn/TableBtn.vue";

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
