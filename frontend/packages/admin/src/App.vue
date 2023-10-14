<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useStore } from "vuex";
import { useI18n } from "vue-i18n";
import Router from "./router";
import NavDrawer from "@main/components/App/NavDrawer.vue";
import AppBar from "@main/components/App/AppBar.vue";
import { Route } from "types";

const store = useStore();

const { t } = useI18n();

const drawerOpen = ref(false);
const showGlobalError = ref(store.getters.getShowGlobalError);

const initKeepAliveIncludes: string[] = Router.getRoutes()
  .filter((route) => route.meta.keepAlive)
  .map((route) => route.name as string);
const keepAliveIncludes = ref<string[]>([...initKeepAliveIncludes]);

const routes = computed<Route.Route[]>(() =>
  Router.options.routes.map((route) => {
    if (route.children) {
      route.children.forEach((child) => {
        child.meta = {
          ...child.meta,
          title: t(`Page.${route.name?.toString()}.${child.name?.toString()}`),
        };
        route.meta = {
          ...route.meta,
          title: t(`Page.${route.name?.toString()}.${route.name?.toString()}`),
        };
      });
    } else {
      route.meta = {
        ...route.meta,
        title: t(`Page.${route.name?.toString()}`),
      };
    }
    return route as Route.Route;
  }),
);

watch(
  () => store.getters.getLoggedIn,
  () => {
    keepAliveIncludes.value = [];
    setTimeout(() => {
      keepAliveIncludes.value = [...initKeepAliveIncludes];
    });
  },
);
watch(
  () => store.getters.getIsEditing,
  (editing) => {
    if (editing) {
      keepAliveIncludes.value = [...keepAliveIncludes.value.filter((route) => route !== "Submit")];
    } else {
      keepAliveIncludes.value = [
        ...keepAliveIncludes.value.filter((route) => route !== "Submit"),
        "Submit",
      ];
    }
  },
);
watch(
  () => store.getters.getShowGlobalError,
  (val) => {
    showGlobalError.value = val;
  },
);
watch(
  () => showGlobalError.value,
  (val) => store.commit("setShowGlobalError", val),
);
</script>

<template>
  <v-app>
    <app-bar v-model:drawerOpen="drawerOpen" :routes="routes"></app-bar>

    <nav-drawer v-model:drawerOpen="drawerOpen" :routes="routes"></nav-drawer>

    <v-main class="bg-gray-100 bg-opacity-50">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <keep-alive :include="keepAliveIncludes">
            <component :is="Component" />
          </keep-alive>
        </transition>
      </router-view>
    </v-main>

    <v-snackbar v-model="showGlobalError" :timeout="2000">
      {{ store.getters.getGlobalErrorMsg }}
      <template #actions>
        <v-btn color="blue" variant="text" @click="store.commit('setShowGlobalError', false)">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<style scoped>
.fade-enter-active {
  transition: opacity 1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
