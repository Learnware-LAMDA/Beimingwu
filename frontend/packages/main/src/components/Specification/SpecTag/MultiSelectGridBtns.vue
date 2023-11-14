<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useDisplay } from "vuetify";
import IconBtn from "./IconBtn.vue";

export interface Btn {
  title: string;
  icon: string;
}

export interface Props {
  value: string[];
  btns: Btn[];
  title: string;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const display = useDisplay();

const props = withDefaults(defineProps<Props>(), {
  cols: 5,
  md: 5,
  sm: 5,
  xs: 3,
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

function clickBtn(btn: Btn): void {
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
    <div class="my-title text-h6 !text-base">{{ title }}</div>
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
  .my-title {
    @apply mb-5 mt-7;
  }

  .btn-container {
    @apply grid gap-2;
  }
}
</style>
