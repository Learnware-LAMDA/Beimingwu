<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useDisplay } from "vuetify";
import { computedAsync } from "@vueuse/core";
import type { LanguageName } from "@main/i18n";

const { t, locale } = useI18n();

const display = useDisplay();

const urlMap: Record<
  "mobile" | "desktop",
  Record<LanguageName, Promise<typeof import("*?url")>>
> = {
  mobile: {
    en: import("../../assets/images/home/process_horizontal.svg?url"),
    "zh-cn": import("../../assets/images/home/process_horizontal_zhcn.svg?url"),
  },
  desktop: {
    en: import("../../assets/images/home/process.svg?url"),
    "zh-cn": import("../../assets/images/home/process_zhcn.svg?url"),
  },
};

const imgSrc = computedAsync<string>(async () => {
  const { default: src } = await (display.smAndDown.value
    ? locale.value === "en"
      ? urlMap.mobile.en
      : urlMap.mobile["zh-cn"]
    : locale.value === "en"
      ? urlMap.desktop.en
      : urlMap.desktop["zh-cn"]);
  return src;
});
</script>

<template>
  <div class="mx-auto w-full max-w-[1400px] py-20 md:px-10 md:py-32">
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

    <div class="bg-white px-5 sm:px-0">
      <v-img
        class="max-h-screen"
        :src="imgSrc"
      />
    </div>
  </div>
</template>
