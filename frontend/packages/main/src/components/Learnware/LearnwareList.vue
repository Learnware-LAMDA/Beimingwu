<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import LearnwareCard from "./LearnwareCard.vue";
import oopsImg from "../../assets/images/public/oops.svg?url";
import type { LearnwareCardInfo, Filter } from "@beiming-system/types/learnware";

const emit = defineEmits(["click:edit", "click:delete"]);

const display = useDisplay();

const router = useRouter();

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
    name: "",
    dataType: "",
    taskType: "",
    libraryType: "",
    tagList: [],
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

function showLearnwareDetail(id: string): void {
  router.push({ path: "/learnwaredetail", query: { id } });
}
</script>

<template>
  <div
    class="learnware-list-container"
    :class="items.length === 0 ? ['!grid-cols-1', 'h-1/1'] : []"
    :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
  >
    <TransitionGroup name="fade">
      <template v-for="(item, _i) in items" :key="_i">
        <learnware-card
          :item="item"
          :filters="filters"
          :is-admin="isAdmin"
          @click="showLearnwareDetail(item.id)"
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
  @apply relative sm:p-2 p-1 grid xl: grid-cols-2 lg:grid-cols-2 sm:gap-3;

  .score {
    @apply lg: '!text-1rem' '!text-0.8rem';
  }

  .no-learnware {
    @apply py-5 w-1/1 text-center text-2xl;

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
