<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useI18n } from "vue-i18n";
import type { Scenario, ScenarioList } from "@beiming-system/types/learnware";

export interface Props {
  value: ScenarioList;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const { t } = useI18n();

const emit = defineEmits(["update:value"]);

const display = useDisplay();

const props = withDefaults(defineProps<Props>(), {
  cols: 4,
  md: 4,
  sm: 2,
  xs: 1,
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

const items = computed<
  {
    text: string;
    icon: string;
    value: Scenario;
  }[]
>(() => [
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Business"),
    icon: "mdi-briefcase",
    value: "Business",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Financial"),
    icon: "mdi-currency-usd",
    value: "Financial",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Health"),
    icon: "mdi-heart",
    value: "Health",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Politics"),
    icon: "mdi-account-group",
    value: "Politics",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Computer"),
    icon: "mdi-desktop-classic",
    value: "Computer",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Internet"),
    icon: "mdi-earth",
    value: "Internet",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Traffic"),
    icon: "mdi-car",
    value: "Traffic",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Nature"),
    icon: "mdi-forest",
    value: "Nature",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Fashion"),
    icon: "mdi-tshirt-crew",
    value: "Fashion",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Industry"),
    icon: "mdi-factory",
    value: "Industry",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Agriculture"),
    icon: "mdi-sprout",
    value: "Agriculture",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Education"),
    icon: "mdi-school",
    value: "Education",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Entertainment"),
    icon: "mdi-movie",
    value: "Entertainment",
  },
  {
    text: t("Submit.SemanticSpecification.Scenario.Type.Architecture"),
    icon: "mdi-home-city",
    value: "Architecture",
  },
]);

const allSelected = computed(() => props.value && props.value.length === items.value.length);

const selections = computed(() => {
  if (props.value) {
    return props.value.map((s) => items.value.find((item) => item.value === s));
  }
  return [];
});

function click(value: Scenario): void {
  if (props.value && props.value.includes(value)) {
    deleteSelect(value);
  } else {
    addSelect(value);
  }
}

function addSelect(value: Scenario): void {
  if (props.value) {
    emit("update:value", [...props.value, value]);
  } else {
    emit("update:value", [value]);
  }
}

function deleteSelect(value: Scenario): void {
  if (props.value) {
    emit(
      "update:value",
      props.value.filter((s) => s !== value),
    );
  } else {
    emit("update:value", []);
  }
}
</script>

<template>
  <div class="scenario-container" flat>
    <div class="my-title text-h6 !text-base">
      {{ t("Submit.SemanticSpecification.Scenario.Scenario") }}
    </div>

    <v-divider v-if="!allSelected"></v-divider>

    <div class="list" :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }">
      <template v-for="item in items" :key="item.text">
        <div
          :class="selections.includes(item) ? ['active'] : []"
          class="item text"
          @click="() => click(item.value)"
        >
          <v-icon class="mr-4" :icon="item.icon"></v-icon>
          <div class="text" v-text="item.text"></div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped lang="scss">
.scenario-container {
  .my-title {
    @apply mt-7 mb-5;
  }

  .list {
    @apply grid sm:gap-2 gap-1 bg-transparent;

    .item {
      @apply flex items-center p-3 pl-4 bg-gray-400 text-white rounded-[2em] cursor-pointer;
    }

    .active {
      @apply bg-orange-600;
    }

    .v-list-item {
      @apply overflow-visible;

      * {
        @apply overflow-visible;
      }
    }
  }

  .text {
    @apply lg:text-base sm:text-sm text-xs;
  }
}
</style>
