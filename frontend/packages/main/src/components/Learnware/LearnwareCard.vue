<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useI18n } from "vue-i18n";
import TextBtn from "../../assets/images/specification/dataType/text.svg?component";
import ImageBtn from "../../assets/images/specification/dataType/image.svg?component";
import TableBtn from "../../assets/images/specification/dataType/table.svg?component";
import dayjs from "dayjs";
import type { LearnwareCardInfo, Filter } from "@beiming-system/types/learnware";

const { t } = useI18n();

export interface Props {
  item: LearnwareCardInfo;
  filters?: Filter;
  showDownload?: boolean;
  isAdmin?: boolean;
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
  showDownload: true,
  isAdmin: false,
});

const emit = defineEmits(["click:download", "click:edit", "click:delete"]);

const display = useDisplay();

const greaterThanXs = computed(() => display.name.value !== "xs");

const greaterThanSm = computed(() => display.name.value !== "xs" && display.name.value !== "sm");

const avatar = computed(() => {
  if (props.item.dataType === "Table") {
    return TableBtn;
  } else if (props.item.dataType === "Image") {
    return ImageBtn;
  } else if (props.item.dataType === "Text") {
    return TextBtn;
  } else {
    return TableBtn;
  }
});

function getColorByScore(score: number): string {
  if (score > 80) return "#4CAF50";
  if (score > 50) return "#FF9800";
  return "#F44336";
}

function handleClickDownload(id: string): void {
  if (id) {
    emit("click:download", id);
  }
}

function handleClickEdit(id: string): void {
  emit("click:edit", id);
}

function handleClickDelete(id: string): void {
  emit("click:delete", id);
}
</script>

<template>
  <v-card
    flat
    :density="greaterThanXs ? 'comfortable' : 'compact'"
    class="card !py-2"
  >
    <v-card-title
      class="my-title !flex"
      :class="item.username ? '' : 'items-center'"
    >
      <v-avatar
        :size="greaterThanSm ? 'default' : 'small'"
        class="mr-2 !rounded-[0]"
      >
        <component
          :is="avatar"
          :class="item.username ? 'w-full' : 'w-4/5'"
          class="opacity-70"
        />
      </v-avatar>
      <div class="flex-1 overflow-hidden">
        <div class="w-full truncate">
          {{ item.name }}
        </div>
        <div
          v-if="item.username"
          class="text-sm text-gray-600"
        >
          {{ item.username }}
        </div>
      </div>
    </v-card-title>

    <v-card-subtitle>
      <div style="color: red">
        {{
          item.verifyStatus != undefined && item.verifyStatus != "SUCCESS"
            ? t("Learnware.Unverified")
            : ""
        }}
      </div>
    </v-card-subtitle>
    <v-card-text class="card-text">
      <div
        class="label"
        :class="
          filters && filters.dataType && filters.dataType.includes(item.dataType)
            ? 'active'
            : undefined
        "
      >
        {{ t(`Submit.SemanticSpecification.DataType.Type.${item.dataType}`) }}
      </div>
      <div
        class="label"
        :class="
          filters && filters.taskType && filters.taskType.includes(item.taskType)
            ? 'active'
            : undefined
        "
      >
        {{
          t(
            `Submit.SemanticSpecification.TaskType.Type.${item.taskType.replace(
              "Others",
              "OtherTask",
            )}`,
          )
        }}
      </div>
      <div
        class="label"
        :class="
          filters && filters.libraryType && filters.libraryType.includes(item.libraryType)
            ? 'active'
            : undefined
        "
      >
        {{
          t(
            `Submit.SemanticSpecification.LibraryType.Type.${item.libraryType.replace(
              "Others",
              "OtherLibrary",
            )}`,
          )
        }}
      </div>
      <div
        v-for="(scenario, i) in item.scenarioList"
        :key="i"
        class="scenario"
        :class="
          filters && filters.scenarioList && filters.scenarioList.includes(scenario)
            ? 'active'
            : undefined
        "
      >
        {{
          t(
            `Submit.SemanticSpecification.Scenario.Type.${scenario.replace(
              "Others",
              "OtherScenario",
            )}`,
          )
        }}
      </div>
    </v-card-text>
    <v-card-text class="card-text">
      <div class="description">
        {{ item.description }}
      </div>
    </v-card-text>
    <v-card-text class="flex items-end justify-between !py-2">
      <div>
        <div
          v-if="item.matchScore && item.matchScore >= 0"
          class="text-base lg:text-lg xl:text-lg"
        >
          {{ t("Search.SpecificationScore") }}:
          <span :style="`color: ${getColorByScore(item.matchScore)}`">{{ item.matchScore }}</span>
        </div>
        <span class="text-xs text-gray-500">
          {{ t("Search.Updated") }} {{ dayjs(item.lastModify).fromNow() }}
        </span>
      </div>

      <div class="flex items-center">
        <div class="actions -mb-2 -mr-3">
          <v-btn
            v-if="showDownload"
            variant="flat"
            icon="mdi-download"
            :size="greaterThanXs ? undefined : 'small'"
            @click.stop.prevent="() => handleClickDownload(item.id)"
          />
          <v-btn
            v-if="isAdmin"
            variant="flat"
            icon="mdi-pencil"
            :size="greaterThanXs ? undefined : 'small'"
            @click.stop.prevent="() => handleClickEdit(item.id)"
          />
          <v-btn
            v-if="isAdmin"
            variant="flat"
            icon="mdi-delete"
            :size="greaterThanXs ? undefined : 'small'"
            @click.stop.prevent="handleClickDelete(item.id)"
          />
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss">
.card {
  @apply border-b sm:border sm:hover:border sm:hover:border-purple-500;

  .first-row {
    @apply flex items-start justify-between;

    .my-title {
      @apply text-base lg:text-lg xl:text-xl;
    }
  }

  .card-text {
    @apply flex flex-wrap items-center pb-2 pt-0 text-gray-700;

    * {
      @apply mr-2 mt-1;
    }

    .label {
      @apply rounded border-gray-700 bg-gray-400 px-2 text-xs text-white;
    }

    .scenario {
      @apply rounded-[1em] border-gray-700 bg-gray-400 px-2 text-xs text-white;
    }

    .label.active {
      background: rgb(var(--v-theme-primary));
    }

    .scenario.active {
      @apply bg-orange-600;
    }

    .description {
      @apply truncate;
    }
  }

  .placeholder {
    @apply opacity-0;
  }
}
</style>
