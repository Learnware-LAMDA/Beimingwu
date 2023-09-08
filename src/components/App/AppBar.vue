<script setup>
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import learnwareLogo from "/logo.svg?url";

const emit = defineEmits(["update:drawerOpen"]);
const router = useRouter();

const props = defineProps({
  drawerOpen: {
    type: Boolean,
    required: true,
  },
  routes: {
    type: Array,
    required: true,
  },
});

const display = useDisplay();

const store = useStore();

function routeFilter(route) {
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

const filteredRoutes = computed(() =>
  props.routes
    .map((route) => {
      if (route.children) {
        return {
          ...route,
          children: route.children.filter(routeFilter),
        };
      }
      return routeFilter(route) ? route : null;
    })
    .filter((route) => route),
);
</script>

<template>
  <v-app-bar app flat class="bg-white border-b-1">
    <template #prepend>
      <v-app-bar-nav-icon
        v-if="['xs', 'sm'].includes(display.name.value)"
        @click="() => emit('update:drawerOpen', !drawerOpen)"
      ></v-app-bar-nav-icon>
      <v-appbar-title class="cursor-pointer" @click="() => router.push('/')">
        <v-img contain width="180" :src="learnwareLogo"></v-img>
      </v-appbar-title>
    </template>

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
                class="mr-2 !h-1/1 text-body-2 rounded"
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
            class="mr-2 !h-1/1 text-body-2 rounded"
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
