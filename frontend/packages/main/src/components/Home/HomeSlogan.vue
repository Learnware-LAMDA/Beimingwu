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
  licenseList: [],
  files: [],
});
const multiRecommendedTips = ref(true);
const multiRecommendedLearnwareItems = computed<LearnwareCardInfo[]>(() =>
  Array.from({ length: 2 }, () => ({
    id: "",
    name: t("Home.Cover.LearnwareName"),
    dataType: "Table",
    taskType: "Classification",
    libraryType: "Scikit-learn",
    scenarioList: [],
    licenseList: [],
    files: [],
    description: t("Home.Cover.LearnwareDescription"),
    lastModify: new Date().toISOString(),
    tags: [],
  })),
);
const multiRecommendedMatchScore = ref(0);
const singleRecommendedTips = ref(true);
const singleRecommendedLearnwareItems = computed<LearnwareCardInfo[]>(() =>
  Array.from({ length: 20 }, () => ({
    id: "",
    name: t("Home.Cover.LearnwareName"),
    dataType: "Table",
    taskType: "Classification",
    libraryType: "Scikit-learn",
    scenarioList: [],
    licenseList: [],
    files: [],
    description: t("Home.Cover.LearnwareDescription"),
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
        left: ["100%", (): string => (display.smAndUp.value ? "10%" : "45%")],
        bottom: ["40%", (): string => (display.smAndUp.value ? "0%" : "50%")],
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
          duration: 100,
          easing: "linear",
        })
        .add(
          {
            targets: easeShowMultiRecommended,
            value: [0, 1],
            duration: 100,
            easing: "linear",
          },
          "-=100",
        )
        .add({
          targets: easeShowMultiRecommended,
          value: [1, 1],
          duration: 800,
          easing: "linear",
        });
    });
  });
});
</script>

