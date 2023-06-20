<script setup>
import analogyImg from "../../assets/images/analogy.png";
</script>

<template>
  <div class="mx-auto md:py-30 <md:py-20 md:px-10 max-w-1200px w-1/1">
    <div class="<md:px-5">
      <div class="xl:(text-5xl my-10) lg:(text-4xl my-7) md:(text-3xl my-5) <md:(text-4xl my-5)">
        What is learnware?
      </div>
      <p class="text-gray-500">
        <!-- eslint-disable-next-line max-len -->
        A learnware is a well-performed trained machine learning model with a specification which
        enables it to be adequately identified to reuse according to the requirement of future users
        who know nothing about the learnware in advance.
      </p>
    </div>

    <div class="mt-10 sm:shadow-md">
      <v-img :src="analogyImg" />
    </div>
  </div>
</template>
