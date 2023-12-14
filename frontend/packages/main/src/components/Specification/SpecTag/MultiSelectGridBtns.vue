<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";

export interface Btn {
  title: string;
  icon?: string;
  value: string;
}

export interface Props {
  modelValue: string[];
  btns: Btn[];
  title: string;
  single?: boolean;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const display = useDisplay();

const props = withDefaults(defineProps<Props>(), {
  single: false,
  cols: 5,
  md: 5,
  sm: 5,
  xs: 3,
});

const emit = defineEmits(["update:modelValue"]);

const modelValue = computed<string[]>({
  get() {
    return props.modelValue;
  },
  set(newValue) {
    emit("update:modelValue", newValue);
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
  if (!modelValue.value) {
    modelValue.value = [];
  }
  if (props.single) {
    modelValue.value = [btn.value];
  } else {
    if (modelValue.value.includes(btn.value)) {
      modelValue.value = modelValue.value.filter((item) => item !== btn.value);
    } else {
      modelValue.value = [...modelValue.value, btn.value];
    }
  }
}
</script>

<template>
  <div>
    <div class="my-3 text-base font-medium md:mb-5 md:mt-7">
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
          :active="modelValue.includes(btn.value)"
          :on-click="() => clickBtn(btn)"
        />
      </template>
    </div>
  </div>
</template>
