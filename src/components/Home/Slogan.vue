<script setup>
import BigTitle from '@/components/Public/BigTitle.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="xl:py-30 lg:py-25 <lg:py-10 text-center text-white" style="background: #6200EE; background: -webkit-linear-gradient(to right, #673AB7, #6200EE); background: linear-gradient(to right, #673AB7, #6200EE);">
    <big-title>
      <h1>Small models do</h1>
      <h1 class="py-5 transform"><span class="text-1.7em">Big</span></h1>
    </big-title>
    <div class="mx-9 white-space-pre-wrap
                              lg:text-2xl
                              sm:text-lg">
      <div class="mt-6 <sm:(text-0.9em leading-5)">
        Learnware paradigm systematically reuses numerous various models to do things that may even be beyond their original purposes, <br>and enables users to easily identify and reuse helpful models, not need to build their models from scratch.
      </div>
    </div>

    <div class="flex justify-center mt-12">
      <v-btn class="mx-3" size="large" @click="router.push('/search')">Try it out</v-btn>
      <v-btn class="mx-3" variant="outlined" size="large" @click="router.push('/submit')">Be a developer</v-btn>
    </div>
  </div>
</template>