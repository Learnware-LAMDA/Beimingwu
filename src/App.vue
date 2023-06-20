<script setup>
import {
  ref, computed, watch, onMounted,
} from 'vue';
import { useStore } from 'vuex';
import Router from '@/router/index.js';
import Drawer from '@/components/App/Drawer.vue';
import AppBar from '@/components/App/AppBar.vue';

const store = useStore();

const drawerOpen = ref(false);
const showGlobalError = ref(store.getters.getShowGlobalError);

const keepAliveIncludes = ref([]);
const _keepAliveIncludes = computed(() => Router.getRoutes().filter((route) => route.meta.keepAlive).map((route) => route.name));

watch(
  () => store.getters.getLoggedIn,
  () => {
    keepAliveIncludes.value = [];
    setTimeout(() => {
      keepAliveIncludes.value = [..._keepAliveIncludes.value];
    });
  },
);
watch(
  () => store.getters.getShowGlobalError,
  (val) => showGlobalError.value = val,
);
watch(
  () => showGlobalError.value,
  (val) => store.commit('setShowGlobalError', val),
);

onMounted(() => {
  keepAliveIncludes.value = [..._keepAliveIncludes.value];
});
</script>

<template>
  <v-app>
    <app-bar v-model:drawerOpen="drawerOpen" :routes="Router.getRoutes()"></app-bar>

    <drawer v-model:drawerOpen="drawerOpen" :routes="Router.getRoutes()"></drawer>

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
      <template v-slot:actions>
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
