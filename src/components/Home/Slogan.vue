<script setup>
import BigTitle from '@/components/Public/BigTitle.vue'
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const ratio = ref(0)

const scroller = ref(null)
const placeholder = ref(null)

onMounted(() => {
  nextTick(() => {
    placeholder.clientHeight = scroller.clientHeight + window.innerHeight / 2
    window.addEventListener('scroll', () => {
      ratio.value = window.scrollY / window.innerHeight * 2
      document.documentElement.style.setProperty('--vh', `${window.scrollY / window.innerHeight * 5 + 1}`)
    })
  })
})
</script>

<template>
  <div ref="scroller" class="top-0 left-0 right-0 z-index-100 overflow-hidden" :class="ratio <= 1 ? ['fixed'] : ['mt-50vh']">
    <div class="xl:py-30
                lg:py-25
                <lg:py-10
                text-center bg-primary text-white">
      <big-title>
        <h1>Small models do</h1>
        <h1 class="py-5" style="position: relative; z-index: 1000; transform: scale(var(--vh))"><span class="text-1.7em">Big</span></h1>
      </big-title>
      <div class="mx-10 white-space-pre-wrap
                        lg:text-2xl
                        sm:text-lg">
        <div class="mt-6">
          Learnware systematically reuses small models to do things that may even be beyond their original
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
  </div>
  <div ref="placeholder" v-if="ratio <= 1" class="h-150vh"></div>
</template>