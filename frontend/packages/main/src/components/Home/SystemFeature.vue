<script setup lang="ts">
import { ref, nextTick, watch } from "vue";
import { computedAsync } from "@vueuse/core";
import { useI18n } from "vue-i18n";
import anime from "animejs";
import TerminalWindow from "../App/TerminalWindow.vue";
import TerminalCode from "../App/TerminalCode.vue";
import TerminalIpythonHeader from "../App/TerminalIpythonHeader.vue";
import SearchDemo from "../App/SearchDemo.vue";
import ScrollAnimate from "../App/ScrollAnimate.vue";
import { getFeatureCode } from "../../constants";
import ProgressedCode from "../App/ProgressedCode.vue";
import collaboration from "@main/assets/images/home/collaboration.svg?component";
import type { LanguageName } from "@main/i18n";

const { t, locale } = useI18n();

const FEATURE_CODE_FRAGMENTS = getFeatureCode();

const recommendationRef = ref<HTMLDivElement | null>(null);
const recommendationTextRef = ref<HTMLDivElement | null>(null);

const scrollRef = ref<HTMLDivElement | null>(null);

const loadAndReuseRef = ref<HTMLDivElement | null>(null);
const loadAndReuseTextRef = ref<HTMLDivElement | null>(null);
const loadAndReuseTitleRefs = ref<(HTMLDivElement | null)[]>([]);
const loadAndReuseDescriptionTextRef = ref<HTMLDivElement | null>(null);
const loadProgress = ref<number>(0);
const reuseProgress = ref<number>(0);

const privacyRef = ref<HTMLDivElement | null>(null);
const privacyTextRef = ref<HTMLDivElement | null>(null);

const openSourceRef = ref<HTMLDivElement | null>(null);
const openSourceTextRef = ref<HTMLDivElement | null>(null);
const openSourceProgress = ref<number>(0);

const tabs = ref(["Reuse"]);
const tabIndex = ref(0);

const t1 = anime.timeline({ autoplay: false });

const progress = ref<number>(0);

const rawDataURLImports = {
  en: import("../../assets/images/home/raw_data.svg?url"),
  "zh-cn": import("../../assets/images/home/raw_data_zhcn.svg?url"),
};
const rkmeUrlImports = {
  en: import("../../assets/images/home/rkme.svg?url"),
  "zh-cn": import("../../assets/images/home/rkme_zhcn.svg?url"),
};
const rawDataURL = computedAsync(async () => {
  const { default: url } = await rawDataURLImports[locale.value as LanguageName];
  return url;
});
const rkmeUrl = computedAsync(async () => {
  const { default: url } = await rkmeUrlImports[locale.value as LanguageName];
  return url;
});

function handleProgress(_progress: number): void {
  progress.value = _progress;
  t1.seek(t1.duration * _progress);
}

