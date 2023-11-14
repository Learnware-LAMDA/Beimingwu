<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useI18n } from "vue-i18n";
import LearnwareCard from "./LearnwareCard.vue";
import oopsImg from "../../assets/images/public/oops.svg?url";
import type { LearnwareCardInfo, Filter } from "@beiming-system/types/learnware";

const emit = defineEmits(["click:edit", "click:delete"]);

const display = useDisplay();

const { t } = useI18n();

export interface Props {
  items: LearnwareCardInfo[];
  filters?: Filter;
  isAdmin?: boolean;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const props = withDefaults(defineProps<Props>(), {
  filters: () => ({
    id: "",
    name: "",
    dataType: "",
    taskType: "",
    libraryType: "",
    scenarioList: [],
    files: [],
  }),
  isAdmin: false,
  cols: 2,
  md: 1,
  sm: 1,
  xs: 1,
});

const realCols = computed(() => {
  if (display.name.value === "xs") {
    return props.xs;
  } else if (display.name.value === "sm") {
    return props.sm;
  } else if (display.name.value === "md") {
    return props.md;
  } else {
    return props.cols;
  }
});

function handleClickEdit(id: string): void {
  emit("click:edit", id);
}

function handleClickDelete(id: string): void {
  emit("click:delete", id);
}
</script>

<template>
  <div
    class="learnware-list-container"
    :class="items.length === 0 ? ['!grid-cols-1', 'h-full'] : []"
    :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
  >
    <TransitionGroup name="fade">
      <template v-for="(item, _i) in items" :key="_i">
        <learnware-card
          :item="item"
          :filters="filters"
          :is-admin="isAdmin"
          :to="item.id ? `/learnwaredetail?id=${item.id}` : ''"
          @click:edit="(id) => handleClickEdit(id)"
          @click:delete="(id) => handleClickDelete(id)"
        />
      </template>
    </TransitionGroup>
    <div v-if="items.length === 0" flat class="no-learnware">
      <v-img class="oops-img" width="100" :src="oopsImg"></v-img>
      {{ t("Learnware.OopsThereNoLearnware") }}
    </div>
  </div>
</template>

<style scoped lang="scss">
.learnware-list-container {
  @apply relative grid p-1 sm:gap-3 sm:p-2 lg:grid-cols-2 xl:grid-cols-2;

  .score {
    @apply text-[0.8rem] lg:text-base;
  }

  .no-learnware {
    @apply w-full py-5 text-center text-2xl;

    .oops-img {
      @apply mx-auto;
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  @apply transition duration-500;
}

.fade-enter,
.fade-leave-to {
  @apply opacity-0;
}
</style>
