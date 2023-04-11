<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { downloadLearnware } from '@/utils'

const route = useRoute()
const router = useRouter()

const learnwareId = ref('')
const downloading = ref(false)

function getLearnwareDetailById(id) {
  return {
    id: id,
    name: 'Learnware 2023',
    dataType: 'Audio',
    taskType: 'Classification',
    deviceType: 'CPU',
    tagList: ['Nature', 'Business'],
    description: 'This is the description of Learnware 2023.'
  }
}

const learnware = computed(() => {
  return getLearnwareDetailById(learnwareId.value)
})

onMounted(() => {
  const _id = route.query.id
  learnwareId.value = _id
})
</script>

<template>
  <v-container class="md:flex max-w-1500px">
    <v-btn class="md:mx-3 <md:my-3" icon="mdi-arrow-left" @click="() => router.go(-1)" size="50" />
    <v-card v-if="learnware" class="p-2 w-1/1">
      <div class="flex justify-between">
        <v-card-title class="text-h4 !md:text-3xl !text-xl">
          {{ learnware.name }}
        </v-card-title>

        <v-card-actions>
          <v-btn icon="mdi-download" @click="() => downloadLearnware(learnware.id)" />
        </v-card-actions>
      </div>

      <v-card-subtitle>
        {{ learnware.id }}
      </v-card-subtitle>

      <v-card-text class="md:(text-xl !leading-7) text-sm">
        <div>Data type: {{ learnware.dataType }}</div>
        <div>Task type: {{ learnware.taskType }}</div>
        <div>Device type: {{ learnware.deviceType }}</div>
        <div>Tags: {{ learnware.tagList.join(', ') }}</div>
      </v-card-text>

      <v-card-text class="md:(text-xl !leading-7) text-sm">
        Description: {{ learnware.description }}
      </v-card-text>
    </v-card>
    <v-overlay class="flex justify-center items-center" v-model="downloading">
      <v-progress-circular size="80" width="8" indeterminate />
    </v-overlay>
  </v-container>
</template>