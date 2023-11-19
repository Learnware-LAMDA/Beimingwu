<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const links = computed(() => [
  {
    icon: "mdi-information",
    name: t("Home.Footer.About"),
    path: "https://www.lamda.nju.edu.cn",
    tooltips: "",
  },
  {
    icon: "mdi-github",
    name: t("Home.Footer.Github"),
    path: "https://github.com/Learnware-LAMDA",
    tooltips: "",
  },
  {
    icon: "mdi-email",
    name: t("Home.Footer.ContactUs"),
    path: "mailto:bmwu-support@lamda.nju.edu.cn",
    tooltips: t("Home.Footer.RightClickToCopy"),
  },
]);
</script>

<template>
  <v-footer
    color="grey-lighten-3"
    class="flex flex-col items-center justify-center"
  >
    <div>
      <v-btn
        v-for="link in links"
        :key="link"
        :href="link.path"
        target="_blank"
        class="mx-2"
        variant="text"
        rounded="xl"
      >
        <v-icon class="mr-1">
          {{ link.icon }}
        </v-icon>
        {{ link.name }}
        <v-tooltip
          v-if="link.tooltips"
          activator="parent"
          location="top"
        >
          {{ link.tooltips }}
        </v-tooltip>
      </v-btn>
    </div>
    <div
      class="mt-4 text-center"
      cols="12"
    >
      &copy; {{ new Date().getFullYear() }} <strong>LAMDA</strong>
      {{ t("Home.Footer.AllRightsReserved") }}
    </div>
    <!--ICP-->
    <div
      class="mt-4 text-center"
      cols="12"
    >
      <a
        :href="`http://www.beian.miit.gov.cn/`"
        target="_blank"
        rel="noopener noreferrer"
      >
        苏ICP备2021003372号-9
      </a>
    </div>
  </v-footer>
</template>
