<script setup lang="ts">
import { computed } from "vue";
interface Props {
  title?: string;
  modelValue: number;
  tabs: string[];
}

const props = withDefaults(defineProps<Props>(), {
  title: "Terminal",
});

const emit = defineEmits(["update:modelValue"]);
const modelValue = computed<number>({
  get() {
    return props.modelValue;
  },
  set(value: number) {
    emit("update:modelValue", value);
  },
});
</script>

<template>
  <div class="flex flex-col overflow-y-hidden rounded-md">
    <div class="relative flex h-7 items-center bg-gray-900">
      <div class="absolute flex">
        <div
          v-for="i in 3"
          :key="i"
          class="ml-1.5 h-3 w-3 rounded-full bg-gray-800"
        />
      </div>
      <div
        class="absolute left-1/2 flex h-6 -translate-x-1/2 transform flex-col justify-center text-xs font-medium text-gray-400"
      >
        {{ props.title }}
      </div>
    </div>

    <!-- tab bar -->
    <div
      v-if="tabs.length > 1"
      class="flex border-b border-gray-900 bg-gray-900"
    >
      <div
        v-for="(tab, index) in tabs"
        :key="index"
        class="flex-1 cursor-pointer border-gray-600 py-1 text-center text-xs text-white"
        :class="[
          modelValue === index ? 'rounded-t bg-gray-700' : 'bg-gray-800',
          index > 0 ? 'border-s' : '',
        ]"
        @click="modelValue = index"
      >
        {{ tab }}
      </div>
    </div>
    <slot />
  </div>
</template>
