<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useStore } from "vuex";
import { useI18n } from "vue-i18n";
import Router from "./router";
import NavDrawer from "./components/App/NavDrawer.vue";
import AppBar from "./components/App/AppBar.vue";
import type { Route } from "@beiming-system/types/route";

const store = useStore();

const { t } = useI18n();

const drawerOpen = ref(false);
const showGlobalError = ref(store.getters.getShowGlobalError);

const initKeepAliveIncludes: string[] = Router.getRoutes()
  .filter((route) => route.meta.keepAlive)
  .map((route) => route.name as string);
const keepAliveIncludes = computed<string[]>(() => {
  let _keepAliveIncludes = [...initKeepAliveIncludes];
  if (store.getters.getLoggedIn) {
    _keepAliveIncludes = [];
  }
  if (store.getters.getIsEditing) {
    _keepAliveIncludes = [..._keepAliveIncludes.filter((route) => route !== "Submit")];
  } else {
    _keepAliveIncludes = [..._keepAliveIncludes.filter((route) => route !== "Submit"), "Submit"];
  }
  return _keepAliveIncludes;
});

const routes = computed<Route[]>(
  () =>
    Router.options.routes.map((route) => {
      if (route.children) {
        route.meta = {
          ...route.meta,
          title:
            route.name === "User" && store.getters.getLoggedIn
              ? store.getters.getUserName
              : t(`Page.${String(route.name)}.${String(route.name)}`),
        };
        route.children.forEach((child) => {
          child.meta = {
            ...child.meta,
            title: t(`Page.${String(route.name)}.${String(child.name)}`),
          };
        });
      } else {
        route.meta = {
          ...route.meta,
          title: t(`Page.${String(route.name)}`),
        };
      }
      return route;
    }) as Route[],
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
    <app-bar
      v-model="drawerOpen"
      :routes="routes"
    />

    <nav-drawer
      v-model="drawerOpen"
      :routes="routes"
    />

    <v-main class="bg-gray-100 bg-opacity-50">
      <router-view v-slot="{ Component }">
        <transition
          name="fade"
          mode="out-in"
        >
          <keep-alive :include="keepAliveIncludes">
            <component :is="Component" />
          </keep-alive>
        </transition>
      </router-view>
    </v-main>

    <v-snackbar
      v-model="showGlobalError"
      :timeout="2000"
    >
      {{ store.getters.getGlobalErrorMsg }}
      <template #actions>
        <v-btn
          color="blue"
          variant="text"
          @click="store.commit('setShowGlobalError', false)"
        >
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
