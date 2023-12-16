<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { useDisplay } from "vuetify";
import process from "../../assets/images/home/process.svg?url";
import procresHorizontal from "../../assets/images/home/process-horizontal.svg?url";

const { t } = useI18n();

const display = useDisplay();

const imgSrc = computed(() => (display.smAndDown.value ? procresHorizontal : process));
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
