<script setup lang="ts">
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import BigTitle from "../Public/BigTitle.vue";
import system from "/public/system.png";

const { t } = useI18n();

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
        <v-btn class="mx-3" size="large" @click="router.push('/search')">
          {{ t("Home.Cover.Try") }}
        </v-btn>
        <v-btn class="mx-3" variant="outlined" size="large" @click="router.push('/submit')">
          {{ t("Home.Cover.Submit") }}
        </v-btn>
      </div>
    </div>

    <div class="mx-auto px-8 max-w-7xl">
      <v-img class="border rounded-t-lg" :src="system" />
    </div>
  </div>
</template>
