<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import BigTitle from "../Public/BigTitle.vue";
import system from "../../../public/search.mp4";
import ScrollAnimate from "../App/ScrollAnimate.vue";

const { t } = useI18n();

const videoElement = ref<HTMLVideoElement | null>(null);
const duration = ref(0);

onMounted(() => {
  nextTick(() => {
    setTimeout(() => {
      if (videoElement.value) {
        videoElement.value.onloadedmetadata = (): void => {
          duration.value = videoElement.value?.duration ?? 0;
        };
      }
    });
  });
});

const router = useRouter();
</script>

<template>
  <div
    class="relative text-center text-white bg-gradient-to-b from-sky-700 via-blue-500 to-blue-100"
  >
    <div class="py-20">
      <big-title>
        <h1>{{ t("Home.Cover.Beiming") }}</h1>
      </big-title>

      <div class="flex justify-center pt-10">
        <v-btn class="mx-3 bg-white" size="large" @click="router.push('/search')">
          {{ t("Home.Cover.Try") }}
        </v-btn>
        <v-btn class="mx-3" variant="outlined" size="large" @click="router.push('/submit')">
          {{ t("Home.Cover.Submit") }}
        </v-btn>
      </div>
    </div>

    <scroll-animate class="h-[800vh]">
      <template #default="{ progress }">
        <div class="h-main-full w-full flex flex-col justify-center items-center">
          <div class="w-full max-w-7xl">
            duration: {{ duration }} progress: {{ progress }} currentTime:
            {{ (duration * progress).toFixed(3) }}
            <video
              ref="videoElement"
              muted
              class="w-full rounded-lg"
              :currentTime="(duration * progress).toFixed(3)"
            >
              <source :src="system" type="video/mp4" />
            </video>
          </div>
        </div>
      </template>
    </scroll-animate>
  </div>
</template>
