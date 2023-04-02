<script setup>
import { ref, computed, watch } from 'vue'
import DataType from '@/views/Submit/SemanticSpec/DataType.vue'
import TaskType from '@/views/Submit/SemanticSpec/TaskType.vue'
import HardwareType from '@/views/Submit/SemanticSpec/HardwareType.vue'
import FileUpload from '@/views/Submit/FileUpload.vue'

const dataType = ref('')
const taskType = ref('')
const hardwareType = ref('')
const files = ref([])

const filters = computed(() => ({
  dataType: dataType.value,
  taskType: taskType.value,
  hardwareType: hardwareType.value,
  files: files.value
}))

watch(
  () => filters.value,
  (newVal) => {
    console.log(newVal)
  }
)
</script>

<template>
  <div class="search-container">
    <div class="filter">
      <data-type :cols="3" :md="2" :sm="2" :xs="2" v-model:value="dataType" />
      <task-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="taskType" />
      <hardware-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="hardwareType" />
      <div class="h-30">
        Upload statistical specification
        <file-upload />
      </div>
    </div>
    <div class="content">
      <div v-for="i in 100" :key="i">
        content
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.search-container {
  @apply fixed md: flex mx-auto w-1/1 overflow-hidden;
  height: calc(100% - var(--v-layout-top));

  .filter {
    @apply p-2 md: h-1/1 h-300px md:w-150 w-1/1 overflow-y-scroll;

    * {
      @apply mt-2;
    }
  }

  .filter.hide {
    @apply h-0;
  }

  .content {
    @apply w-1/1 md: h-1/1 overflow-y-scroll;
    height: calc(100% - 300px)
  }
}
</style>