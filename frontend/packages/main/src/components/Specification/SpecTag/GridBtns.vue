<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";

export interface Btn {
  title: any;
  icon: any;
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
  <div>
    <div class="text-h6 my-3 !text-base md:mb-5 md:mt-7">
      {{ title }}
    </div>
    <div
      class="grid gap-2"
      :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
    >
      <template v-for="btn in btns">
        <slot
          name="btn"
          :title="btn.title"
          :icon="btn.icon"
          :active="btn.value === value"
          :on-click="() => clickBtn(btn)"
        />
      </template>
    </div>
  </div>
</template>
