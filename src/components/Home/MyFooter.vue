<script setup>
const links = [
  { icon: "mdi-information", name: "About", path: "https://www.lamda.nju.edu.cn" },
  { icon: "mdi-github", name: "GitHub", path: "https://github.com/lamda-nju" },
  { icon: "mdi-email", name: "Contact Us", path: "mailto:bm-support@lamda.nju.edu.cn" },
];
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
        <v-tooltip activator="parent" location="top"> Right click to copy</v-tooltip>
      </v-btn>
      <v-col class="text-center mt-4" cols="12">
        &copy; {{ new Date().getFullYear() }} <strong>LAMDA</strong>. All rights reserved.
      </v-col>
    </v-row>
  </v-footer>
</template>
