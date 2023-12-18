<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import MultiSelectGridBtns from "./MultiSelectGridBtns.vue";
import type { Scenario, ScenarioList } from "@beiming-system/types/learnware";

export interface Props {
  modelValue: ScenarioList;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const { t } = useI18n();

const emit = defineEmits(["update:modelValue"]);

const props = withDefaults(defineProps<Props>(), {
  cols: 4,
  md: 4,
  sm: 2,
  xs: 2,
});

const items = computed<
  {
    title: string;
    icon: string;
    value: Scenario;
  }[]
>(() => [
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Business"),
    icon: "mdi-briefcase",
    value: "Business",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Financial"),
    icon: "mdi-currency-usd",
    value: "Financial",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Health"),
    icon: "mdi-heart",
    value: "Health",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Politics"),
    icon: "mdi-account-group",
    value: "Politics",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Computer"),
    icon: "mdi-desktop-classic",
    value: "Computer",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Internet"),
    icon: "mdi-earth",
    value: "Internet",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Traffic"),
    icon: "mdi-car",
    value: "Traffic",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Nature"),
    icon: "mdi-forest",
    value: "Nature",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Fashion"),
    icon: "mdi-tshirt-crew",
    value: "Fashion",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Industry"),
    icon: "mdi-factory",
    value: "Industry",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Agriculture"),
    icon: "mdi-sprout",
    value: "Agriculture",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Education"),
    icon: "mdi-school",
    value: "Education",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Entertainment"),
    icon: "mdi-movie",
    value: "Entertainment",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Architecture"),
    icon: "mdi-home-city",
    value: "Architecture",
  },
  {
    title: t("Submit.SemanticSpecification.Scenario.Type.Others"),
    icon: "mdi-dots-horizontal-circle",
    value: "Others",
  },
]);

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
    :btns="items"
    :title="t('Submit.SemanticSpecification.Scenario.Scenario')"
    :cols="cols"
    :md="md"
    :sm="sm"
    :xs="xs"
  >
    <template #btn="{ title, icon, active, onClick }">
      <div
        :class="{ 'bg-secondary-light dark:bg-secondary-dark': active }"
        class="bg-inactive-light dark:bg-inactive-dark flex cursor-pointer items-center rounded-[2em] p-3 pl-4 text-xs text-white dark:border sm:text-sm lg:text-base"
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