<template>
  <div class="relative bg-gradient-to-b from-sky-700 via-blue-500 to-blue-100">
    <div class="py-20 text-center text-white">
      <big-title>
        <h1>{{ t("Home.Cover.Beiming") }}</h1>
      </big-title>

      <div class="mx-auto mt-6 max-w-7xl px-10 sm:px-20 md:px-40 lg:px-60">
        {{ t("Home.Cover.Introduction") }}
      </div>

      <div class="flex justify-center pt-10">
        <v-btn
          class="mx-3 bg-white"
          size="large"
          @click="router.push('/search')"
        >
          {{ t("Home.Cover.Try") }}
        </v-btn>
        <v-btn
          class="mx-3"
          variant="outlined"
          size="large"
          @click="router.push('/submit')"
        >
          {{ t("Home.Cover.Submit") }}
        </v-btn>
      </div>
    </div>

    <scroll-animate
      class="h-[300vh]"
      @progress="handleProgress"
    >
      <template #default>
        <div class="h-main-full flex w-full flex-col items-center justify-center px-2">
          <div class="relative flex h-[90vh] w-full max-w-7xl flex-col overflow-hidden rounded-md">
            <div
              ref="rkmeJsonRef"
              class="absolute z-10"
            >
              <svg
                class="w-20"
                viewBox="-6 -1 37 42"
              >
                <path
                  d="M0 0 v30 h25 v-21 l-9 -9 h-16 z M15 0 v9 a1 1 0 0 0 1 1 h9"
                  fill="white"
                  stroke="black"
                />
                <text
                  x="13"
                  y="38"
                  font-size="7"
                  text-anchor="middle"
                  fill="black"
                >
                  RKME.json
                </text>
              </svg>
            </div>
            <div class="flex h-6 items-center justify-between bg-gray-900">
              <div class="flex">
                <div class="ml-2" />
                <div
                  v-for="i in 3"
                  :key="i"
                  class="my-2 ml-1.5 h-2 w-2 rounded-full bg-gray-800"
                />
                <svg
                  class="ml-2 mt-1 h-5"
                  viewBox="-1 -1 72 11"
                >
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
                  <logo-no-text
                    x="5"
                    y="2"
                    height="6"
                    width="6"
                  />
                  <text
                    x="14"
                    y="5"
                    text-anchor="start"
                    dominant-baseline="middle"
                    font-size="4"
                    fill="white"
                  >
                    Beimingwu
                  </text>
                  <use
                    href="#cross"
                    x="60"
                    y="4"
                  />
                </svg>
                <svg
                  class="mr-2 mt-1 w-1.5"
                  viewBox="0 0 10 10"
                >
                  <path
                    d="M 0 5 10 5 M5 0 5 10"
                    stroke="white"
                    stroke-width="1"
                  />
                </svg>
              </div>
              <svg
                class="m-1 mr-2 w-1"
                viewBox="0 0 10 10"
              >
                <path
                  d="M 1,3 5,9 9,3"
                  stroke="white"
                  stroke-width="1"
                  fill="none"
                />
              </svg>
            </div>

            <div class="flex h-6 items-center bg-gray-700">
              <div class="text-[0.4rem]">
                <v-icon class="ml-1 p-2"> mdi-arrow-left </v-icon>
                <v-icon class="p-2"> mdi-arrow-right </v-icon>
                <v-icon class="p-2"> mdi-reload </v-icon>
                <v-icon class="p-2"> mdi-home-outline </v-icon>
              </div>
              <div
                class="flex h-3.5 flex-1 flex-col justify-center rounded-full bg-gray-600 px-1.5 text-left text-[0.3rem]"
              >
                <div class="flex h-full items-center">
                  <v-icon>mdi-lock</v-icon>
                  <span class="mx-1 text-[0.4rem]"> bmwu.cloud </span>
                </div>
              </div>
              <div class="text-[0.4rem]">
                <v-icon class="p-2"> mdi-magnify </v-icon>
                <v-icon class="p-2"> mdi-dots-horizontal </v-icon>
              </div>
            </div>

            <div class="flex items-center justify-between border-b border-gray-300 bg-white">
              <div class="p-2">
                <logo class="w-20" />
              </div>
            </div>

            <div class="flex-1 justify-start overflow-hidden bg-gray-200 md:flex">
              <div class="no-scroll h-[40%] md:h-full md:w-1/4 md:min-w-[20rem]">
                <user-requirement
                  v-model="filters"
                  :show-example="false"
                  class="h-[200%] w-[200%] origin-top-left scale-50 transform md:h-[150%] md:w-[150%] md:scale-[calc(200%/3)]"
                />
              </div>

              <div class="flex-1">
                <div
                  class="w-[150%] origin-top-left scale-[calc(200%/3)] transform"
                  disabled="true"
                >
                  <v-card
                    v-if="showMultiRecommended"
                    flat
                    class="mt-4 bg-transparent sm:m-2"
                  >
                    <v-card-title v-if="!multiRecommendedTips">
                      {{ t("Search.RecommendedMultipleLearnware") }}
                    </v-card-title>
                    <v-card-text
                      v-if="multiRecommendedTips"
                      class="!p-2"
                    >
                      <v-alert
                        v-model="multiRecommendedTips"
                        :title="t('Search.RecommendedMultipleLearnware')"
                        :text="t('Search.RecommendedMultipleLearnwareTips')"
                        closable
                        color="success"
                      >
                        <template #prepend>
                          <v-icon
                            icon="mdi-hexagon-multiple"
                            size="x-large"
                          />
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
                  <v-card
                    flat
                    class="mt-4 bg-transparent sm:m-2"
                  >
                    <v-card-title v-if="showMultiRecommended && !singleRecommendedTips">
                      {{ t("Search.RecommendedSingleLearnware") }}
                    </v-card-title>
                    <v-card-text
                      v-if="showMultiRecommended && singleRecommendedTips"
                      class="!p-2"
                    >
                      <v-alert
                        v-model="singleRecommendedTips"
                        :title="t('Search.RecommendedSingleLearnware')"
                        :text="t('Search.RecommendedSingleLearnwareTips')"
                        closable
                        color="info"
                      >
                        <template #prepend>
                          <v-icon
                            icon="mdi-hexagon"
                            size="x-large"
                          />
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
