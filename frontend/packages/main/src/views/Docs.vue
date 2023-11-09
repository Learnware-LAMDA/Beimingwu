<script setup lang="ts">
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

const router = useRouter();
const { locale } = useI18n();

router.go(-1);
location.href = `https://docs.beiming.cloud${
  locale.value.toLocaleLowerCase() === "zh-cn" ? "/zh-CN/" : ""
}`;
</script>

<template>
  <div></div>
</template>
