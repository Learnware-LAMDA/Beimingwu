<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router'
import { useDisplay } from 'vuetify'
import Router from '../router/index.js'

const display = useDisplay()

const emit = defineEmits(['update:drawerOpen'])

const props = defineProps({
  drawerOpen: {
    type: Boolean,
    required: true
  }
})

const drawer = computed({
  get: () => props.drawerOpen && ['xs', 'sm'].includes(display.name.value),
  set: (value) => emit('update:drawerOpen', value)
})

const items = computed(() => {
  return Router.getRoutes().map(route => {
    return {
      text: route.name,
      path: route.path,
      icon: route.meta.icon
    }
  })
})

const router = useRouter()
</script>

<template>
  <v-navigation-drawer v-model="drawer" app clipped>
    <!--v-list navigation from router-->
    <v-list>
      <h1 class="ma-4">Pages</h1>

      <v-list-item v-for="(item, i) in items" :key="i" :value="item" active-color="primary" variant="plain"
        @click="() => router.push(item.path)">
        <template v-slot:prepend>
          <v-icon :icon="item.icon"></v-icon>
        </template>

        <v-list-item-title>{{ item.text }}</v-list-item-title>
      </v-list-item>
    </v-list>

  </v-navigation-drawer>
</template>