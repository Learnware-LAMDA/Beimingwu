<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useDisplay } from "vuetify";
import IconBtn from "./IconBtn.vue";

const display = useDisplay();

const props = defineProps({
  value: {
    type: String,
    require: true,
    default: "",
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

function clickBtn(btn): void {
  value.value = btn.value === value.value ? "" : btn.value;
}

watch(
  () => value.value,
  (newValue) => {
    emit("update:value", newValue);
  },
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
        class="btn"
        :title="btn.title"
        :active="btn.value === value"
        @click="() => clickBtn(btn)"
      >
        <component :is="btn.icon" class="icon" />
      </icon-btn>
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

    .btn {
      @apply pr-3;

      .icon {
        @apply w-1/1 h-1/1;
        fill: rgb(var(--v-theme-on-primary));
      }
    }
  }
}
</style>
