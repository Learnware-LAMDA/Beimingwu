<script setup lang="ts">
import { useI18n } from "vue-i18n";
import process from "../../assets/images/home/process.svg?url";

const { t } = useI18n();
</script>

<template>
  <div class="md:pb-30 mx-auto w-full max-w-[1200px] pb-20 md:px-10">
    <div class="px-5 md:px-0">
      <div class="my-5 text-3xl lg:my-7 lg:text-4xl xl:my-10 xl:text-5xl">
        {{ t("Home.How.Title") }}
      </div>
      <p class="text-gray-500">
        {{ t("Home.How.Description") }}
      </p>
    </div>
    <v-responsive
      class="mt-10 border sm:shadow-md"
      :aspect-ratio="96 / 55"
    >
      <v-img
        cover
        width="100%"
        :src="process"
      />
    </v-responsive>
  </div>
</template>
