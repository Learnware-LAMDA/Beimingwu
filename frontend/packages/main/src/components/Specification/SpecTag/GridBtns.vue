<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import IconBtn from "./IconBtn.vue";
import type { FunctionalComponent, SVGAttributes } from "vue";

export interface Btn {
  title: string;
  icon: FunctionalComponent<SVGAttributes>;
  value: string;
}

export interface Props {
  modelValue: string;
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

const emit = defineEmits(["update:modelValue"]);

const value = computed({
  get() {
    return props.modelValue;
  },
  set(val) {
    emit("update:modelValue", val);
  },
});

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
  value.value = btn.value === value.value ? "" : btn.value;
}
</script>

<template>
  <div class="grid-container">
    <div class="my-title text-h6 !text-base">
      {{ title }}
    </div>
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
        <component
          :is="btn.icon"
          class="icon"
        />
      </icon-btn>
    </div>
  </div>
</template>

<style scoped lang="scss">
.grid-container {
  .my-title {
    @apply my-3 md:mb-5 md:mt-7;
  }

  .btn-container {
    @apply grid gap-2;

    .btn {
      @apply pr-3;

      .icon {
        @apply h-full w-full;
        fill: rgb(var(--v-theme-on-primary));
      }
    }
  }
}
</style>
