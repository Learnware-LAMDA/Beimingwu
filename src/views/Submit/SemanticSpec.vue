<script setup>
import { ref, watch } from 'vue'
import DataType from './SemanticSpec/DataType.vue'
import TaskType from './SemanticSpec/TaskType.vue'
import RequirementType from './SemanticSpec/HardwareType.vue'
import TagList from './SemanticSpec/TagList.vue'

const dataType = ref('')
const taskType = ref('')
const requirementType = ref('')

watch(
  () => dataType.value,
  (newValue) => {
    console.log(newValue)
  }
)
</script>

<template>
  <div class="semantic-spec">
    <data-type v-model:value="dataType"/>
    <task-type v-model:value="taskType"/>
    <requirement-type v-model:value="requirementType"/>
    <tag-list />
  </div>
</template>

<style scoped lang="scss">
.semantic-spec {
}
</style>