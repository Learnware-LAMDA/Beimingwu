<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
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

const router = useRouter();

const store = useStore();

const filteredRoutes = computed(() =>
  props.routes.filter((route) => {
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
  }),
);
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
        @click="() => router.push(route.path)"
      >
        <template #prepend>
          <v-icon :icon="route.meta.icon"></v-icon>
        </template>
        <v-list-item-title>{{ route.name }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
