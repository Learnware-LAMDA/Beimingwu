<script setup lang="ts">
import process from "../../assets/images/home/process.svg?url";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
</script>

<template>
  <div class="mx-auto w-full max-w-[1200px] py-20 md:px-10 md:py-32">
    <div class="my-8 px-5 md:px-0">
      <div class="my-5 text-3xl font-medium lg:my-7 lg:text-4xl xl:my-10 xl:text-4xl">
        {{ t("Home.Function.Title") }}
      </div>
      <p class="text-gray-500">
        <b> {{ t("Home.Function.SearchAndDeploy.Title") }} </b
        >{{ t("Home.Function.SearchAndDeploy.Description") }}
      </p>
      <p class="text-gray-500">
        <b> {{ t("Home.Function.Submit.Title") }} </b>{{ t("Home.Function.Submit.Description") }}
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
