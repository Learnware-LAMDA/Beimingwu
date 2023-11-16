<script setup lang="ts">
import { onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { logout } from "../request/auth";

const store = useStore();

const router = useRouter();

onMounted(() => {
  logout()
    .then((res) => {
      if (res.code === 0) {
        localStorage.removeItem("token");
        return res;
      }
      throw new Error("Logout failed");
    })
    .catch((err) => {
      store.commit("setShowGlobalError", true);
      store.commit("setGlobalErrorMsg", err.message);
    })
    .finally(() => {
      store.dispatch("logout");
      router.push("/");
    });
});
</script>

<template>
  <div />
</template>
