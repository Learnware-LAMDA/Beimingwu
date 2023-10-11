<script setup lang="ts">
import { useI18n } from "vue-i18n";
import analogyImg from "../../assets/images/home/analogy.png";

const { t } = useI18n();
</script>

<template>
  <div class="mx-auto md:py-30 <md:py-20 md:px-10 max-w-1200px w-1/1">
    <div class="<md:px-5">
      <div class="xl:(text-5xl my-10) lg:(text-4xl my-7) md:(text-3xl my-5) <md:(text-4xl my-5)">
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
