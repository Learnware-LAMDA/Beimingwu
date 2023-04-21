<script setup>
import { ref, computed } from 'vue'
import { useDisplay } from 'vuetify'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import JSZip from 'jszip'
import { VSkeletonLoader } from 'vuetify/labs/VSkeletonLoader'
import DeleteDialog from './DeleteDialog.vue'
import colors from 'vuetify/lib/util/colors'
import oopsImg from '/oops.svg'
import AudioBtn from '@/components/Specification/SpecTag/DataTypeBtn/AudioBtn.vue'
import VideoBtn from '@/components/Specification/SpecTag/DataTypeBtn/VideoBtn.vue'
import TextBtn from '@/components/Specification/SpecTag/DataTypeBtn/TextBtn.vue'
import ImageBtn from '@/components/Specification/SpecTag/DataTypeBtn/ImageBtn.vue'
import TableBtn from '@/components/Specification/SpecTag/DataTypeBtn/TableBtn.vue'

const emit = defineEmits(['delete'])

const display = useDisplay()

const router = useRouter()

const store = useStore()

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
  matchScore: {
    type: Number,
    required: true,
  },
  filters: {
    type: Object,
  },
  showActions: {
    type: Boolean,
    default: false,
  },
  cols: {
    type: Number,
    default: 2,
  },
  md: {
    type: Number,
    default: 1,
  },
  sm: {
    type: Number,
    default: 1,
  },
  xs: {
    type: Number,
    default: 1,
  },
  loading: {
    type: Boolean,
    default: false,
  }
})

const dialog = ref(null)

const downloading = ref(false)

const realCols = computed(() => {
  switch (display.name.value) {
    case 'md': if (props.md) return props.md
    case 'sm': if (props.sm) return props.sm
    case 'xs': if (props.xs) return props.xs
    default: return props.cols
  }
})

function deleteLearnware(id) {
  emit('delete', id)
}

function showLearnwareDetail(id) {
  router.push({ path: '/learnwaredetail', query: { id } })
}

function confirmDelete(index) {
  dialog.value.confirmDelete({
    id: props.items[index].id,
    name: props.items[index].name
  })
}

function downloadAll() {
  downloading.value = true

  const zip = new JSZip()
  Promise.all(props.items.map((item) => {
    return fetch(`/api/engine/download_learnware?learnware_id=${item.id}`)
      .then((res) => {
        if (res.status === 200) {
          return res
        }
        throw new Error('Network error')
      })
      .then((res) => res.arrayBuffer())
      .then(arrayBuffer => {
        zip.file(`${item.name}.zip`, arrayBuffer)
      })
  }))
    .then(() => zip.generateAsync({ type: 'blob' }))
    .then((blob) => {
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'learnwares.zip'
      a.click()
      downloading.value = false
    })
    .catch((err) => {
      downloading.value = false
      console.error(err)
      store.commit('setShowGlobalError', true)
      store.commit('setGlobalErrorMsg', err.message)
    })
}

function transformQuery(item) {
  return {
    name: item.name,
    dataType: item.dataType,
    taskType: item.taskType,
    deviceType: JSON.stringify(item.deviceType),
    tagList: JSON.stringify(item.tagList),
    description: item.description,
  }
}

function getColorByScore(score) {
  if (score > 80) return colors.green.base
  if (score > 50) return colors.orange.base
  return colors.red.base
}

const dataTypeBtns = {
  'Table': TableBtn,
  'Image': ImageBtn,
  'Text': TextBtn,
  'Video': VideoBtn,
  'Audio': AudioBtn,
}
</script>