nextTick(() => {
  // Smart Recommendation
  t1.add(
    {
      targets: recommendationTextRef.value,
      top: [
        { value: ["50%", "50%"], duration: 400 },
        { value: ["50%", "0"], duration: 600 },
      ],
      translateY: [
        { value: ["-50%", "-50%"], duration: 400 },
        { value: ["-50%", "-100%"], duration: 600 },
      ],
      opacity: [
        { value: [0, 1], duration: 400 },
        { value: [1, 1], duration: 600 },
      ],
      easing: "easeInOutQuad",
    },
    0,
  ).add(
    {
      targets: recommendationRef.value,
      top: [
        { value: ["50%", "50%"], duration: 600 },
        { value: ["50%", "0"], duration: 400 },
      ],
      translateY: [
        { value: ["-50%", "-50%"], duration: 600 },
        { value: ["-50%", "-100%"], duration: 400 },
      ],
      easing: "easeInOutQuad",
    },
    0,
  );

  // Reuse
  t1.add(
    {
      targets: loadAndReuseTextRef.value,
      top: [
        { value: ["50%", "50%"], duration: 400 },
        { value: ["50%", "50%"], duration: 800 },
        { value: ["50%", "0"], duration: 800 },
      ],
      translateY: [
        { value: ["-50%", "-50%"], duration: 400 },
        { value: ["-50%", "-50%"], duration: 800 },
        { value: ["-50%", "-100%"], duration: 800 },
      ],
      easing: "easeInOutQuad",
    },
    800,
  )
    .add(
      {
        targets: loadAndReuseTitleRefs.value,
        opacity: [0, 1],
        translateY: ["50%", "0"],
        duration: 300,
        easing: "linear",
        delay: anime.stagger(600),
      },
      800,
    )
    .add(
      {
        targets: loadAndReuseDescriptionTextRef.value,
        opacity: [0, 1],
        translateY: ["50%", "0"],
        duration: 300,
        easing: "linear",
      },
      1400,
    )
    .add(
      {
        targets: loadProgress,
        value: [0, 1],
        duration: 600,
        easing: "easeInOutQuad",
      },
      800,
    )
    .add(
      {
        targets: reuseProgress,
        value: [0, 1],
        duration: 600,
        easing: "easeInOutQuad",
      },
      1400,
    )
    .add(
      {
        targets: loadAndReuseRef.value,
        opacity: [
          { value: [0, 1], duration: 300 },
          { value: [1, 1], duration: 2300 },
        ],
        top: [
          { value: ["50%", "50%"], duration: 1700 },
          { value: ["50%", "0"], duration: 600 },
        ],
        translateY: [
          { value: ["-50%", "-50%"], duration: 1700 },
          { value: ["-50%", "-100%"], duration: 600 },
        ],
        easing: "easeInOutQuad",
      },
      800,
    );

  // Privacy
  t1.add(
    {
      targets: privacyTextRef.value,
      top: [
        { value: ["50%", "50%"], duration: 400 },
        { value: ["50%", "0"], duration: 600 },
      ],
      translateY: [
        { value: ["-50%", "-50%"], duration: 400 },
        { value: ["-50%", "-100%"], duration: 600 },
      ],
      opacity: [
        { value: [0, 1], duration: 400 },
        { value: [1, 1], duration: 600 },
      ],
      easing: "easeInOutQuad",
    },
    2800,
  ).add(
    {
      targets: privacyRef.value,
      opacity: [{ value: [0, 1], duration: 300 }],
      top: [
        { value: ["50%", "50%"], duration: 600 },
        { value: ["50%", "0"], duration: 400 },
      ],
      translateY: [
        { value: ["-50%", "-50%"], duration: 600 },
        { value: ["-50%", "-100%"], duration: 400 },
      ],
      easing: "easeInOutQuad",
    },
    2800,
  );

  // Opensource
  t1.add(
    {
      targets: openSourceRef.value,
      opacity: [{ value: [0, 1], duration: 200 }],
      easing: "easeInOutQuad",
    },
    3600,
  )
    .add(
      {
        targets: openSourceTextRef.value,
        opacity: [{ value: [0, 1], duration: 400 }],
        easing: "easeInOutQuad",
      },
      3600,
    )
    .add(
      {
        targets: [".hand1", ".hand2", ".hand3", ".hand4"],
        translateX: function (_el: HTMLElement, index: number) {
          return [index % 2 === 0 ? -4 : 4, 0];
        },
        translateY: function (_el: HTMLElement, index: number) {
          return [index < 2 ? -4 : 4, 0];
        },
        duration: 300,
        easing: "easeInOutQuad",
      },
      3600,
    )
    .add(
      {
        targets: openSourceProgress,
        value: [0, 1],
        duration: 600,
        easing: "easeInOutQuad",
      },
      3600,
    );
});

