<script setup>
import { computed } from 'vue';
import { useDisplay } from 'vuetify'
import process from '/process.png'

const display = useDisplay()

const greaterThanMd = computed(() => ['lg', 'xl'].includes(display.name.value))

const classGreaterThanMd = ['elevation-10']
</script>

<template>
  <div class="max-w-1200px w-1/1 m-auto lg:py-20 md:py-13 sm:py-10 py-10">
    <div class="xl:(text-6xl mb-16)
                  lg:(text-5xl mb-13)
                  md:(text-4xl mb-10)
                  <md:(text-3xl mb-10)
                  text-3xl
                  text-center">
      How learnware works?
    </div>

    <v-responsive :class="greaterThanMd ? classGreaterThanMd : null" :aspect-ratio="96/55">
      <v-img contain width="100%" :src="process" />
    </v-responsive>
  </div>
</template>