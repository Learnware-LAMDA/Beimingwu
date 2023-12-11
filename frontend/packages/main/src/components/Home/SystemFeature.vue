<script setup lang="ts">
import { ref, nextTick } from "vue";
import { useI18n } from "vue-i18n";
import anime from "animejs";
import TerminalWindow from "../App/TerminalWindow.vue";
import TerminalCode from "../App/TerminalCode.vue";
import TerminalIpythonHeader from "../App/TerminalIpythonHeader.vue";
import ScrollAnimate from "../App/ScrollAnimate.vue";
import recommendation from "../../assets/images/home/smart-recommendation.png?url";
import { FEATURE_CODE_FRAGMENTS } from "../../constants";
import ProgressedCode from "../App/ProgressedCode.vue";
import process from "../../assets/images/home/process.svg?url";
import collaboration from "../../assets/images/home/collaboration.svg?component";

const { t } = useI18n();

const recommendationRef = ref<HTMLDivElement | null>(null);
const recommendationTextRef = ref<HTMLDivElement | null>(null);

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

function handleProgress(progress: number): void {
  t1.seek(t1.duration * progress);
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
</script>

<template>
  <div class="mx-auto w-full max-w-[1400px] py-20 md:px-10 md:py-32">
    <scroll-animate
      class="h-[6000px] min-h-[200vh]"
      @progress="handleProgress"
    >
      <template #default>
        <div class="sm:h-main-full flex w-full">
          <div class="h-main-full relative w-full sm:w-2/3">
            <div
              ref="recommendationRef"
              class="absolute flex w-full flex-col items-center justify-center bg-gray-50"
              style="top: -50%; transform: translateY(-50%)"
            >
              <div class="p-2 text-lg sm:hidden">
                <div class="text-2xl font-bold">
                  {{ t(`Home.Feature.Recommendation.Name`) }}
                </div>
                <div class="my-4 text-sm">
                  {{ t(`Home.Feature.Recommendation.Description`) }}
                </div>
              </div>
              <img
                class="w-full"
                :src="recommendation"
              />
            </div>

            <div
              ref="loadAndReuseRef"
              class="absolute -z-10 flex h-full w-full flex-col items-center justify-center bg-gray-50 px-2 py-8 sm:px-0"
              style="top: 50%; transform: translateY(-50%); opacity: 0"
            >
              <div class="p-2 text-lg sm:hidden">
                <div
                  v-for="i in 2"
                  :key="i"
                  class="text-2xl font-bold"
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
                class="w-full flex-1 overflow-hidden bg-gray-900"
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
              </terminal-window>
            </div>

            <div
              ref="privacyRef"
              class="absolute -z-20 flex w-full flex-col items-center justify-center bg-gray-50"
              style="top: 50%; transform: translateY(-50%); opacity: 0"
            >
              <div class="p-2 text-lg sm:hidden">
                <div class="text-2xl font-bold">
                  {{ t(`Home.Feature.Privacy.Name`) }}
                </div>
                <div class="my-4 text-sm">
                  {{ t(`Home.Feature.Privacy.Description`) }}
                </div>
              </div>
              <v-img
                :src="process"
                class="w-full"
              />
            </div>

            <div
              ref="openSourceRef"
              class="absolute -z-30 flex w-full flex-col items-center justify-center bg-gray-50"
              style="top: 50%; transform: translateY(-50%); opacity: 0"
            >
              <div class="p-2 text-lg sm:hidden">
                <div class="text-2xl font-bold">
                  {{ t(`Home.Feature.OpenSource.Name`) }}
                </div>
                <div class="my-4 text-sm">
                  {{ t(`Home.Feature.OpenSource.Description`) }}
                </div>
              </div>
              <collaboration class="mx-auto w-4/5" />
            </div>
          </div>

          <div class="h-main-full absolute hidden w-full flex-1 pl-8 sm:static sm:block">
            <div class="relative h-full">
              <div
                ref="recommendationTextRef"
                class="absolute w-full px-5 md:px-0"
                style="top: 50%; transform: translateY(-50%); opacity: 0"
              >
                <div class="text-base font-medium md:text-lg lg:text-2xl xl:text-3xl">
                  {{ t(`Home.Feature.Recommendation.Name`) }}
                </div>
                <div class="mt-5 text-xs lg:mt-7 lg:text-sm xl:mt-10 xl:text-base">
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
                  class="text-base font-medium md:text-lg lg:text-2xl xl:text-3xl"
                  style="opacity: 0"
                >
                  {{ t(`Home.Feature.loadAndReuse.Name${i}`) }}
                </div>
                <div
                  ref="loadAndReuseDescriptionTextRef"
                  class="mt-5 text-xs lg:mt-7 lg:text-sm xl:mt-10 xl:text-base"
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
                <div class="text-base font-medium md:text-lg lg:text-2xl xl:text-3xl">
                  {{ t(`Home.Feature.Privacy.Name`) }}
                </div>
                <div class="mt-5 text-xs lg:mt-7 lg:text-sm xl:mt-10 xl:text-base">
                  {{ t(`Home.Feature.Privacy.Description`) }}
                </div>
              </div>
              <div
                ref="openSourceTextRef"
                class="absolute w-full px-5 md:px-0"
                style="top: 50%; transform: translateY(-50%); opacity: 0"
              >
                <div class="text-base font-medium md:text-lg lg:text-2xl xl:text-3xl">
                  {{ t(`Home.Feature.OpenSource.Name`) }}
                </div>
                <div class="mt-5 text-xs lg:mt-7 lg:text-sm xl:mt-10 xl:text-base">
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
