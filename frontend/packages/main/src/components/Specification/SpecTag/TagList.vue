<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const emit = defineEmits(["update:value"]);

const display = useDisplay();

const props = defineProps({
  value: {
    type: Array,
    required: true,
  },
  cols: {
    type: Number,
    default: 4,
  },
  md: {
    type: Number,
    default: 4,
  },
  sm: {
    type: Number,
    default: 2,
  },
  xs: {
    type: Number,
    default: 1,
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

const items = computed(() => [
  {
    text: t("Submit.Tag.Scenario.Type.Business"),
    icon: "mdi-briefcase",
    value: "Business",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Financial"),
    icon: "mdi-currency-usd",
    value: "Financial",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Health"),
    icon: "mdi-heart",
    value: "Health",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Politics"),
    icon: "mdi-account-group",
    value: "Politics",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Computer"),
    icon: "mdi-desktop-classic",
    value: "Computer",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Internet"),
    icon: "mdi-earth",
    value: "Internet",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Traffic"),
    icon: "mdi-car",
    value: "Traffic",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Nature"),
    icon: "mdi-tree",
    value: "Nature",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Fashion"),
    icon: "mdi-tshirt-crew",
    value: "Fashion",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Industry"),
    icon: "mdi-factory",
    value: "Industry",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Agriculture"),
    icon: "mdi-tractor",
    value: "Agriculture",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Education"),
    icon: "mdi-school",
    value: "Education",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Entertainment"),
    icon: "mdi-movie",
    value: "Entertainment",
  },
  {
    text: t("Submit.Tag.Scenario.Type.Architecture"),
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

function click(value): void {
  if (props.value && props.value.includes(value)) {
    deleteSelect(value);
  } else {
    addSelect(value);
  }
}

function addSelect(value): void {
  if (props.value) {
    emit("update:value", [...props.value, value]);
  } else {
    emit("update:value", [value]);
  }
}

function deleteSelect(value): void {
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
  <div class="tag-container" flat>
    <div class="title text-h6 !text-1rem">
      {{ t("Submit.Tag.Scenario.Scenario") }}
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
.tag-container {
  .title {
    @apply mt-7 mb-5;
  }

  .list {
    @apply grid sm: gap-2 gap-1 bg-transparent;

    .item {
      @apply flex items-center p-3 pl-4 bg-gray-400 text-white rounded-2em cursor-pointer;
    }

    .active {
      @apply bg-orange-600;
    }

    .v-list-item {
      @apply '!overflow-visible';

      * {
        @apply '!overflow-visible';
      }
    }
  }

  .text {
    @apply lg: text-1rem sm:text-sm text-xs;
  }
}
</style>
