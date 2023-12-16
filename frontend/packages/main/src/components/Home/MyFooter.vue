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
  {
    icon: "mdi-pencil-ruler",
    name: t("Home.Footer.UserAgreement"),
    click: (): void => {
      window.open(t("Url.Docs.UserAgreement"));
    },
    tooltips: "",
  },
  {
    icon: "mdi-home-lock",
    name: t("Home.Footer.PrivacyPolicy"),
    click: (): void => {
      window.open(t("Url.Docs.PrivacyPolicy"));
    },
    tooltips: "",
  },
]);

function buttonClick(func: (() => void) | undefined): void {
  if (func !== undefined) {
    func();
  }
}
</script>

<template>
  <v-footer class="flex flex-col items-center justify-center">
    <div class="text-center">
      <v-btn
        v-for="link in links"
        :key="link.name"
        :href="link.path === undefined ? undefined : link.path"
        target="_blank"
        class="sm:mx-2"
        variant="text"
        rounded="xl"
        @click="buttonClick(link.click)"
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
      class="mt-4 text-center dark:text-white"
      cols="12"
    >
      <a
        :href="`http://www.beian.miit.gov.cn/`"
        class="text-black dark:text-white"
        target="_blank"
        rel="noopener noreferrer"
      >
        苏ICP备2021003372号-9
      </a>
    </div>
  </v-footer>
</template>
