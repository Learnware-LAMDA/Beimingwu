<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useDisplay } from "vuetify";

export interface Btn {
  title: string;
  icon: string;
  value: string;
}

export interface Props {
  modelValue: string[];
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

const modelValue = ref(props.modelValue);

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
  if (modelValue.value.includes(btn.value)) {
    modelValue.value = modelValue.value.filter((item) => item !== btn.value);
  } else {
    modelValue.value = [...modelValue.value, btn.value];
  }
}

watch(
  () => modelValue.value,
  (newValue) => {
    emit("update:modelValue", newValue);
  },
  { deep: true },
);
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
          :active="modelValue.includes(btn.value)"
          :on-click="() => clickBtn(btn)"
        />
      </template>
    </div>
  </div>
</template>