watch(
  () => progress.value,
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
  <div class="mx-auto w-full max-w-[1400px] py-20 md:px-10 md:py-32">
    <div class="my-8 px-5 md:px-0">
      <div class="my-5 text-3xl font-medium lg:my-7 lg:text-4xl xl:my-10 xl:text-4xl">
        {{ t("Home.Feature.Title") }}
      </div>
      <p class="text-gray-500">
        {{ t("Home.Feature.Description") }}
      </p>
    </div>

    <scroll-animate
      class="h-[6000px] min-h-[200vh]"
      @progress="handleProgress"
    >
      <template #default>
        <div class="sm:h-main-full flex w-full">
          <div class="h-main-full relative w-full sm:w-2/3">
            <div
              ref="recommendationRef"
              class="bg-background absolute flex h-full w-full flex-col items-center justify-center px-4 py-8 sm:px-0"
              style="top: -50%; transform: translateY(-50%)"
            >
              <!--Show in mobile-->
              <div class="text-lg sm:hidden">
                <div class="text-2xl font-medium">
                  {{ t("Home.Feature.Recommendation.Name") }}
                </div>
                <div class="my-4 text-sm">
                  {{ t("Home.Feature.Recommendation.Description") }}
                </div>
              </div>

              <search-demo
                class="aspect-[5/3] w-full"
                :show-multi-recommended="true"
                :loading="false"
              />
            </div>

            <div
              ref="loadAndReuseRef"
              class="bg-background absolute -z-10 flex h-full w-full flex-col items-center justify-center px-4 py-8 sm:px-0"
              style="top: 50%; transform: translateY(-50%); opacity: 0"
            >
              <!--Show in mobile-->
              <div class="text-lg sm:hidden">
                <div
                  v-for="i in 2"
                  :key="i"
                  class="text-2xl font-medium"
                >
                  {{ t(`Home.Feature.loadAndReuse.Name${i}`) }}
                </div>
                <div class="my-4 text-sm">
                  {{ t(`Home.Feature.loadAndReuse.Description`) }}
                </div>
              </div>

              <terminal-window
                title="Python"
                :model-value="tabIndex"
                :tabs="tabs"
                class="aspect-[5/3] w-full overflow-hidden bg-gray-900"
              >
                <div
                  ref="scrollRef"
                  class="flex-1 overflow-y-hidden break-all bg-gray-800 opacity-90"
                >
                  <terminal-code>
                    <terminal-ipython-header />
                    <progressed-code
                      :progress="loadProgress"
                      :fragments="FEATURE_CODE_FRAGMENTS[0].load"
                    />
                    <progressed-code
                      v-if="loadProgress === 1"
                      :progress="reuseProgress"
                      :fragments="FEATURE_CODE_FRAGMENTS[0].reuse"
                    />
                  </terminal-code>
                </div>
              </terminal-window>
            </div>

            <div
              ref="privacyRef"
              class="bg-background absolute -z-20 flex h-full w-full flex-col items-center justify-center px-4 py-8 sm:px-0"
              style="top: 50%; transform: translateY(-50%); opacity: 0"
            >
              <!--Show in mobile-->
              <div class="text-lg sm:hidden">
                <div class="text-2xl font-medium">
                  {{ t(`Home.Feature.Privacy.Name`) }}
                </div>
                <div class="my-4 text-sm">
                  {{ t(`Home.Feature.Privacy.Description`) }}
                </div>
              </div>

              <div class="relative flex aspect-[2] w-full">
                <v-img :src="rawDataURL" />
                <v-img :src="rkmeUrl" />

                <svg
                  class="absolute left-0 top-0 w-full"
                  viewBox="0 0 400 200"
                >
                  <defs>
                    <marker
                      id="arrow-green"
                      viewBox="0 0 10 10"
                      refX="5"
                      refY="5"
                      markerWidth="6"
                      markerHeight="6"
                      orient="auto-start-reverse"
                    >
                      <path
                        d="M 0 0 L 10 5 L 0 10 z"
                        fill="#2CA02C"
                      />
                    </marker>
                    <marker
                      id="arrow-blue"
                      viewBox="0 0 10 10"
                      refX="5"
                      refY="5"
                      markerWidth="6"
                      markerHeight="6"
                      orient="auto-start-reverse"
                    >
                      <path
                        d="M 0 0 L 10 5 L 0 10 z"
                        fill="#1F77B4"
                      />
                    </marker>
                    <marker
                      id="arrow-orange"
                      viewBox="0 0 10 10"
                      refX="5"
                      refY="5"
                      markerWidth="6"
                      markerHeight="6"
                      orient="auto-start-reverse"
                    >
                      <path
                        d="M 0 0 L 10 5 L 0 10 z"
                        fill="#FF7F0E"
                      />
                    </marker>
                  </defs>

                  <path
                    d="M158 78 S253 -2 348 68"
                    fill="none"
                    color="#2CA02C"
                    stroke="#2CA02C"
                    stroke-dasharray="3"
                    marker-end="url(#arrow-green)"
                  >
                    <animate
                      attributeName="stroke-dashoffset"
                      from="6"
                      to="0"
                      dur="500ms"
                      repeatCount="indefinite"
                    />
                  </path>
                  <path
                    d="M97 75 S141 -5 285 75"
                    fill="none"
                    stroke="#FF7F0E"
                    stroke-dasharray="3"
                    marker-end="url(#arrow-orange)"
                  >
                    <animate
                      attributeName="stroke-dashoffset"
                      from="6"
                      to="0"
                      dur="500ms"
                      repeatCount="indefinite"
                    />
                  </path>
                  <path
                    d="M56 140 S151 60 246 126"
                    fill="none"
                    stroke="#1F77B4"
                    stroke-dasharray="3"
                    marker-end="url(#arrow-blue)"
                  >
                    <animate
                      attributeName="stroke-dashoffset"
                      from="6"
                      to="0"
                      dur="500ms"
                      repeatCount="indefinite"
                    />
                  </path>
                </svg>
              </div>
            </div>

            <div
              ref="openSourceRef"
              class="bg-background absolute -z-30 flex h-full w-full flex-col items-center justify-center px-4 py-8 sm:px-0"
              style="top: 50%; transform: translateY(-50%); opacity: 0"
            >
              <!--Show in mobile-->
              <div class="text-lg sm:hidden">
                <div class="text-2xl font-medium">
                  {{ t(`Home.Feature.OpenSource.Name`) }}
                </div>
                <div class="my-4 text-sm">
                  {{ t(`Home.Feature.OpenSource.Description`) }}
                </div>
              </div>

              <collaboration class="mx-auto w-4/5" />
            </div>
          </div>

          <!-- Show in iPad and larger -->
          <div class="h-main-full absolute hidden w-full flex-1 pl-8 sm:static sm:block">
            <div class="relative h-full">
              <div
                ref="recommendationTextRef"
                class="absolute w-full px-5 md:px-0"
                style="top: 50%; transform: translateY(-50%); opacity: 0"
              >
                <div class="text-lg font-medium md:text-xl lg:text-2xl xl:text-3xl">
                  {{ t(`Home.Feature.Recommendation.Name`) }}
                </div>
                <div class="mt-5 text-xs text-gray-500 lg:mt-7 lg:text-sm xl:mt-10 xl:text-base">
                  {{ t(`Home.Feature.Recommendation.Description`) }}
                </div>
              </div>
              <div
                ref="loadAndReuseTextRef"
                class="absolute w-full px-5 md:px-0"
                style="top: 50%; transform: translateY(-50%)"
              >
                <div
                  v-for="i in 2"
                  :key="i"
                  ref="loadAndReuseTitleRefs"
                  class="mb-1 text-lg font-medium md:text-xl lg:text-2xl xl:text-3xl"
                  style="opacity: 0"
                >
                  {{ t(`Home.Feature.loadAndReuse.Name${i}`) }}
                </div>
                <div
                  ref="loadAndReuseDescriptionTextRef"
                  class="mt-5 text-xs text-gray-500 lg:mt-7 lg:text-sm xl:mt-10 xl:text-base"
                  style="opacity: 0"
                >
                  {{ t(`Home.Feature.loadAndReuse.Description`) }}
                </div>
              </div>
              <div
                ref="privacyTextRef"
                class="absolute w-full px-5 md:px-0"
                style="top: 50%; transform: translateY(-50%); opacity: 0"
              >
                <div class="text-lg font-medium md:text-xl lg:text-2xl xl:text-3xl">
                  {{ t(`Home.Feature.Privacy.Name`) }}
                </div>
                <div class="mt-5 text-xs text-gray-500 lg:mt-7 lg:text-sm xl:mt-10 xl:text-base">
                  {{ t(`Home.Feature.Privacy.Description`) }}
                </div>
              </div>
              <div
                ref="openSourceTextRef"
                class="absolute w-full px-5 md:px-0"
                style="top: 50%; transform: translateY(-50%); opacity: 0"
              >
                <div class="text-lg font-medium md:text-xl lg:text-2xl xl:text-3xl">
                  {{ t(`Home.Feature.OpenSource.Name`) }}
                </div>
                <div class="mt-5 text-xs text-gray-500 lg:mt-7 lg:text-sm xl:mt-10 xl:text-base">
                  {{ t(`Home.Feature.OpenSource.Description`) }}
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
:deep(.hand1) {
  transform: translate(-4px, -4px);
}
:deep(.hand2) {
  transform: translate(4px, -4px);
}
:deep(.hand3) {
  transform: translate(-4px, 4px);
}
:deep(.hand4) {
  transform: translate(4px, 4px);
}
</style>
