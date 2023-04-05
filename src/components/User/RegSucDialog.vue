<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const emit = defineEmits(['close'])

const router = useRouter()

const start = ref(false)
const dialog = ref(true)

onMounted(() => {
  nextTick(() => {
    start.value = true
  })
})
</script>

<template>
  <v-dialog v-model="dialog">
    <v-sheet elevation="12" max-width="600" rounded="lg" width="100%" class="pa-4 text-center mx-auto">
      <svg class="m-auto w-120px h-120px" viewBox="0 0 200 200">
        <circle style="fill: rgb(var(--v-theme-success))" cx="100" cy="100" r="80" />
        <path d="M50 100 L90 134 L152 64" stroke="white" stroke-width="16" fill="none" stroke-dasharray="146"
          stroke-dashoffset="146" class="transition-all duration-800" :class="start ? ['offset-animate'] : null">
        </path>
      </svg>

      <h2 class="text-h5 mt-6 mb-8">You registered successfully</h2>

      <div class="text-end">
        <v-btn class="text-none mr-3" color="primary" rounded variant="flat" @click="router.push('/login')">
          Login now
        </v-btn>
        <v-btn class="text-none" color="primary" rounded variant="outlined" width="90" @click="router.go()">
          Close
        </v-btn>
      </div>
    </v-sheet>
  </v-dialog>
</template>

<style scoped lang="scss">
.offset-animate {
  stroke-dashoffset: 0;
}
</style>