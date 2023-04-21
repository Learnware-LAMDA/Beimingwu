<script setup>
import { ref, onMounted } from 'vue'
import { useDisplay } from 'vuetify'
import { useRoute, useRouter } from 'vue-router'
import { downloadLearnware } from '@/utils'

const route = useRoute()
const router = useRouter()

const display = useDisplay()

const learnware = ref(null)
const learnwareId = ref('')
const downloading = ref(false)
const loading = ref(false)

const showError = ref(false)
const errorMsg = ref('')
const errorTimer = ref(null)

function getLearnwareDetailById(id) {
  fetch('/api/engine/get_learnware_info?learnware_id=' + id, {
    method: 'GET',
  })
  .then((res) => {
      if (res.status === 200) {
        return res
      }
      throw new Error('Network error')
    })
    .then((res) => res.json())
    .then((res) => {
      switch (res.code) {
        case 0: {
          loading.value = false

          const learnwareInfo = res.data ? res.data.learnware_info : {}
          learnware.value =  {
            id: learnwareInfo.learnware_id,
            name: learnwareInfo.semantic_specification.Name.Values,
            description: learnwareInfo.semantic_specification.Description.Values,
            dataType: learnwareInfo.semantic_specification.Data.Values[0],
            taskType: learnwareInfo.semantic_specification.Task.Values[0],
            libraryType: learnwareInfo.semantic_specification.Library.Values[0],
            tagList: learnwareInfo.semantic_specification.Scenario.Values
          }
          return 
        }
        default: {
          throw new Error(res.msg)
        }
      }
    })
    .catch((err) => {
      console.error(err)
      loading.value = false
      showError.value = true
      errorMsg.value = err.message
    })
}

onMounted(() => {
  const _id = route.query.id
  learnwareId.value = _id
  getLearnwareDetailById(learnwareId.value)
})
</script>

<template>
  <v-container class="md:flex max-w-1500px <sm:p-1">
    <v-scroll-y-transition class="fixed left-0 right-0 z-index-10" style="top: var(--v-layout-top)">
      <v-card-actions v-if="showError">
        <v-alert class="w-1/1 max-w-900px mx-auto" closable :text="errorMsg" type="error" @click:close="showError = false" />
      </v-card-actions>
    </v-scroll-y-transition>
    
    <v-btn v-if="display.name.value !== 'xs'" class="md:mx-3 <md:my-3" icon="mdi-arrow-left" @click="() => router.go(-1)" size="50" />
    <v-card v-if="learnware" class="p-2 w-1/1" :flat="display.name.value === 'xs'">
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
        <div>Library type: {{ learnware.libraryType }}</div>
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