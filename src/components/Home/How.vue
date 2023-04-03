<script setup>
import { computed } from 'vue';
import { useDisplay } from 'vuetify'
import process from '/process.png'

const display = useDisplay()

const greaterThanMd = computed(() => ['lg', 'xl'].includes(display.name.value))

const classGreaterThanMd = ['elevation-10']
</script>

<template>
  <div class="max-w-1200px w-1/1 m-auto lg:py-20 md:py-13 sm:py-10 xs:py-10">
    <div class="xl:(text-6xl mb-16)
                lg:(text-5xl mb-13)
                md:(text-4xl mb-10)
                <md:(text-3xl mb-10)
                text-3xl
                font-700
                text-center">
      How learnware works?
    </div>
    <!--<v-responsive class="bg-gray-200 rounded-xl" :aspect-ratio="16/9">

    </v-responsive>-->
    <v-img class="px-5" :class="greaterThanMd ? classGreaterThanMd : null" contain width="100%" :src="process" />
  </div>
</template>