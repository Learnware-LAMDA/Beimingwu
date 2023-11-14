<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useDisplay } from "vuetify";
import BigTitle from "../Public/BigTitle.vue";
import UserRequirement from "../Search/UserRequirement.vue";
import ScrollAnimate from "../App/ScrollAnimate.vue";
import PageLearnwareList from "../Learnware/PageLearnwareList.vue";
import MultiRecommendedLearnwareList from "../Learnware/MultiRecommendedLearnwareList.vue";
import type { Filter, LearnwareCardInfo } from "@beiming-system/types/learnware";
import LogoNoText from "../../../public/logo-no-text.svg?component";
import Logo from "../../../public/logo.svg?component";
import anime from "animejs";

const { t } = useI18n();

const display = useDisplay();

const t1 = anime.timeline({ autoplay: false });

const filters = ref<Filter>({
  id: "",
  name: "",
  dataType: "",
  taskType: "",
  libraryType: "",
  scenarioList: [],
  files: [],
});
const multiRecommendedTips = ref(true);
const multiRecommendedLearnwareItems = ref<LearnwareCardInfo[]>(
  Array.from({ length: 2 }, () => ({
    id: "",
    name: "Learnware",
    dataType: "Table",
    taskType: "Classification",
    libraryType: "Scikit-learn",
    scenarioList: [],
    files: [],
    description: "This is a learnware.",
    lastModify: new Date().toISOString(),
    tags: [],
  })),
);
const multiRecommendedMatchScore = ref(0);
const singleRecommendedTips = ref(true);
const singleRecommendedLearnwareItems = ref<LearnwareCardInfo[]>(
  Array.from({ length: 20 }, () => ({
    id: "",
    name: "Learnware",
    dataType: "Table",
    taskType: "Classification",
    libraryType: "Scikit-learn",
    scenarioList: [],
    files: [],
    description: "This is a learnware.",
    lastModify: new Date().toISOString(),
    tags: [],
  })),
);
const singleRecommendedLearnwarePage = ref(1);
const singleRecommendedLearnwarePageNum = ref(1);
const singleRecommendedLearnwarePageSize = ref(20);
const easeLoading = ref(0);
const loading = computed(() => easeLoading.value >= 0.5);
const easeShowMultiRecommended = ref(0);
const showMultiRecommended = computed(() => easeShowMultiRecommended.value >= 0.5);
const isAdmin = ref(false);

const rkmeJsonRef = ref<HTMLDivElement | null>(null);

function handleProgress(progress: number): void {
  t1.seek(t1.duration * progress);
}

const router = useRouter();

onMounted(() => {
  nextTick(() => {
    setTimeout(() => {
      t1.add({
        targets: rkmeJsonRef.value,
        left: ["100%", (): string => (display.mdAndUp.value ? "10%" : "45%")],
        bottom: ["50%", (): string => (display.mdAndUp.value ? "0%" : "45%")],
        easing: "linear",
        duration: 500,
      })
        .add({
          targets: rkmeJsonRef.value,
          opacity: [1, 0],
          easing: "linear",
          duration: 100,
          loop: true,
        })
        .add(
          {
            targets: easeLoading,
            value: [0, 1],
            duration: 100,
            easing: "linear",
          },
          "-=100",
        )
        .add({
          targets: easeLoading,
          value: [1, 0],
          duration: 800,
          easing: "linear",
        })
        .add(
          {
            targets: easeShowMultiRecommended,
            value: [0, 1],
            duration: 800,
            easing: "linear",
          },
          "-=800",
        );
    });
  });
});
</script>

