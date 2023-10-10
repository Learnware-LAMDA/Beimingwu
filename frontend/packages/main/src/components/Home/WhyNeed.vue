<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useI18n } from "vue-i18n";

const display = useDisplay();

const { t } = useI18n();

const smallerThanMd = computed(() => ["md", "sm", "xs"].includes(display.name.value));

const iconSize = computed(() => 80);

const reasons = computed(() => [
  {
    icon: "mdi-chart-scatter-plot",
    title: t("Home.Why.LackOfTrainingDataSkills"),
    description: t("Home.Why.LackOfTrainingDataSkillsDescription"),
  },
  {
    icon: "mdi-all-inclusive-box",
    title: t("Home.Why.ContinualLearning"),
    description: t("Home.Why.ContinualLearningDescription"),
  },
  {
    icon: "mdi-head-snowflake",
    title: t("Home.Why.CatastrophicForgetting"),
    description: t("Home.Why.CatastrophicForgettingDescription"),
  },
  {
    icon: "mdi-eye-lock",
    title: t("Home.Why.DataPrivacyProprietary"),
    description: t("Home.Why.DataPrivacyProprietaryDescription"),
  },
]);
</script>

<template>
  <div class="mx-auto md:pb-30 <md:pb-20 md:px-10 max-w-1200px w-1/1">
    <div class="<md:px-5">
      <div class="xl:(text-5xl my-10) lg:(text-4xl my-7) md:(text-3xl my-5) <md:(text-4xl my-5)">
        {{ t("Home.Why.Title") }}
      </div>
      <p class="text-gray-500">
        {{ t("Home.Why.Description") }}
      </p>
    </div>
    <div class="mt-8 grid sm:grid-cols-2 sm:gap-5 gap-2">
      <div v-for="reason in reasons" :key="reason.title">
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            flat
            class="relative fill-height p-4 transition-all duration-300 ease-in-out transform"
            :class="{
              'elevation-20': isHovering && !smallerThanMd,
              'bg-primary': isHovering,
              'scale-105': isHovering && !smallerThanMd,
            }"
            v-bind="props"
          >
            <v-card-title class="my-2 text-center">
              <v-icon :size="iconSize">{{ reason.icon }}</v-icon>
            </v-card-title>
            <v-card-title
              class="mb-4 xl:text-2xl lg:text-xl md:text-xl text-lg font-600 text-center"
            >
              {{ reason.title }}
            </v-card-title>
            <v-card-text class="xl:text-md lg:text-md md:text-sm text-sm !leading-5">
              {{ reason.description }}
            </v-card-text>
          </v-card>
        </v-hover>
      </div>
    </div>
  </div>
</template>
