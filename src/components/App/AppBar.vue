<script setup>
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import lamdaLogo from "/logo.svg";

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
  <v-app-bar app flat class="bg-white border-b-1">
    <div class="flex justify-start max-w-1500px w-md-1/1 m-auto md:px-5">
      <v-app-bar-nav-icon
        v-if="['xs', 'sm'].includes(display.name.value)"
        @click="() => emit('update:drawerOpen', !drawerOpen)"
      ></v-app-bar-nav-icon>
      <v-toolbar-items class="cursor-pointer" @click="() => router.push('/')">
        <v-img contain width="180" :src="lamdaLogo"></v-img>
      </v-toolbar-items>
      <v-spacer></v-spacer>

      <v-toolbar-items v-if="!['xs', 'sm'].includes(display.name.value)">
        <v-btn
          v-for="route in filteredRoutes"
          :key="route.name"
          class="mr-2 text-body-2 rounded"
          :variant="route.meta.variant"
          :class="route.meta.class"
          @click="() => router.push(route.path)"
        >
          <v-icon class="mr-1" :icon="route.meta.icon"></v-icon>
          {{ route.meta.name || route.name }}
        </v-btn>
      </v-toolbar-items>
    </div>
  </v-app-bar>
</template>
