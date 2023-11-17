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
  <div class="md:pb-30 mx-auto w-full max-w-[1200px] pb-20 md:px-10">
    <div class="px-5 md:px-0">
      <div class="my-5 text-3xl lg:my-7 lg:text-4xl xl:my-10 xl:text-5xl">
        {{ t("Home.Why.Title") }}
      </div>
      <p class="text-gray-500">
        {{ t("Home.Why.Description") }}
      </p>
    </div>
    <div class="mt-8 grid gap-2 sm:grid-cols-2 sm:gap-5">
      <div
        v-for="reason in reasons"
        :key="reason.title"
      >
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            flat
            class="fill-height relative transform p-4 transition-all duration-300 ease-in-out"
            :class="{
              'elevation-20': isHovering && !smallerThanMd,
              'bg-primary': isHovering,
              'scale-105': isHovering && !smallerThanMd,
            }"
            v-bind="props"
          >
            <v-card-title class="my-2 text-center">
              <v-icon :size="iconSize">
                {{ reason.icon }}
              </v-icon>
            </v-card-title>
            <v-card-title
              class="font-600 mb-4 text-center text-lg md:text-xl lg:text-xl xl:text-2xl"
            >
              {{ reason.title }}
            </v-card-title>
            <v-card-text class="lg:text-md xl:text-md text-sm !leading-5 md:text-sm">
              {{ reason.description }}
            </v-card-text>
          </v-card>
        </v-hover>
      </div>
    </div>
  </div>
</template>
