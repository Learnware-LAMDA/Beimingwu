<script setup>
import { useStore } from "vuex";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import "animate.css";

const router = useRouter();

const store = useStore();

const animateClass = ref([]);

onMounted(() => {
  animateClass.value = ["animate__animated", "animate__tada"];
});
</script>

<template>
  <div class="slogan-container bg-primary">
    <div class="xl:text-8xl lg:text-7xl md:text-6xl sm:text-5xl text-2.75rem font-700">
      <div v-if="store.getters.getLoggedIn">
        <h1>Hello, dear</h1>
        <h1 class="py-5" :class="animateClass">
          <span class="sm:text-1.7em text-1.4em">Administrator</span>
        </h1>
      </div>
      <div v-else>
        <h1>Please login</h1>
        <h1 class="py-5"><span class="text-1.7em">First</span></h1>
      </div>
    </div>
    <v-btn v-if="!store.getters.getLoggedIn" variant="outlined" @click="router.push('/login')"
      >Login</v-btn
    >
  </div>
</template>

<style scoped lang="scss">
.slogan-container {
  @apply flex flex-col justify-center items-center w-1/1 h-1/1 xl:py-30 lg:py-25 <lg:py-10 text-center;
}
</style>
