<script setup lang="ts">
import process from "../../assets/images/home/process.svg?url";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>

<template>
  <div class="mx-auto w-full max-w-[1200px] py-20 md:px-10 md:py-32">
    <div class="my-8 px-5 md:px-0">
      <div class="my-5 text-3xl lg:my-7 lg:text-4xl xl:my-10 xl:text-5xl">
        {{ t("Home.Function.Title") }}
      </div>
      <p class="text-gray-500">
        {{ t("Home.Function.SearchAndDeploy") }}
      </p>
      <p class="text-gray-500">
        {{ t("Home.Function.Submit") }}
      </p>
    </div>

    <div class="">
      <div class="">
        <v-img :src="process" />
      </div>
      <div></div>
    </div>
  </div>
</template>
