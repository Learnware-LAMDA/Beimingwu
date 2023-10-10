<script setup lang="ts">
import { computed } from "vue";
import { useStore } from "vuex";
import { useDisplay } from "vuetify";

const display = useDisplay();

const emit = defineEmits(["update:drawerOpen"]);

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

const drawer = computed({
  get: () => props.drawerOpen && ["xs", "sm"].includes(display.name.value),
  set: (value) => emit("update:drawerOpen", value),
});

const store = useStore();

interface Route {
  name: string;
  path: string;
  meta: {
    showInNavBar: boolean;
    hideWhenLoggedIn: boolean;
    requiredLogin: boolean;
    icon: string;
    title: string;
  };
  children?: Route[];
  parent?: Route;
}

const filteredRoutes = computed(() => {
  function filter(route: Route): boolean {
    if (route.meta.showInNavBar) {
      if (route.meta.hideWhenLoggedIn && store.getters.getLoggedIn) {
        return false;
      }
      if (!route.meta.requiredLogin) {
        return true;
      }
      if (store.getters.getLoggedIn) {
        return true;
      }
    }
  }

  const routes: Route[] = [];
  props.routes.forEach((route) => {
    if (route.children) {
      route.children.forEach((child) => {
        child.parent = route;
        filter(child) && routes.push(child);
      });
    } else {
      filter(route) && routes.push(route);
    }
  });
  return routes;
});
</script>

<template>
  <v-navigation-drawer v-model="drawer" app clipped>
    <!--v-list navigation from router-->
    <v-list>
      <h1 class="ma-4">Pages</h1>
      <v-list-item
        v-for="(route, i) in filteredRoutes"
        :key="i"
        :value="route.name"
        color="primary"
        variant="plain"
        :to="route.path"
        @click="drawer = false"
      >
        <template #prepend>
          <v-icon
            v-if="route.meta.icon && route.meta.icon.startsWith('mdi-')"
            :icon="route.meta.icon"
          />
          <span v-if="route.meta.icon && !route.meta.icon.startsWith('mdi-')" class="v-icon">
            {{ route.meta.icon }}
          </span>
        </template>
        <v-list-item-title>
          {{ route.meta.title }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
