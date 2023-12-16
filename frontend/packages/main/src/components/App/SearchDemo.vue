<script setup lang="ts">
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import { useDisplay } from "vuetify";
import UserRequirement from "../Search/UserRequirement.vue";
import MultiRecommendedLearnwareList from "../Learnware/MultiRecommendedLearnwareList.vue";
import PageLearnwareList from "../Learnware/PageLearnwareList.vue";
import Browser from "./Browser.vue";
import type { Filter, LearnwareCardInfo } from "@beiming-system/types/learnware";

const { t } = useI18n();

const display = useDisplay();

const props = defineProps<{
  loading: boolean;
  showMultiRecommended: boolean;
}>();

const filters = computed<Filter>(() => ({
  id: "",
  name: "",
  dataType: "",
  taskType: "",
  libraryType: "",
  scenarioList: [],
  licenseList: [],
  files: props.loading || props.showMultiRecommended ? [new File([], "RKME.json")] : [],
}));
const multiRecommendedTips = ref(true);
const multiRecommendedLearnwareItems = computed<LearnwareCardInfo[]>(() =>
  Array.from(
    { length: 2 },
    (): LearnwareCardInfo => ({
      id: "",
      name: t("Home.Cover.LearnwareName"),
      username: t("Home.Cover.Developer"),
      dataType: "Table",
      taskType: "Classification",
      libraryType: "Scikit-learn",
      scenarioList: [],
      licenseList: [],
      description: t("Home.Cover.LearnwareDescription"),
      lastModify: new Date().toISOString(),
    }),
  ),
);

const singleRecommendedTips = ref(true);
const singleRecommendedLearnwareItems = computed<LearnwareCardInfo[]>(() =>
  Array.from(
    { length: 20 },
    (): LearnwareCardInfo => ({
      id: "",
      name: t("Home.Cover.LearnwareName"),
      username: t("Home.Cover.Developer"),
      dataType: "Table",
      taskType: "Classification",
      libraryType: "Scikit-learn",
      scenarioList: [],
      licenseList: [],
      description: t("Home.Cover.LearnwareDescription"),
      lastModify: new Date().toISOString(),
    }),
  ),
);
</script>

<template>
  <Browser>
    <div class="flex flex-1 justify-start overflow-hidden bg-gray-100 dark:bg-gray-800">
      <div
        v-if="display.mdAndUp.value || (!showMultiRecommended && !loading)"
        class="no-scroll h-full w-full min-w-[5rem] sm:w-1/4"
      >
        <user-requirement
          v-model="filters"
          :show-example="false"
          class="relative h-[150%] w-[150%] origin-top-left scale-[calc(100%/1.5)] transform md:h-[300%] md:w-[300%] md:scale-[calc(100%/3)] xl:h-[200%] xl:w-[200%] xl:scale-[calc(100%/2)]"
        />
      </div>

      <div
        v-if="display.smAndUp.value || showMultiRecommended || loading"
        class="flex-1"
      >
        <div
          class="w-[200%] origin-top-left scale-[calc(100%/2)] transform overflow-hidden md:w-[300%] md:scale-[calc(100%/3)] xl:w-[200%] xl:scale-[calc(100%/2)]"
          disabled="true"
        >
          <div
            v-if="showMultiRecommended"
            flat
            class="mt-4 bg-transparent sm:mt-2"
          >
            <v-card-text
              v-if="multiRecommendedTips"
              class="px-2 py-0"
            >
              <v-alert
                :model-value="true"
                color="success"
              >
                <template #prepend>
                  <v-icon
                    icon="mdi-hexagon-multiple"
                    :size="display.smAndUp.value ? 'x-large' : 'small'"
                  />
                </template>
                <template #title>
                  <span class="text-base md:text-xl">
                    {{ t("Search.RecommendedMultipleLearnware") }}</span
                  >
                </template>
                <template #text>
                  <span class="text-xs md:text-base">
                    {{ t("Search.RecommendedMultipleLearnwareTips") }}
                  </span>
                </template>
              </v-alert>
            </v-card-text>
            <v-card-title
              v-else
              class="text-base md:text-xl"
            >
              <v-icon>mdi-hexagon-multiple</v-icon>
              {{ t("Search.RecommendedMultipleLearnware") }}
            </v-card-title>

            <multi-recommended-learnware-list
              :items="multiRecommendedLearnwareItems"
              :match-score="0"
              :filters="filters"
              :loading="loading"
            />
          </div>
          <div
            flat
            class="mt-4 bg-transparent sm:m-0"
          >
            <v-card-title
              v-if="showMultiRecommended && !singleRecommendedTips"
              class="text-base md:text-xl"
            >
              <v-icon>mdi-hexagon</v-icon>
              {{ t("Search.RecommendedSingleLearnware") }}
            </v-card-title>
            <v-card-text
              v-if="showMultiRecommended && singleRecommendedTips"
              class="px-2 py-0"
            >
              <v-alert
                :model-value="true"
                color="info"
              >
                <template #prepend>
                  <v-icon
                    icon="mdi-hexagon"
                    :size="display.smAndUp.value ? 'x-large' : 'default'"
                  />
                </template>
                <template #title>
                  <span class="text-base md:text-xl">
                    {{ t("Search.RecommendedSingleLearnware") }}
                  </span>
                </template>
                <template #text>
                  <span class="text-xs md:text-base">
                    {{ t("Search.RecommendedSingleLearnwareTips") }}
                  </span>
                </template>
              </v-alert>
            </v-card-text>
            <page-learnware-list
              :items="singleRecommendedLearnwareItems"
              :filters="filters"
              :page="1"
              :page-num="1"
              :page-size="20"
              :loading="loading"
              :is-admin="false"
              :show-pagination="false"
            />
          </div>
        </div>
      </div>
    </div>
  </Browser>
</template>
