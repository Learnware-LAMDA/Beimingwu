<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { computedAsync } from "@vueuse/core";
import type { Route } from "@beiming-system/types/route";
import type { Language } from "@main/i18n";

export interface Props {
  modelValue: boolean;
  dark: boolean;
  routes: Route[];
  languages?: Language[];
}

const emit = defineEmits(["update:modelValue", "click:dark", "updateLanguage"]);
const router = useRouter();

const props = defineProps<Props>();

const display = useDisplay();

const store = useStore();

const logoSrc = computedAsync<string>(async () => {
  const { default: src } = display.smAndDown.value
    ? await import("/logo_no_text.svg?url")
    : await import("/logo.svg?url");
  return src;
});

function routeFilter(route: Route): boolean {
  if (route.meta.showInNavBar) {
    if (route.meta.hideWhenLoggedIn && store.getters.getLoggedIn) {
      return false;
    }
    if (!route.meta.requiredLogin || route.meta.showWhenNotLoggedIn) {
      return true;
    }
    return store.getters.getLoggedIn;
  }
  return false;
}

const filteredRoutes = computed<Route[]>(
  () =>
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
  <v-app-bar
    flat
    class="border-b"
  >
    <div class="prepend">
      <v-app-bar-nav-icon
        v-if="['xs', 'sm'].includes(display.name.value)"
        @click="() => emit('update:modelValue', !modelValue)"
      />
      <div
        class="logo"
        @click="() => router.push('/')"
      >
        <img
          class="logo-img"
          :src="logoSrc"
        />
      </div>
    </div>

    <template #append>
      <v-toolbar-items
        v-if="display.mdAndUp.value"
        class="my-3"
      >
        <template
          v-for="route in filteredRoutes"
          :key="route.name"
        >
          <v-list-item
            v-if="!route.children"
            class="rounded text-sm font-medium tracking-tight"
            :to="route.path"
          >
            <!-- route without children -->
            <v-icon
              class="mr-1"
              :icon="route.meta.icon"
            />
            {{ route.meta.title }}
          </v-list-item>

          <!-- route with children -->
          <v-menu
            v-else
            :open-on-hover="display.mdAndUp.value"
            :open-on-click="display.smAndDown.value"
          >
            <template #activator="{ props: menuProps }">
              <v-btn
                class="mr-2 h-full text-sm font-medium normal-case tracking-tight"
                :variant="route.meta.variant"
                :class="route.meta.class"
                rounded="md"
                v-bind="menuProps"
              >
                <v-icon
                  class="mr-1"
                  :icon="route.meta.icon"
                />
                {{ route.meta.title }}
                <v-icon>mdi-chevron-down</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="child in route.children"
                :key="child.name"
                class="text-sm font-medium tracking-tight"
                :to="child.path"
              >
                <v-icon
                  v-if="child.meta.icon && child.meta.icon.startsWith('mdi-')"
                  class="mr-1"
                  :icon="child.meta.icon"
                />
                <span v-if="child.meta.icon && !child.meta.icon.startsWith('mdi-')">{{
                  child.meta.icon
                }}</span>
                {{ child.meta.title }}
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-toolbar-items>

      <!-- language switcher -->
      <v-menu
        v-if="languages && languages.length > 0"
        :open-on-hover="display.mdAndUp.value"
        :open-on-click="display.smAndDown.value"
      >
        <template #activator="{ props: menuProps }">
          <v-btn
            class="mr-2 h-full text-sm font-medium normal-case tracking-tight"
            rounded="md"
            v-bind="menuProps"
          >
            <v-icon
              class="mr-1"
              icon="mdi-translate"
            />
            <v-icon>mdi-chevron-down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="language in languages"
            :key="language.name"
            class="text-sm font-medium tracking-tight"
            @click="() => emit('updateLanguage', language)"
          >
            {{ language.title }}
          </v-list-item>
        </v-list>
      </v-menu>

      <v-btn
        variant="flat"
        :icon="dark ? 'mdi-weather-night' : 'mdi-weather-sunny'"
        @click="() => emit('click:dark')"
      />
    </template>
  </v-app-bar>
</template>

<style scoped lang="scss">
.prepend {
  @apply flex h-full items-center p-[1.1rem];
  .logo {
    @apply h-full cursor-pointer;
    .logo-img {
      @apply h-full;
    }
  }
}
</style>
