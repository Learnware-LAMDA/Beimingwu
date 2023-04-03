<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Router from '@/router/index.js'
import Drawer from './components/Drawer.vue'
import AppBar from './components/AppBar.vue'

const drawerOpen = ref(false)

const route = useRoute()

watch(() => route.path, () => {
  drawerOpen.value = false
  console.log(route.path)
  console.log(route.name)
  console.log(route)
})
</script>

<template>
  <v-app>
    <app-bar v-model:drawerOpen="drawerOpen" :routes="Router.getRoutes()"></app-bar>

    <drawer v-model:drawerOpen="drawerOpen" :routes="Router.getRoutes()"></drawer>

    <v-main class="bg-gray-100">
      <router-view v-slot="{ Component, route }">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="route.paty" />
        </transition>
      </router-view>
    </v-main>
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