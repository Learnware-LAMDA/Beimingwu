<script lang="ts" setup>
import type { DefaultTheme } from "vitepress/theme";
import { useData } from "vitepress";
import { isActive } from "vitepress/dist/client/shared";
import VPLink from "vitepress/dist/client/theme-default/components/VPLink.vue";
import "@mdi/font/css/materialdesignicons.min.css";

defineProps<{
  item: DefaultTheme.NavItemWithLink;
}>();

const { page } = useData();
</script>

<template>
  <VPLink
    :class="{
      VPNavBarMenuLink: true,
      active: isActive(
        page.relativePath,
        item.activeMatch || item.link,
        !!item.activeMatch
      ),
    }"
    :href="item.link"
    :target="item.target"
    :rel="item.rel"
    tabindex="0"
  >
    <span :class="`mdi ${item.icon}`" style="margin-right: 0.2em"></span>
    <span v-html="item.text"></span>
  </VPLink>
</template>

<style scoped>
.VPNavBarMenuLink {
  display: flex;
  align-items: center;
  padding: 0 12px;
  line-height: calc(var(--vp-nav-height) * 3 / 5);
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  color: var(--vp-c-text-1);
  transition: color 0.25s;
}

.VPNavBarMenuLink.active {
  color: var(--vp-c-brand-1);
}

.VPNavBarMenuLink:hover {
  color: var(--vp-c-brand-1);
  background: var(--vp-c-gray-1);
}
</style>