<template>
  <div class="relative bg-gradient-to-b from-sky-700 via-blue-500 to-blue-100">
    <div class="py-20 text-white text-center">
      <big-title>
        <h1>{{ t("Home.Cover.Beiming") }}</h1>
      </big-title>

      <div class="mt-6 px-10 mx-auto max-w-7xl sm:px-20 md:px-40 lg:px-60">
        {{ t("Home.Cover.Introduction") }}
      </div>

      <div class="flex justify-center pt-10">
        <v-btn class="mx-3 bg-white" size="large" @click="router.push('/search')">
          {{ t("Home.Cover.Try") }}
        </v-btn>
        <v-btn class="mx-3" variant="outlined" size="large" @click="router.push('/submit')">
          {{ t("Home.Cover.Submit") }}
        </v-btn>
      </div>
    </div>

    <scroll-animate class="h-[600vh]" @progress="handleProgress">
      <template #default>
        <div class="flex flex-col justify-center items-center px-2 h-main-full w-full">
          <div class="flex flex-col relative h-[90vh] w-full max-w-7xl rounded-md overflow-hidden">
            <div ref="rkmeJsonRef" class="absolute z-10">
              <svg class="w-20" viewBox="-6 -1 37 42">
                <path
                  d="M0 0 v30 h25 v-21 l-9 -9 h-16 z M15 0 v9 a1 1 0 0 0 1 1 h9"
                  fill="white"
                  stroke="black"
                />
                <text x="13" y="38" font-size="7" text-anchor="middle" fill="black">RKME.json</text>
              </svg>
            </div>
            <div class="flex justify-between items-center h-6 bg-gray-900">
              <div class="flex">
                <div class="ml-2" />
                <div class="my-2 ml-1.5 w-2 h-2 bg-gray-800 rounded-full" v-for="i in 3" :key="i" />
                <svg class="mt-1 ml-2 h-5" viewBox="-1 -1 72 11">
                  <defs>
                    <g id="cross">
                      <path
                        d="M 0,0 2,2 M 2,0 0,2"
                        stroke="white"
                        stroke-width="0.3"
                        stroke-linecap="round"
                      />
                    </g>
                  </defs>
                  <path
                    d="M0 10 a2 2 0 0 0 2 -2 v-6 a2 2 0 0 1 2 -2 h60 a2 2 0 0 1 2 2 v6 a2 2 0 0 0 2 2"
                    class="fill-gray-700"
                  />
                  <logo-no-text x="5" y="2" height="6" width="6" />
                  <text
                    x="14"
                    y="5"
                    text-anchor="start"
                    dominant-baseline="middle"
                    font-size="4"
                    fill="white"
                  >
                    Beiming
                  </text>
                  <use href="#cross" x="60" y="4" />
                </svg>
                <svg class="mt-1 mr-2 w-1.5" viewBox="0 0 10 10">
                  <path d="M 0 5 10 5 M5 0 5 10" stroke="white" stroke-width="1" />
                </svg>
              </div>
              <svg class="w-1 m-1 mr-2" viewBox="0 0 10 10">
                <path d="M 1,3 5,9 9,3" stroke="white" stroke-width="1" fill="none" />
              </svg>
            </div>

            <div class="flex items-center h-6 bg-gray-700">
              <div class="text-[0.4rem]">
                <v-icon class="ml-1 p-2">mdi-arrow-left</v-icon>
                <v-icon class="p-2">mdi-arrow-right</v-icon>
                <v-icon class="p-2">mdi-reload</v-icon>
                <v-icon class="p-2">mdi-home-outline</v-icon>
              </div>
              <div
                class="flex flex-col justify-center flex-1 h-3.5 px-1.5 bg-gray-600 rounded-full text-left text-[0.3rem]"
              >
                <div class="flex items-center h-full">
                  <v-icon>mdi-lock</v-icon>
                  <span class="mx-1 text-[0.4rem]"> beiming.cloud </span>
                </div>
              </div>
              <div class="text-[0.4rem]">
                <v-icon class="p-2">mdi-magnify</v-icon>
                <v-icon class="p-2">mdi-dots-horizontal</v-icon>
              </div>
            </div>

            <div class="flex justify-between items-center bg-white border-b border-gray-300">
              <div class="p-2">
                <logo class="w-20" />
              </div>
            </div>

            <div class="bg-gray-200 flex-1 md:flex justify-start overflow-hidden">
              <div class="no-scroll h-[40vh] md:min-w-[20rem] md:w-1/4">
                <user-requirement
                  v-model="filters"
                  class="w-[150%] transform scale-[calc(200%/3)] origin-top-left h-[60vh] md:h-[120vh]"
                />
              </div>

              <div class="flex-1">
                <div
                  class="w-[150%] transform scale-[calc(200%/3)] origin-top-left"
                  disabled="true"
                >
                  <v-card v-if="showMultiRecommended" flat class="sm:m-2 mt-4 bg-transparent">
                    <v-card-title v-if="!multiRecommendedTips">
                      {{ t("Search.RecommendedMultipleLearnware") }}
                    </v-card-title>
                    <v-card-text v-if="multiRecommendedTips" class="!p-2">
                      <v-alert
                        v-model="multiRecommendedTips"
                        :title="t('Search.RecommendedMultipleLearnware')"
                        :text="t('Search.RecommendedMultipleLearnwareTips')"
                        closable
                        color="success"
                      >
                        <template #prepend>
                          <v-icon icon="mdi-hexagon-multiple" size="x-large"></v-icon>
                        </template>
                      </v-alert>
                    </v-card-text>
                    <multi-recommended-learnware-list
                      :items="multiRecommendedLearnwareItems"
                      :match-score="multiRecommendedMatchScore"
                      :filters="filters"
                      :loading="loading"
                    />
                  </v-card>
                  <v-card flat class="sm:m-2 mt-4 bg-transparent">
                    <v-card-title v-if="showMultiRecommended && !singleRecommendedTips">
                      {{ t("Search.RecommendedSingleLearnware") }}
                    </v-card-title>
                    <v-card-text v-if="showMultiRecommended && singleRecommendedTips" class="!p-2">
                      <v-alert
                        v-model="singleRecommendedTips"
                        :title="t('Search.RecommendedSingleLearnware')"
                        :text="t('Search.RecommendedSingleLearnwareTips')"
                        closable
                        color="info"
                      >
                        <template #prepend>
                          <v-icon icon="mdi-hexagon" size="x-large"></v-icon>
                        </template>
                      </v-alert>
                    </v-card-text>
                    <page-learnware-list
                      :items="singleRecommendedLearnwareItems"
                      :filters="filters"
                      :page="singleRecommendedLearnwarePage"
                      :page-num="singleRecommendedLearnwarePageNum"
                      :page-size="singleRecommendedLearnwarePageSize"
                      :loading="loading"
                      :is-admin="isAdmin"
                      :show-pagination="singleRecommendedLearnwarePageNum > 1"
                    />
                  </v-card>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </scroll-animate>
  </div>
</template>

<style scoped lang="scss">
:global(.no-scroll .filter) {
  overflow: hidden !important;
}
</style>
