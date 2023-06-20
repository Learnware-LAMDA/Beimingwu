<script setup>
import { useRouter } from "vue-router";
import BigTitle from "../Public/BigTitle.vue";

const router = useRouter();
</script>

<template>
  <div class="xl:py-35 lg:py-30 md:py-20 <md:py-10 text-center text-white gradient">
    <big-title>
      <h1>Small models do</h1>
      <h1 class="py-5 transform"><span class="text-1.7em">Big</span></h1>
    </big-title>
    <div class="md:mx-20 sm:mx-15 <sm:mx-9">
      <div
        class="mx-auto max-w-1200px white-space-pre-wrap lg:text-xl md:(text-1rem leading-6) sm:(text-0.9rem leading-5)"
      >
        <div class="mt-6 <sm:(text-0.9em leading-5)">
          <!-- eslint-disable-next-line max-len -->
          Learnware paradigm systematically reuses numerous various models to do things that may
          even be beyond their
          <!-- eslint-disable-next-line max-len -->
          original purposes, and enables users to easily identify and reuse helpful models, not need
          to build their models from scratch.
        </div>
      </div>
    </div>

    <div class="flex justify-center mt-12">
      <v-btn class="mx-3" size="large" @click="router.push('/search')">Try it out</v-btn>
      <v-btn class="mx-3" variant="outlined" size="large" @click="router.push('/submit')"
        >Be a developer</v-btn
      >
    </div>
  </div>
</template>

<style scoped>
.gradient {
  background: -webkit-linear-gradient(to right, #673ab7, #6200ee);
  background: linear-gradient(to right, #673ab7, #6200ee);
}
</style>
