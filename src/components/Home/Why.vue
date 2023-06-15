<script setup>
import { ref, computed } from 'vue'
import { useDisplay } from 'vuetify'

const display = useDisplay()

const smallerThanMd = computed(() => ['md', 'sm', 'xs'].includes(display.name.value))

const iconSize = computed(() => {
    
      return 80
})

const reasons = ref([
  {
    icon: 'mdi-chart-scatter-plot',
    title: 'Lack of training data/skills',
    content: 'Strong machine learning models can be attained even for ordinary users with little training skills or small data, because the users can adapte or refine well-performed learnwares rather than building a model from scratch by themselves.'
  },
  {
    icon: 'mdi-all-inclusive-box',
    title: 'Continual learning',
    content: 'The learnware market naturally realizes continual and lifelong learning, because with the constant submissions of well-performed learnwares trained from diverse tasks, the knowledge held in the learnware market is being continually enriched.'
  },
  {
    icon: 'mdi-head-snowflake',
    title: 'Catastrophic forgetting',
    content: 'A learnware will always be accommodated in the learnware market once it is accepted, unless every aspect of its function can be replaced by other learnwares. Thus, the old knowledge in the learnware market is always held. Nothing to be forgotten.'
  },
  {
    icon: 'mdi-eye-lock',
    title: 'Data privacy/proprietary',
    content: 'The developers only submit their models without sharing their own data, and thus, the data privacy/proprietary can be well preserved. Although one could not deny the possibility of reverse engineering the models, the risk would be too small compared with many other privacy-preserving solutions.'
  }
])
</script>

<template>
  <div class="mx-auto md:pb-30 <md:pb-20 md:px-10 max-w-1200px w-1/1">
    <div class="<md:px-5">
      <div class="xl:(text-5xl my-10) lg:(text-4xl my-7) md:(text-3xl my-5) <md:(text-4xl my-5)">
        Why do you need learnware?
      </div>
      <p class="text-gray-500">
        There are complaints about current machine learning techniques such as the requirement of a huge amount of training data and proficient training skills, the difficulty of continual learning, the risk of catastrophic forgetting, the leaking of data privacy/proprietary, etc.
      </p>
    </div>
    <div class="mt-8 grid sm:grid-cols-2 sm:gap-5 gap-2">
      <div v-for="reason in reasons" :key="reason.title">
        <v-hover v-slot="{ isHovering, props }">
          <v-card flat class="relative fill-height p-4 transition-all duration-300 ease-in-out transform"
            :class="{ 'elevation-20': isHovering && !smallerThanMd, 'bg-primary': isHovering, 'scale-105': isHovering && !smallerThanMd }"
            v-bind="props">
            <v-card-title class="my-2 text-center">
              <v-icon :size="iconSize">{{ reason.icon }}</v-icon>
            </v-card-title>
            <v-card-title class="mb-4 xl:text-2xl
                          lg:text-xl
                          md:text-xl
                          text-lg
                          font-600 text-center">
              {{ reason.title }}
            </v-card-title>
            <v-card-text class="xl:text-md
                          lg:text-md
                          md:text-sm
                          text-sm !leading-5">
              {{ reason.content }}
            </v-card-text>
          </v-card>
        </v-hover>
      </div>
    </div>
  </div>
</template>