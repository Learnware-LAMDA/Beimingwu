<script setup>
import { ref, watch } from "vue";
import AudioBtn from "./DataTypeBtn/AudioBtn.vue";
import VideoBtn from "./DataTypeBtn/VideoBtn.vue";
import TextBtn from "./DataTypeBtn/TextBtn.vue";
import ImageBtn from "./DataTypeBtn/ImageBtn.vue";
import TableBtn from "./DataTypeBtn/TableBtn.vue";

const props = defineProps({
  value: {
    type: String,
    default: "",
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

const emit = defineEmits(["update:value"]);

const dataTypeBtns = [
  {
    title: "Audio",
    icon: AudioBtn,
  },
  {
    title: "Video",
    icon: VideoBtn,
  },
  {
    title: "Text",
    icon: TextBtn,
  },
  {
    title: "Image",
    icon: ImageBtn,
  },
  {
    title: "Table",
    icon: TableBtn,
  },
];

const value = ref(props.value);

watch(
  () => value.value,
  (newValue) => {
    emit("update:value", newValue);
  },
);
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
