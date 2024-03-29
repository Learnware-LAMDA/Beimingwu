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
  to?: string;
}

const props = withDefaults(defineProps<Props>(), {
  filters: () => ({
    id: "",
    name: "",
    dataType: "",
    taskType: "",
    libraryType: "",
    scenarioList: [],
    licenseList: [],
    files: [],
  }),
  showDownload: true,
  isAdmin: false,
  to: "",
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
    :to="to"
    :class="to ? 'cursor-pointer' : ''"
  >
    <div class="rounded border-b p-4 sm:border sm:hover:border sm:hover:border-gray-400">
      <div
        class="flex text-base font-medium lg:text-lg xl:text-xl"
        :class="item.username ? '' : 'items-center'"
      >
        <v-avatar
          :size="greaterThanSm ? 'default' : 'small'"
          class="mr-2 rounded-[0]"
        >
          <component
            :is="avatar"
            :class="item.username ? 'w-10' : 'w-4/5'"
            class="fill-black opacity-70 dark:fill-white dark:opacity-100"
          />
        </v-avatar>
        <div class="flex-1 overflow-hidden">
          <div class="w-full truncate text-base md:text-xl">
            {{ item.name }}
          </div>
          <div
            v-if="item.username"
            class="text-xs text-gray-600 dark:text-gray-400 md:text-sm"
          >
            {{ item.username }}
          </div>
        </div>

        <template v-if="item.verifyStatus">
          <v-chip
            v-if="item.verifyStatus"
            :prepend-icon="
              item.verifyStatus === 'FAIL'
                ? 'mdi-close'
                : item.verifyStatus === 'SUCCESS'
                  ? 'mdi-check'
                  : 'mdi-alert'
            "
            :color="
              item.verifyStatus === 'FAIL'
                ? 'error'
                : item.verifyStatus === 'SUCCESS'
                  ? 'success'
                  : 'warning'
            "
          >
            {{ t(`Learnware.VerifyStatus.${item.verifyStatus}`) }}
          </v-chip>
        </template>
      </div>

      <div class="mt-2 flex flex-wrap items-center space-x-2 pb-2 pt-0 text-gray-700">
        <div
          class="my-1 rounded border-gray-700 bg-gray-400 px-2 text-xs text-white dark:border-gray-500 dark:bg-gray-700 dark:text-gray-300"
          :class="
            filters && filters.dataType && filters.dataType.includes(item.dataType)
              ? 'bg-primary'
              : undefined
          "
        >
          {{ t(`Submit.SemanticSpecification.DataType.Type.${item.dataType}`) }}
        </div>
        <div
          class="my-1 rounded border-gray-700 bg-gray-400 px-2 text-xs text-white dark:border-gray-500 dark:bg-gray-700 dark:text-gray-300"
          :class="
            filters && filters.taskType && filters.taskType.includes(item.taskType)
              ? 'bg-primary'
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
          class="my-1 rounded border-gray-700 bg-gray-400 px-2 text-xs text-white dark:border-gray-500 dark:bg-gray-700 dark:text-gray-300"
          :class="
            filters && filters.libraryType && filters.libraryType.includes(item.libraryType)
              ? 'bg-primary'
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
          class="bg-inactive-light dark:bg-inactive-dark my-1 rounded-[1em] border-gray-700 px-2 text-xs text-white dark:border-gray-500 dark:text-gray-300"
          :class="
            filters && filters.scenarioList && filters.scenarioList.includes(scenario)
              ? 'bg-secondary'
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
        <div
          v-for="(license, i) in item.licenseList"
          :key="i"
          class="bg-inactive-light dark:bg-inactive-dark my-1 rounded-[1em] px-2 text-xs text-white dark:border-gray-500"
          :class="
            filters && filters.licenseList && filters.licenseList.includes(license)
              ? 'bg-secondary'
              : undefined
          "
        >
          {{
            license === "Others"
              ? t("Submit.SemanticSpecification.License.Type.OtherLicense")
              : license
          }}
        </div>
      </div>
      <div
        class="mt-1 overflow-hidden truncate whitespace-nowrap pb-2 pt-0 text-sm text-gray-700 dark:text-gray-300"
      >
        {{ item.description }}
      </div>

      <div class="mt-2 flex items-end justify-between">
        <div>
          <div
            v-if="item.matchScore && item.matchScore >= 0"
            class="text-base lg:text-lg xl:text-lg"
          >
            {{ t("Search.SpecificationScore") }}:
            <span :style="`color: ${getColorByScore(item.matchScore)}`">{{ item.matchScore }}</span>
          </div>
          <span class="text-xs text-gray-500 dark:text-gray-400">
            {{ t("Search.Updated") }} {{ dayjs.utc(item.lastModify.replace(" UTC", "")).fromNow() }}
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
      </div>
    </div>
  </v-card>
</template>
