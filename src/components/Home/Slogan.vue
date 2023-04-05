<script setup>
import BigTitle from '@/components/Public/BigTitle.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <v-sheet>
    <div class="xl:py-30
                lg:py-25
                <lg:py-10
                text-center bg-primary text-white">
      <big-title>
        <h1>Small models do</h1>
        <h1 class="py-5"><span class="text-1.7em">Big</span></h1>
      </big-title>
      <div class="mx-10 white-space-pre-wrap
                        lg:text-2xl
                        sm:text-lg">
        <div class="mt-6">
          Learnware attempts to systematically reuse small models to do things that may even be beyond their original
          purposes, <br>and enables users not need to build their machine learning models from scratch.
        </div>
      </div>

      <div class="flex justify-center mt-12">
        <v-btn class="mx-3" size="large" @click="router.push('/search')">Try it out</v-btn>
        <v-btn
          class="mx-3"
          variant="outlined"
          size="large"
          @click="router.push('/submit')"
        >Be a developer</v-btn>
      </div>
    </div>
  </v-sheet>
</template>