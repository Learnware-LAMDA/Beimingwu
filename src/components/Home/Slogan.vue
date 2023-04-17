<script setup>
import BigTitle from '@/components/Public/BigTitle.vue'
import { ref, onMounted, nextTick, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const ratio = ref(0)

const scroller = ref(null)
const placeholder = ref(null)

function handleScroll() {
  ratio.value = window.scrollY / window.innerHeight * 2
  document.documentElement.style.setProperty('--scale', `${window.scrollY / window.innerHeight * 3 + 1}`)
}

onMounted(() => {
  nextTick(() => {
    placeholder.value.style.height = `${scroller.value.clientHeight + window.innerHeight / 2}px`

    window.addEventListener('scroll', handleScroll)
  })
})

onUnmounted(() => {
  document.documentElement.style.setProperty('--scale', '1')
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div class="d-sm-block d-none">
    <div ref="scroller" class="left-0 right-0 z-index-100 overflow-hidden" :class="ratio <= 1 ? ['fixed'] : null"
      :style="ratio > 1 ? { marginTop: `50vh` } : null">
      <div class="xl:py-30
                        lg:py-25
                        <lg:py-10
                        text-center bg-primary text-white">
        <big-title>
          <h1>Small models do</h1>
          <h1 class="py-5 transform" style="position: relative; z-index: 1000; transform: scale(var(--scale))"><span
              class="text-1.7em">Big</span></h1>
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
          <v-btn class="mx-3" variant="outlined" size="large" @click="router.push('/submit')">Be a developer</v-btn>
        </div>
      </div>
    </div>
    <div ref="placeholder" v-show="ratio <= 1"></div>
  </div>
  <div class="d-sm-none d-block">
    <div class="xl:py-30
                        lg:py-25
                        <lg:py-10
                        text-center bg-primary text-white">
      <big-title>
        <h1>Small models do</h1>
        <h1 class="py-5 transform"><span class="text-1.7em">Big</span></h1>
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
        <v-btn class="mx-3" variant="outlined" size="large" @click="router.push('/submit')">Be a developer</v-btn>
      </div>
    </div>
  </div>
</template>