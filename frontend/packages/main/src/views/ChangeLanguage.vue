<script setup lang="ts">
import { onMounted } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";

const store = useStore();

const route = useRoute();

const router = useRouter();

onMounted(() => {
  store.commit("setLocale", route.path.split("/").slice(-1)[0]);
  router.go(-1);
});
</script>

<template>
  <div />
</template>
