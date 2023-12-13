<script setup lang="ts">
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

const router = useRouter();
const { t } = useI18n();

router.go(-1);
location.href = t("Url.Docs.Home");
</script>

<template>
  <div />
</template>
