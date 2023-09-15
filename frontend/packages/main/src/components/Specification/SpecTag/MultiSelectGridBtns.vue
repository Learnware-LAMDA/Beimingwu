<script setup>
import { ref, computed, watch } from "vue";
import { useDisplay } from "vuetify";
import IconBtn from "./IconBtn.vue";

const display = useDisplay();

const props = defineProps({
  value: {
    type: Array,
    require: true,
    default: () => [],
  },
  btns: {
    type: Array,
    require: true,
    default: () => [],
  },
  title: {
    type: String,
    default: "title",
  },
  cols: {
    type: Number,
    default: 5,
  },
  md: {
    type: Number,
    default: 5,
  },
  sm: {
    type: Number,
    default: 5,
  },
  xs: {
    type: Number,
    default: 3,
  },
});

const emit = defineEmits(["update:value"]);

const value = ref(props.value);

const realCols = computed(() => {
  let { cols } = props;
  if (props.md && display.md.value) {
    cols = props.md;
  } else if (props.sm && display.sm.value) {
    cols = props.sm;
  } else if (props.xs && display.xs.value) {
    cols = props.xs;
  }
  return cols;
});

function clickBtn(btn) {
  if (!value.value) {
    value.value = [];
  }
  if (value.value.includes(btn.title)) {
    value.value.splice(value.value.indexOf(btn.title), 1);
  } else {
    value.value.push(btn.title);
  }
}

watch(
  () => value.value,
  (newValue) => {
    emit("update:value", newValue);
  },
  { deep: true },
);
</script>

<template>
  <div class="grid-container">
    <div class="title text-h6 !text-1rem">{{ title }}</div>
    <div
      class="btn-container"
      :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
    >
      <icon-btn
        v-for="(btn, i) in btns"
        :key="i"
        :icon-component="btn.icon"
        :title="btn.title"
        :active="value && value.includes(btn.title)"
        @click="() => clickBtn(btn)"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.grid-container {
  .title {
    @apply mt-7 mb-5;
  }

  .btn-container {
    @apply grid gap-2;
  }
}
</style>