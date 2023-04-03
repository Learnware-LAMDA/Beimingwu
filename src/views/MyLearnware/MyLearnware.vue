<script setup>
import LearnwareList from '@/views/Search/LearnwareList.vue'

const learnwareItems = Array(3).fill(0).map((_, i) => {
  const allDataType = ['Audio', 'Video', 'Text', 'Image', 'Table']
  const allTaskType = ['Classification', 'Clustering', 'Detection', 'Extraction', 'Generation', 'Regression', 'Segmentation', 'Ranking']
  const allHardwareType = ['CPU', 'GPU']
  const allTagList = ['Business', 'Financial', 'Health', 'Politics', 'Computer', 'Internet', 'Traffic', 'Nature', 'Fashion', 'Industry', 'Agriculture', 'Education']

  return {
    id: Array(32).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
    title: `Learnware ${i + 1}`,
    description: `This is the description of learnware ${i + 1}`,
    dataType: allDataType[Math.floor(Math.random() * allDataType.length)],
    taskType: allTaskType[Math.floor(Math.random() * allTaskType.length)],
    hardwareType: allHardwareType[Math.floor(Math.random() * allHardwareType.length)],
    tagList: Array.from(new Set(Array(Math.ceil(Math.random() * 5)).fill(0).map(() => allTagList[Math.floor(Math.random() * allTagList.length)]))),
  }
})
</script>

<template>
  <div class="flex flex-col h-1/1 justify-start items-center">
    <learnware-list class="w-1/1 max-w-900px" :items="learnwareItems" :cols="1" :show-actions="true" />
  </div>
</template>