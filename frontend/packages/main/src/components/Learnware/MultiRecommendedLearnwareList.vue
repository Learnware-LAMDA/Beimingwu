<script setup lang="ts">
import { ref, computed } from "vue";
import { useDisplay } from "vuetify";
import { useI18n } from "vue-i18n";
import { downloadMultipleLearnwaresSync } from "../../utils/download";
import LearnwareCard from "./LearnwareCard.vue";
import oopsImg from "../../assets/images/public/oops.svg?url";
import type { LearnwareCardInfo, Filter } from "@beiming-system/types/learnware";

export interface Props {
  items: LearnwareCardInfo[];
  matchScore: number;
  filters?: Filter;
  showActions?: boolean;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
  loading?: boolean;
}

const emit = defineEmits(["download"]);

const display = useDisplay();

const { t } = useI18n();

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
  showActions: false,
  cols: 2,
  md: 1,
  sm: 1,
  xs: 1,
  loading: false,
});

const downloading = ref(false);

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

function downloadAll(): void {
  emit("download");
  downloadMultipleLearnwaresSync(props.items.map((item) => item.id));
}

function getColorByScore(score: number): string {
  if (score > 80) return "#4CAF50";
  if (score > 50) return "#FF9800";
  return "#F44336";
}
</script>

<template>
  <div
    v-if="!loading"
    class="m-2 rounded-md p-2 hover:border-purple-500 md:rounded-lg"
    :class="items.length > 0 ? ['border'] : []"
  >
    <div
      v-if="items.length > 0"
      class="flex justify-between"
    >
      <v-card-title
        v-if="matchScore"
        class="score text-base md:text-lg xl:text-xl"
      >
        {{ t("Search.TotalSpecificationScore") }}
        <span
          class="ml-1 lg:ml-2"
          :style="`color: ${getColorByScore(matchScore)}`"
          >{{ matchScore }}</span
        >
      </v-card-title>
      <v-btn
        variant="flat"
        :size="display.mdAndUp ? 'x-large' : 'large'"
        class="text-body-2 border px-4"
        @click.stop="() => downloadAll()"
      >
        <span v-if="!downloading">
          <v-icon icon="mdi-download" />
          {{ t("Search.DownloadAll") }}
        </span>
        <span
          v-else
          class="flex items-center"
        >
          <v-progress-circular
            class="mr-3"
            indeterminate
          />
          {{ t("Search.Downloading") }}
        </span>
      </v-btn>
    </div>
    <v-card
      flat
      class="learnware-list-container"
      :class="items.length === 0 ? ['!grid-cols-1', 'h-full'] : null"
      :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
    >
      <TransitionGroup name="fade">
        <learnware-card
          v-for="(item, i) in items"
          :key="i"
          :item="item"
          :filters="filters"
          :show-download="false"
          :to="item.id ? `/learnwaredetail?id=${item.id}` : ''"
        />
      </TransitionGroup>
      <div
        v-if="items.length === 0"
        flat
        class="no-learnware"
      >
        <v-img
          class="oops-img"
          width="100"
          :src="oopsImg"
        />
        {{ t("Learnware.OopsThereNoLearnware") }}
      </div>
    </v-card>
  </div>
  <div
    v-else
    class="grid gap-3 p-2"
    :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
  >
    <v-skeleton-loader
      v-for="(_item, index) in 4"
      :key="index"
      class="w-full"
      type="article"
    />
  </div>
</template>

<style scoped lang="scss">
.learnware-list-container {
  @apply relative mt-2 grid gap-2 bg-transparent md:gap-2 lg:grid-cols-2 xl:grid-cols-2;

  .card {
    @apply border;

    .first-row {
      @apply flex items-center justify-between;

      .title {
        @apply text-base lg:text-lg xl:text-xl;
      }

      .actions {
        @apply mt-1 justify-end;
      }
    }

    .card-text {
      @apply flex flex-wrap items-center pb-2 pt-0 text-gray-700;

      * {
        @apply mr-2 mt-1;
      }

      .label {
        @apply rounded border-gray-700 bg-gray-200 px-2 text-xs text-black;
      }

      .scenario {
        @apply rounded-[1em] border-gray-700 bg-gray-200 px-2 text-xs text-black;
      }

      .label.active {
        @apply border-0 bg-gray-100;
        color: rgb(var(--v-theme-primary));
      }

      .scenario.active {
        @apply border-0 bg-gray-100 text-orange-600;
      }

      .description {
        @apply truncate;
      }
    }

    .placeholder {
      @apply opacity-0;
    }
  }

  .score {
    @apply my-2;
    @apply text-sm lg:text-[1.3rem];
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
