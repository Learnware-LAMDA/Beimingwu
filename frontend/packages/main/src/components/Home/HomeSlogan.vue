<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useDisplay } from "vuetify";
import BigTitle from "../Public/BigTitle.vue";
import TerminalWindow from "../App/TerminalWindow.vue";
import TerminalCode from "../App/TerminalCode.vue";
import TerminalIpythonHeader from "../App/TerminalIpythonHeader.vue";
import ProgressedCode from "../App/ProgressedCode.vue";
import Browser from "../App/Browser.vue";
import UserRequirement from "../Search/UserRequirement.vue";
import ScrollAnimate from "../App/ScrollAnimate.vue";
import PageLearnwareList from "../Learnware/PageLearnwareList.vue";
import MultiRecommendedLearnwareList from "../Learnware/MultiRecommendedLearnwareList.vue";
import { COVER_CODE_FRAGMENTS as fragments } from "../../constants";
import type { Filter, LearnwareCardInfo } from "@beiming-system/types/learnware";
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
const multiRecommendedMatchScore = ref(0);
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
const singleRecommendedLearnwarePage = ref(1);
const singleRecommendedLearnwarePageNum = ref(1);
const singleRecommendedLearnwarePageSize = ref(20);
const easeShowMultiRecommended = ref(0);
const showMultiRecommended = computed(() => easeShowMultiRecommended.value >= 0.5);
const isAdmin = ref(false);

const rkmeJsonRef = ref<HTMLDivElement | null>(null);
const browserRef = ref<HTMLDivElement | null>(null);

const scrollRef = ref<HTMLDivElement | null>(null);

const easeLoading = ref(0);
const loading = computed(() => easeLoading.value >= 0.5);

const importProgress = ref(0);
const resultProgress = ref(0);
const reuseProgress = ref(0);

const fragmentIndex = ref(0);

const msgs = computed(() => [
  {
    id: 0,
    text: t("Home.Cover.ServeralLinesOfCode"),
    class: "text-5xl md:text-6xl lg:text-7xl",
  },
  {
    id: 1,
    text: t("Home.Cover.SolveYourTasks"),
    class: "text-3xl md:text-4xl lg:text-6xl",
  },
]);
const msgRefs = ref<HTMLDivElement[]>([]);

const progress = ref<number>(0);
function handleProgress(p: number): void {
  t1.seek(t1.duration * p);
  progress.value = p;
}

const router = useRouter();

onMounted(() => {
  nextTick(() => {
    setTimeout(() => {
      t1.add({
        targets: rkmeJsonRef.value,
        left: ["100%", "10%"],
        bottom: ["40%", "0%"],
        easing: "linear",
        duration: 500,
      })
        .add(
          {
            targets: importProgress,
            value: [0, 1],
            easing: "linear",
            duration: 600,
          },
          "-=500",
        )
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
          duration: 600,
          easing: "linear",
        })
        .add(
          {
            targets: resultProgress,
            value: [0, 1],
            easing: "linear",
            duration: 350,
          },
          "-=650",
        )
        .add(
          {
            targets: easeShowMultiRecommended,
            value: [0, 1],
            duration: 100,
            easing: "linear",
          },
          "-=350",
        )
        .add({
          targets: browserRef.value,
          opacity: [1, 0],
          duration: 100,
          easing: "linear",
        })
        .add({
          targets: msgRefs.value,
          translateY: ["200%", "0%"],
          opacity: [0, 1],
          duration: 300,
          easing: "easeInOutQuad",
          delay: anime.stagger(100),
        })
        .add(
          {
            targets: reuseProgress,
            value: [0, 1],
            easing: "linear",
            duration: 300,
          },
          "-=300",
        )
        .add({
          duration: 500,
        });
    });
  });
});

watch(
  () => [progress.value, fragmentIndex.value],
  () => {
    setTimeout(() => {
      if (scrollRef.value) {
        scrollRef.value.scrollTop = scrollRef.value.scrollHeight - scrollRef.value.clientHeight;
      }
    });
  },
  { deep: true },
);
</script>

