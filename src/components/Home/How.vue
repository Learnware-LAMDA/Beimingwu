<script setup>
import process from '@/assets/images/process.svg';
</script>

<template>
  <div class="mx-auto md:pb-30 <md:pb-20 md:px-10 max-w-1200px w-1/1">
    <div class="<md:px-5">
      <div class="xl:(text-5xl my-10) lg:(text-4xl my-7) md:(text-3xl my-5) <md:(text-4xl my-5)">
        How does learnware work?
      </div>
      <p class="text-gray-500">
        There are three important entities: developers, users, and the market. The developers are usually machine learning
        experts who produce and want to share/sell their well-performed trained machine learning models. The users need
        machine learning services but usually have only limited data and lack machine learning knowledge and skills. The
        learnware market accepts/buys well-performed trained models from developers, accommodates them in the market, and
        provides/sells services to users via identifying and reusing learnwares to help users tackle their present tasks
      </p>
    </div>
    <v-responsive class="mt-10 sm:shadow-md border-1" :aspect-ratio="96 / 55">
      <v-img contain width="100%" :src="process" />
    </v-responsive>
  </div>
</template>
