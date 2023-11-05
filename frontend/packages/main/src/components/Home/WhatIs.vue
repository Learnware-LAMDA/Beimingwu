<script setup lang="ts">
import { useI18n } from "vue-i18n";
import analogyImg from "../../assets/images/home/analogy.png";

const { t } = useI18n();
</script>

<template>
  <div class="mx-auto py-20 md:py-30 md:px-10 max-w-[1200px] w-full">
    <div class="px-5 md:px-0">
      <div class="text-4xl my-5 md:text-3xl md:my-5 lg:text-4xl lg:my-7 xl:text-5xl xl:my-10">
        {{ t("Home.What.Title") }}
      </div>
      <p class="text-gray-500">
        {{ t("Home.What.Description") }}
      </p>
    </div>

    <div class="mt-10 sm:shadow-md">
      <v-img :src="analogyImg" />
    </div>
  </div>
</template>
