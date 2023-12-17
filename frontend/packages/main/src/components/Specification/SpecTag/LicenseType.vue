<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import MultiSelectGridBtns from "./MultiSelectGridBtns.vue";
import type { License, LicenseList } from "@beiming-system/types/learnware";

export interface Props {
  modelValue: LicenseList;
  single?: boolean;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const { t } = useI18n();

const emit = defineEmits(["update:modelValue"]);

const props = withDefaults(defineProps<Props>(), {
  single: false,
  cols: 4,
  md: 4,
  sm: 2,
  xs: 2,
});

const items: {
  title: string;
  icon: string;
  value: License;
}[] = (
  [
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "GPL-2.0",
    "GPL-3.0",
    "LGPL-2.1",
    "LGPL-3.0",
    "AGPL-3.0",
    "ECL-2.0",
    "AFL-3.0",
    "CC-BY-4.0",
    "CC-BY-SA-4.0",
    "Others",
  ] as LicenseList
)
  .sort()
  .map((item: License) => ({
    title: item,
    icon: `mdi-alpha-${item[0].toLowerCase()}-box`,
    value: item,
  }));

const modelValue = computed({
  get() {
    return props.modelValue;
  },
  set(val) {
    emit("update:modelValue", val);
  },
});
</script>

<template>
  <multi-select-grid-btns
    v-model="modelValue"
    :single="single"
    :btns="items"
    :title="t('Submit.SemanticSpecification.License.License')"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  >
    <template #btn="{ title, icon, active, onClick }">
      <div
        :class="{ 'bg-secondary-light dark:bg-secondary-dark': active }"
        class="bg-inactive-light dark:bg-inactive-dark flex cursor-pointer items-center rounded-[2em] p-3 pl-4 text-xs text-white sm:text-sm lg:text-base"
        @click="onClick"
      >
        <v-icon
          class="mr-4"
          :icon="icon"
        />
        <div class="text-xs sm:text-sm lg:text-base">
          {{ title }}
        </div>
      </div>
    </template>
  </multi-select-grid-btns>
</template>