<template>
  <div v-if="!loading" class="m-2 p-2 rounded-lg hover:border-purple-500" :class="items.length > 0 ? ['border-1'] : []">
    <div v-if="items.length > 0" class="flex justify-between">
      <v-card-title v-if="matchScore" class="score">
        Total specification score <span class="ml-2" :style="`color: ${getColorByScore(matchScore)}`">{{
          matchScore
        }}</span>
      </v-card-title>
      <v-btn variant="flat" class="!px-4 text-body-2 !text-1em border-1" @click.stop="() => downloadAll()"
        size="x-large">
        <span v-if="!downloading">
          <v-icon icon="mdi-download"></v-icon>
          Download All
        </span>
        <span v-else class="flex items-center">
          <v-progress-circular class="mr-3" indeterminate></v-progress-circular>
          Downloading ...
        </span>
      </v-btn>
    </div>
    <v-card flat class="learnware-list-container" :class="items.length === 0 ? ['!grid-cols-1', 'h-1/1'] : null"
      :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }">
      <delete-dialog ref="dialog" @confirm="(id) => deleteLearnware(id)" />
      <TransitionGroup name="fade">
        <v-card flat class="card" v-for="(item, i) in items" :key="i" @click="() => showLearnwareDetail(item.id)">
          <div class="first-row">
            <v-card-title class="title">
              <v-avatar>
                <component class="w-4/5 opacity-70" :is="dataTypeBtns[item.dataType]" />
              </v-avatar>
              {{ `${item.username}/${item.name}` }}
            </v-card-title>
            <v-card-actions class="actions">
              <v-tooltip v-model="item.showEditTips" location="top">
                <template v-slot:activator="{ props }">
                  <v-btn v-if="showActions" icon="mdi-pencil" @click.stop="() => { }" v-bind="props"></v-btn>
                </template>
                <span>Not availble</span>
              </v-tooltip>
              <v-btn v-if="showActions" icon="mdi-delete" @click.stop="() => confirmDelete(i)"></v-btn>
            </v-card-actions>
          </div>
          <v-card-text class="card-text">
            <div class="label"
              :class="filters && filters.dataType && filters.dataType.includes(item.dataType) ? 'active' : null">{{
                item.dataType }}</div>
            <div class="label"
              :class="filters && filters.taskType && filters.taskType.includes(item.taskType) ? 'active' : null">{{
                item.taskType }}</div>
            <div v-for="deviceType in item.deviceType" class="label"
              :class="filters && filters.deviceType && filters.deviceType.includes(deviceType) ? 'active' : null">
              {{ deviceType }}</div>
            <div class="tag" :class="filters && filters.tagList && filters.tagList.includes(tag) ? 'active' : null"
              v-for="(tag, i) in item.tagList" :key="i">{{ tag }}</div>
          </v-card-text>
          <v-card-text class="card-text">
            <div class="description">{{ item.description }}</div>
          </v-card-text>
        </v-card>
      </TransitionGroup>
      <div flat v-if="items.length === 0" class="no-learnware">
        <v-img class="oops-img" width="100" :src="oopsImg"></v-img>
        Oops! There are no learnwares.
      </div>
    </v-card>
  </div>
  <div v-else class="grid p-2 gap-3" :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }">
    <v-skeleton-loader v-for="_ in 4" class="w-1/1" type="article"></v-skeleton-loader>
  </div>
</template>

<style scoped lang="scss">
.learnware-list-container {
  @apply relative m-2 grid xl: grid-cols-2 lg:grid-cols-2 gap-3 bg-transparent;

  .card {
    @apply border-1;

    .first-row {
      @apply flex justify-between items-center;

      .title {
        @apply xl: text-xl lg:text-lg text-1rem;
      }

      .actions {
        @apply justify-end mt-1;
      }
    }

    .card-text {
      @apply flex flex-wrap items-center pt-0 pb-2 text-gray-700;

      * {
        @apply mr-2 mt-1;
      }

      .label {
        @apply px-2 border-gray-700 bg-gray-200 text-xs text-black rounded;
      }

      .tag {
        @apply px-2 border-gray-700 bg-gray-200 text-xs text-black rounded-1em;
      }

      .label.active {
        @apply bg-gray-100 border-0;
        color: rgb(var(--v-theme-primary));
      }

      .tag.active {
        @apply bg-gray-100 text-orange-600 border-0;
      }

      .description {
        @apply truncate;
      }
    }

    .placeholder {
      @apply opacity-0;
    }
  }

  .score {
    @apply my-2 lg: '!text-1.3rem' '!text-0.8rem';
  }

  .no-learnware {
    @apply py-5 w-1/1 text-center text-2xl;

    .oops-img {
      @apply mx-auto;
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  @apply transition duration-500;
}

.fade-enter,
.fade-leave-to {
  @apply opacity-0;
}
</style>