<template>
  <div class="relative bg-sky-700">
    <div class="py-20 text-center text-white">
      <big-title>
        <div>{{ t("Home.Cover.Beiming") }}</div>
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
      class="h-[4000px] min-h-[200vh]"
      @progress="handleProgress"
    >
      <template #default>
        <div
          class="h-main-full flex w-full flex-col items-center justify-center px-2 transition-all"
        >
          <div class="h-[85vh] w-full max-w-[1800px]">
            <div class="relative h-full">
              <div
                class="absolute aspect-[9/16] max-w-7xl transform transition-all duration-500 lg:aspect-video"
                :class="
                  progress === 0
                    ? ['left-1/2 w-full -translate-x-1/2']
                    : [
                        'left-0 z-10 w-4/5 translate-x-0 md:w-3/5 xl:w-3/5',
                        reuseProgress === 0 ? 'bottom-0' : 'bottom-1/2 w-full translate-y-1/2',
                      ]
                "
              >
                <terminal-window
                  v-model="fragmentIndex"
                  :tabs="fragments.map((fragment) => fragment.name)"
                  class="h-full"
                  title="python"
                >
                  <div
                    ref="scrollRef"
                    class="flex-1 overflow-y-hidden break-all bg-gray-800 opacity-90"
                  >
                    <terminal-code
                      v-for="fragment in fragments"
                      v-show="fragmentIndex === fragment.index"
                      :key="fragment.index"
                    >
                      <terminal-ipython-header />

                      <progressed-code
                        :fragments="fragment.import"
                        :progress="importProgress"
                      />
                      <progressed-code
                        v-if="importProgress === 1"
                        :fragments="fragment.result"
                        :progress="resultProgress"
                      />
                      <progressed-code
                        v-if="resultProgress === 1"
                        :fragments="fragment.reuse"
                        :progress="reuseProgress"
                      />
                    </terminal-code>
                  </div>
                </terminal-window>
              </div>
              <div
                ref="browserRef"
                class="absolute right-0 aspect-[9/16] max-w-7xl transform transition-all duration-500 lg:aspect-video"
                :class="
                  progress === 0
                    ? 'right-1/2 w-full translate-x-1/2'
                    : [
                        'right-0 w-4/5 -translate-x-0 md:w-3/5 xl:w-3/5',
                        showMultiRecommended && 'transition-none',
                      ]
                "
              >
                <Browser class="relative h-full">
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

                  <div class="flex flex-1 justify-start overflow-hidden bg-gray-200">
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
                        <v-card
                          v-if="showMultiRecommended"
                          flat
                          class="mt-4 bg-transparent sm:mt-2"
                        >
                          <v-card-title
                            v-if="!multiRecommendedTips"
                            class="text-h5 text-base md:text-xl"
                          >
                            <v-icon>mdi-hexagon-multiple</v-icon>
                            {{ t("Search.RecommendedMultipleLearnware") }}
                          </v-card-title>
                          <v-card-text
                            v-if="multiRecommendedTips"
                            class="px-2 py-0"
                          >
                            <v-alert
                              v-model="multiRecommendedTips"
                              closable
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
                          <multi-recommended-learnware-list
                            :items="multiRecommendedLearnwareItems"
                            :match-score="multiRecommendedMatchScore"
                            :filters="filters"
                            :loading="loading"
                          />
                        </v-card>
                        <v-card
                          flat
                          class="mt-4 bg-transparent sm:m-0"
                        >
                          <v-card-title
                            v-if="showMultiRecommended && !singleRecommendedTips"
                            class="text-h5 text-base md:text-xl"
                          >
                            <v-icon>mdi-hexagon</v-icon>
                            {{ t("Search.RecommendedSingleLearnware") }}
                          </v-card-title>
                          <v-card-text
                            v-if="showMultiRecommended && singleRecommendedTips"
                            class="px-2 py-0"
                          >
                            <v-alert
                              v-model="singleRecommendedTips"
                              closable
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
                </Browser>
              </div>
              <div
                class="pointer-events-none absolute right-0 z-20 flex h-full w-full flex-col items-center justify-center font-medium text-white opacity-80 sm:w-2/5"
              >
                <div
                  v-for="msg in msgs"
                  ref="msgRefs"
                  :key="msg.id"
                  class="mb-4 text-center"
                  :class="msg.class"
                  :style="{ opacity: 0 }"
                >
                  {{ msg.text }}
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
.no-scroll :deep(.filter) {
  overflow: hidden !important;
}
</style>
