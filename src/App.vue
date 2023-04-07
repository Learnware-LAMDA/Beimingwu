<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import Router from '@/router/index.js'
import Drawer from '@/components/App/Drawer.vue'
import AppBar from '@/components/App/AppBar.vue'

const store = useStore()

const drawerOpen = ref(false)

const keepAliveIncludes = computed(() => {
  return Router.getRoutes().filter((route) => route.meta.keepAlive).map((route) => route.name)
})
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

    <v-snackbar
      v-model="store.showGlobalError"
      :timeout="3000"
    >
      {{ store.globalErrorMsg }}
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