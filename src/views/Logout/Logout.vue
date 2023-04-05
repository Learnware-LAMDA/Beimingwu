<script setup>
import { onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()

const router = useRouter()

onMounted(() => {
    fetch('/api/auth/logout', {
        method: 'POST'
    }).then(() => {
        store.commit('setLoggedIn', false)
        router.push('/')
    })
})
</script>

<template>
    <div></div>
</template>