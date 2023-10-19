<script lang="ts" setup>
import VPFlyout from "vitepress/dist/client/theme-default/components/VPFlyout.vue";
import VPMenuLink from "vitepress/dist/client/theme-default/components/VPMenuLink.vue";
import { useData } from "vitepress";
import { useLangs } from "../composables";
import "@mdi/font/css/materialdesignicons.min.css";

const { theme } = useData();
const { localeLinks, currentLang } = useLangs({ correspondingLink: true });
</script>

<template>
  <VPFlyout
    v-if="localeLinks.length && currentLang.label"
    class="VPNavBarTranslations"
    :button="`<span class='mdi mdi-earth'></span> ${currentLang.changeLang}`"
    :label="theme.langMenuLabel || 'Change language'"
  >
    <div class="items">
      <p class="title">{{ currentLang.label }}</p>

      <template v-for="locale in localeLinks" :key="locale.link">
        <VPMenuLink :item="locale" />
      </template>
    </div>
  </VPFlyout>
</template>

<style scoped>
.VPNavBarTranslations {
  display: none;
}

@media (min-width: 1280px) {
  .VPNavBarTranslations {
    display: flex;
    align-items: center;
  }
}

.title {
  padding: 0 24px 0 12px;
  line-height: 32px;
  font-size: 14px;
  font-weight: 700;
  color: var(--vp-c-text-1);
}
</style>
