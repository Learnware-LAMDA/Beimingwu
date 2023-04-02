<script setup>
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import lamdaLogo from '/lamda.png'

const emit = defineEmits(['update:drawerOpen'])
const router = useRouter()

const props = defineProps({
    drawerOpen: {
        type: Boolean,
        required: true,
    },
    routes: {
        type: Array,
        required: true
    }
})

const display = useDisplay()

const store = useStore()

const filteredRoutes = computed(() => {
    return props.routes.filter(route => {
        if (route.meta.showInNavBar) {
            if (route.meta.hideWhenLoggedIn && store.getters.getLoggedIn) {
                return false
            }
            if (!route.meta.requiredLogin) {
                return true
            } else {
                return store.getters.getLoggedIn
            }
        }
    })
})
</script>

<template>
    <v-app-bar app flat class="bg-white">
        <div class="flex justify-start max-w-1200px w-md-1/1 m-auto md:px-5">
            <v-app-bar-nav-icon v-if="['xs', 'sm'].includes(display.name.value)"
                @click="() => emit('update:drawerOpen', !drawerOpen)"></v-app-bar-nav-icon>
            <v-toolbar-items class="cursor-pointer" @click="() => router.push('/')">
                <v-img contain width="80" :src="lamdaLogo"></v-img>
                <h1 class="ml-4 flex flex-column justify-center text-xl" v-if="!['xs', 'sm'].includes(display.name.value)">
                    Learnware Market
                </h1>
            </v-toolbar-items>
            <v-spacer></v-spacer>

            <v-toolbar-items v-if="!['xs', 'sm'].includes(display.name.value)">
                <v-btn v-for="route in filteredRoutes" :key="route.name" class="mr-2 text-body-2" @click="() => router.push(route.path)"
                    :variant="route.meta.variant" :class="route.meta.class">
                    {{ route.name }}
                </v-btn>
            </v-toolbar-items>
        </div>
    </v-app-bar>
</template>