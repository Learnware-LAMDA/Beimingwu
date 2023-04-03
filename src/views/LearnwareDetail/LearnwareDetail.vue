<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const learnwareId = ref('')

function getLearnwareDetailById(id) {
  return {
    id: id,
    name: 'Learnware 2023',
    dataType: 'Audio',
    taskType: 'Classification',
    hardwareType: 'CPU',
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
  <v-container class="max-w-800px">
    <v-card v-if="learnware" class="p-2">
      <div class="flex justify-between">
        <v-card-title class="text-h4">
          {{ learnware.name }}
        </v-card-title>
        
        <v-card-actions>
          <v-btn icon="download-circle"></v-btn>
        </v-card-actions>
      </div>

      <v-card-subtitle>
        {{ learnware.id }}
      </v-card-subtitle>
      
      <v-card-text class="text-xl !leading-7">
        <div>Data type: {{ learnware.dataType }}</div>
        <div>Task type: {{ learnware.taskType }}</div>
        <div>Hardware type: {{ learnware.hardwareType }}</div>
        <div>Tags: {{ learnware.tagList.join(', ') }}</div>
      </v-card-text>

      <v-card-text class="text-xl !leading-7">
        Description: {{ learnware.description }}
      </v-card-text>
    </v-card>
  </v-container>
</template>