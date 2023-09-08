<script setup>
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
    path: "https://github.com/lamda-nju",
    tooltips: "",
  },
  {
    icon: "mdi-email",
    name: t("Home.Footer.ContactUs"),
    path: "mailto:bm-support@lamda.nju.edu.cn",
    tooltips: t("Home.Footer.RightClickToCopy"),
  },
]);
</script>

<template>
  <v-footer color="grey-lighten-3" class="text-center">
    <v-row justify="center" no-gutters>
      <v-btn
        v-for="link in links"
        :key="link"
        :href="link.path"
        target="_blank"
        class="mx-2"
        variant="text"
        rounded="xl"
      >
        <v-icon class="mr-1">{{ link.icon }}</v-icon>
        {{ link.name }}
        <v-tooltip v-if="link.tooltips" activator="parent" location="top">
          {{ link.tooltips }}
        </v-tooltip>
      </v-btn>
      <v-col class="text-center mt-4" cols="12">
        &copy; {{ new Date().getFullYear() }} <strong>LAMDA</strong>
        {{ t("Home.Footer.AllRightsReserved") }}
      </v-col>
    </v-row>
  </v-footer>
</template>
