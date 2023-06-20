<script setup>
import { onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();

const router = useRouter();

onMounted(() => {
  fetch('/api/auth/logout', {
    method: 'POST',
  })
    .then((res) => {
      if (res.status === 200) {
        return res;
      }
      throw new Error('Network error');
    })
    .then((res) => res.json())
    .then((res) => {
      if (res.code === 0) {
        return res;
      }
      throw new Error('Logout failed');
    })
    .then(() => {
      store.commit('setLoggedIn', false);
      router.push('/');
    })
    .catch((err) => {
      store.commit('setShowGlobalError', true);
      store.commit('setGlobalErrorMsg', err.message);
      store.commit('setLoggedIn', false);
      router.push('/');
    });
});
</script>

<template>
    <div></div>
</template>
