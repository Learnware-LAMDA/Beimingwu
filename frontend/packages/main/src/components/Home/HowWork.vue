<script setup lang="ts">
import { useI18n } from "vue-i18n";
import process from "../../assets/images/home/process.svg?url";

const { t } = useI18n();
</script>

<template>
  <div class="w-full max-w-[1200px] mx-auto pb-20 md:pb-30 md:px-10">
    <div class="px-5 md:px-0">
      <div class="text-3xl my-5 <md:text-4xl <md:my-5 lg:text-4xl lg:my-7 xl:text-5xl xl:my-10">
        {{ t("Home.How.Title") }}
      </div>
      <p class="text-gray-500">
        {{ t("Home.How.Description") }}
      </p>
    </div>
    <v-responsive class="mt-10 sm:shadow-md border" :aspect-ratio="96 / 55">
      <v-img cover width="100%" :src="process" />
    </v-responsive>
  </div>
</template>
