<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import learnwareLogo from "/logo.svg?url";
import type { Route } from "@beiming-system/types/route";

export interface Props {
  drawerOpen: boolean;
  routes: Route[];
}

const emit = defineEmits(["update:drawerOpen"]);
const router = useRouter();

const props = defineProps<Props>();

const display = useDisplay();

const store = useStore();

function routeFilter(route: Route): boolean {
  if (route.meta.showInNavBar) {
    if (route.meta.hideWhenLoggedIn && store.getters.getLoggedIn) {
      return false;
    }
    if (!route.meta.requiredLogin) {
      return true;
    }
    return store.getters.getLoggedIn;
  }
  return false;
}

const filteredRoutes = computed<Route[]>(() =>
  props.routes
    .map((route: Route) => {
      if (route.children) {
        return {
          ...route,
          children: route.children.filter(routeFilter),
        };
      }
      return routeFilter(route) ? route : null;
    })
    .filter((route) => route) as Route[],
);
</script>

<template>
  <v-app-bar app flat class="bg-white border-b-1">
    <div class="prepend">
      <v-app-bar-nav-icon
        v-if="['xs', 'sm'].includes(display.name.value)"
        @click="() => emit('update:drawerOpen', !drawerOpen)"
      ></v-app-bar-nav-icon>
      <div class="logo" @click="() => router.push('/')">
        <img class="logo-img" :src="learnwareLogo" />
      </div>
    </div>

    <template #append>
      <v-toolbar-items v-if="!['xs', 'sm'].includes(display.name.value)" class="my-3">
        <router-link
          v-for="route in filteredRoutes"
          :key="route.name"
          :to="route.children ? '' : route.path"
        >
          <v-menu v-if="route.children" open-on-hover>
            <template #activator="{ props: menuProps }">
              <v-btn
                class="mr-2 h-100 text-body-2 rounded"
                :variant="route.meta.variant"
                :class="route.meta.class"
                v-bind="menuProps"
              >
                <v-icon class="mr-1" :icon="route.meta.icon"></v-icon>
                {{ route.meta.title }}
                <v-icon>mdi-chevron-down</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="child in route.children"
                :key="child.name"
                class="text-body-2 font-weight-bold"
                :to="child.path"
              >
                <v-icon
                  v-if="child.meta.icon && child.meta.icon.startsWith('mdi-')"
                  class="mr-1"
                  :icon="child.meta.icon"
                ></v-icon>
                <span v-if="child.meta.icon && !child.meta.icon.startsWith('mdi-')">{{
                  child.meta.icon
                }}</span>
                {{ child.meta.title }}
              </v-list-item>
            </v-list>
          </v-menu>
          <v-btn
            v-else
            class="mr-2 h-100 text-body-2 rounded"
            :variant="route.meta.variant"
            :class="route.meta.class"
          >
            <v-icon class="mr-1" :icon="route.meta.icon"></v-icon>
            {{ route.meta.title }}
          </v-btn>
        </router-link>
      </v-toolbar-items>
    </template>
  </v-app-bar>
</template>

<style scoped lang="scss">
.prepend {
  @apply flex items-center h-full p-4.5;
  .logo {
    @apply cursor-pointer h-full;
    .logo-img {
      @apply h-full;
    }
  }
}
</style>
