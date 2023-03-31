<script setup>
import { ref, computed } from 'vue'
import { useDisplay } from 'vuetify'

const display = useDisplay()

const smallerThanMd = computed(() => ['md', 'sm', 'xs'].includes(display.name.value))

const cardHoverClass = computed(() => {

})

const iconSize = computed(() => {
  switch (display.name.value) {
    case 'xs':
      return 'x-large'
    case 'sm':
      return 'large'
    case 'md':
      return 'x-large'
    case 'lg':
      return 'xx-large'
    case 'xl':
      return 37
  }
})

const reasons = ref([
  {
    icon: 'mdi-chart-scatter-plot',
    title: 'Lack of training data',
    content: 'Strong machine learning models can be attained even for tasks with small data, because the models are built upon well-performed learnwares, and only a small amount of data are needed for adaptation or refinement for most cases.'
  },
  {
    icon: 'mdi-hammer-wrench',
    title: 'Lack of training skills',
    content: 'Strong machine learning models can be attained even for ordinary users with little training skills, because the users can get help from well-performed learnwares rather than building a model from scratch by themselves.'
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
  <v-container class="relative max-w-1600px w-1/1 md:pt-20 sm:pt-15 xs:pt-10 pt-10">
    <v-row>
      <v-col>
        <div class="xl:(text-6xl my-10)
                    lg:(text-5xl my-7)
                    md:(text-4xl my-5)
                    <md:(text-3xl my-5)
                    text-3xl
                    font-700
                    text-center">
          Why you need learnware?
          </div>
        </v-col>
      </v-row>
    <v-row>
      <v-col
        v-for="reason in reasons"
        :key="reason.title"
        cols="12"
        lg="3"
        md="6"
      >
        <v-hover v-slot="{ isHovering, props }">
          <v-card
            flat
            class="relative fill-height p-4 transition-all duration-300 ease-in-out transform"
            :class="{ 'elevation-20': isHovering && !smallerThanMd, 'elevation-8': !isHovering && !smallerThanMd, 'bg-primary': isHovering, 'scale-105': isHovering && !smallerThanMd }"
            v-bind="props"
          >
            <v-card-title
              class="xl:text-2xl
                    lg:text-xl
                    md:text-xl
                    text-lg
                    font-300"
            >
              <v-icon class="mr-3" :size="iconSize">{{ reason.icon }}</v-icon>
              {{ reason.title }}
            </v-card-title>
            <v-card-text
              class="xl:text-md
                     lg:text-md
                     md:text-sm
                     text-sm !leading-5"
            >
              {{ reason.content }}
            </v-card-text>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
  </v-container>
</template>