<script setup lang="ts">
import { ref, nextTick } from "vue";
import { useI18n } from "vue-i18n";
import anime from "animejs";
import TerminalWindow from "../App/TerminalWindow.vue";
import TerminalCode from "../App/TerminalCode.vue";
import TerminalIpythonHeader from "../App/TerminalIpythonHeader.vue";
import ScrollAnimate from "../App/ScrollAnimate.vue";
import smartRecommendation from "../../assets/images/home/smart-recommendation.png?url";
import { FEATURE_CODE_FRAGMENTS } from "../../constants";
import ProgressedCode from "../App/ProgressedCode.vue";
import process from "../../assets/images/home/process.svg?url";

const { t } = useI18n();

const smartRecommendationRef = ref<HTMLDivElement | null>(null);
const smartRecommendationMsgRef = ref<HTMLDivElement | null>(null);

const reuseRef = ref<HTMLDivElement | null>(null);
const reuseMsgRef = ref<HTMLDivElement | null>(null);
const reuseProgress = ref<number>(0);

const privacyRef = ref<HTMLDivElement | null>(null);
const privacyMsgRef = ref<HTMLDivElement | null>(null);

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
      targets: smartRecommendationMsgRef.value,
      top: [
        { value: ["50%", "50%"], duration: 200 },
        { value: ["50%", "0"], duration: 800 },
      ],
      translateY: [
        { value: ["-50%", "-50%"], duration: 200 },
        { value: ["-50%", "-100%"], duration: 800 },
      ],
      opacity: [
        { value: [0, 1], duration: 200 },
        { value: [1, 1], duration: 800 },
      ],
      easing: "easeInOutQuad",
    },
    0,
  ).add(
    {
      targets: smartRecommendationRef.value,
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
  t1.add({
    targets: reuseMsgRef.value,
    top: [
      { value: ["50%", "50%"], duration: 400 },
      { value: ["50%", "0"], duration: 800 },
    ],
    translateY: [
      { value: ["-50%", "-50%"], duration: 400 },
      { value: ["-50%", "-100%"], duration: 800 },
    ],
    opacity: [
      { value: [0, 1], duration: 400 },
      { value: [1, 1], duration: 800 },
    ],
    easing: "easeInOutQuad",
  })
    .add(
      {
        targets: reuseProgress,
        value: [0, 1],
        duration: 600,
        easing: "easeInOutQuad",
      },
      800,
    )
    .add(
      {
        targets: reuseRef.value,
        opacity: [
          { value: [0, 1], duration: 300 },
          { value: [1, 1], duration: 800 },
        ],
        top: [
          { value: ["50%", "50%"], duration: 700 },
          { value: ["50%", "0"], duration: 400 },
        ],
        translateY: [
          { value: ["-50%", "-50%"], duration: 700 },
          { value: ["-50%", "-100%"], duration: 400 },
        ],
        easing: "easeInOutQuad",
        duration: 1000,
      },
      700,
    );

  // Privacy
  t1.add(
    {
      targets: privacyMsgRef.value,
      opacity: [
        { value: [0, 1], duration: 400 },
        { value: [1, 1], duration: 200 },
      ],
      easing: "easeInOutQuad",
    },
    1800,
  ).add(
    {
      targets: privacyRef.value,
      opacity: [
        { value: [0, 1], duration: 300 },
        { value: [1, 1], duration: 300 },
      ],
    },
    1700,
  );
});
</script>

<template>
  <div class="mx-auto w-full max-w-[1400px] py-20 md:px-10 md:py-32">
    <scroll-animate
      class="h-[4000px] min-h-[200vh]"
      @progress="handleProgress"
    >
      <template #default>
        <div class="sm:h-main-full flex w-full">
          <div class="h-main-full relative w-full sm:w-2/3">
            <div
              ref="smartRecommendationRef"
              class="absolute flex w-full flex-col items-center justify-center bg-gray-50"
              style="top: -50%; transform: translateY(-50%)"
            >
              <img
                class="w-full"
                :src="smartRecommendation"
              />
            </div>

            <div
              ref="reuseRef"
              class="absolute -z-10 flex h-full w-full flex-col items-center justify-center bg-gray-50 px-2 py-8 sm:px-0"
              style="top: 50%; transform: translateY(-50%); opacity: 0"
            >
              <terminal-window
                title="Python"
                :model-value="tabIndex"
                :tabs="tabs"
                class="w-full flex-1 overflow-hidden bg-gray-900"
              >
                <terminal-code>
                  <terminal-ipython-header />
                  <progressed-code
                    :progress="reuseProgress"
                    :fragments="FEATURE_CODE_FRAGMENTS[0].code"
                  />
                </terminal-code>
              </terminal-window>
            </div>

            <div
              ref="privacyRef"
              class="absolute -z-20 flex w-full flex-col items-center justify-center bg-gray-50"
              style="top: 50%; transform: translateY(-50%); opacity: 0"
            >
              <v-img
                :src="process"
                class="w-full"
              />
            </div>
          </div>

          <div class="h-main-full absolute w-full flex-1 pl-8 sm:static">
            <div class="relative h-full">
              <div
                ref="smartRecommendationMsgRef"
                class="absolute w-full px-5 md:px-0"
                style="top: 50%; transform: translateY(-50%); opacity: 0"
              >
                <div class="text-base font-medium md:text-lg lg:text-2xl xl:text-3xl">
                  {{ t(`Home.Feature.Feature1.Name`) }}
                </div>
                <div class="mt-5 text-xs lg:mt-7 lg:text-sm xl:mt-10 xl:text-base">
                  {{ t(`Home.Feature.Feature1.Description`) }}
                </div>
              </div>
              <div
                ref="reuseMsgRef"
                class="absolute w-full px-5 md:px-0"
                style="top: 50%; transform: translateY(-50%); opacity: 0"
              >
                <div class="text-base font-medium md:text-lg lg:text-2xl xl:text-3xl">
                  {{ t(`Home.Feature.Feature2.Name`) }}
                </div>
                <div class="mt-5 text-xs lg:mt-7 lg:text-sm xl:mt-10 xl:text-base">
                  {{ t(`Home.Feature.Feature2.Description`) }}
                </div>
              </div>
              <div
                ref="privacyMsgRef"
                class="absolute w-full px-5 md:px-0"
                style="top: 50%; transform: translateY(-50%); opacity: 0"
              >
                <div class="text-base font-medium md:text-lg lg:text-2xl xl:text-3xl">
                  {{ t(`Home.Feature.Feature3.Name`) }}
                </div>
                <div class="mt-5 text-xs lg:mt-7 lg:text-sm xl:mt-10 xl:text-base">
                  {{ t(`Home.Feature.Feature3.Description`) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </scroll-animate>
  </div>
</template>
