<script setup lang="ts">
import { useI18n } from "vue-i18n";
import process from "../../assets/images/home/process.svg?url";

const { t } = useI18n();
</script>

<template>
  <div class="mx-auto md:pb-30 <md:pb-20 md:px-10 max-w-1200px w-1/1">
    <div class="<md:px-5">
      <div class="xl:(text-5xl my-10) lg:(text-4xl my-7) md:(text-3xl my-5) <md:(text-4xl my-5)">
        {{ t("Home.How.Title") }}
      </div>
      <p class="text-gray-500">
        {{ t("Home.How.Description") }}
      </p>
    </div>
    <v-responsive class="mt-10 sm:shadow-md border-1" :aspect-ratio="96 / 55">
      <v-img cover width="100%" :src="process" />
    </v-responsive>
  </div>
</template>
