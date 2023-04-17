<script setup>
import { ref, computed, onActivated, onDeactivated } from 'vue'
import { useDisplay } from 'vuetify'
import { useRouter } from 'vue-router'
import DeleteDialog from './DeleteDialog.vue'
import { downloadLearnware } from '@/utils'
import colors from 'vuetify/lib/util/colors'
import oopsImg from '/oops.svg'

const emit = defineEmits(['delete'])

const display = useDisplay()

const router = useRouter()

const props = defineProps({
  items: {
    type: Array,
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
  }
})

const dialog = ref(null)
const scrollY = ref(0)

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

function saveScroll() {
  scrollY.value = window.scrollY
}

function getColorByScore(score) {
  if (score > 80) return colors.green.base
  if (score > 50) return colors.orange.base
  return colors.red.base
}

onActivated(() => {
  window.scrollTo(0, scrollY.value)
  window.addEventListener('scroll', saveScroll)
})

onDeactivated(() => {
  window.removeEventListener('scroll', saveScroll)
})
</script>

<template>
  <div class="learnware-list-container" :class="items.length === 0 ? ['!grid-cols-1', 'h-1/1'] : null"
    :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }">
    <delete-dialog ref="dialog" @confirm="(id) => deleteLearnware(id)" />
    <TransitionGroup name="fade">
      <v-card flat class="card" v-for="(item, i) in items" :key="i" @click="() => showLearnwareDetail(item.id)">
        <div class="first-row">
          <v-card-title class="title">{{ item.name }}</v-card-title>
          <v-card-actions class="actions">
            <v-tooltip v-model="item.showEditTips" location="top">
              <template v-slot:activator="{ props }">
                <v-btn v-if="showActions" icon="mdi-pencil" @click.stop="() => { }" v-bind="props"></v-btn>
              </template>
              <span>Not availble</span>
            </v-tooltip>
            <v-btn icon="mdi-download" @click.stop="() => downloadLearnware(item.id)"></v-btn>
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
        <v-card-title v-if="item.matchScore" class="score">
          Specification score <span class="ml-2 text-xl" :style="`color: ${getColorByScore(item.matchScore)}`">{{
            item.matchScore
          }}</span>
        </v-card-title>
      </v-card>
    </TransitionGroup>
    <div flat v-if="items.length === 0" class="no-learnware">
      <v-img class="oops-img" width="100" :src="oopsImg"></v-img>
      Oops! There are no learnwares.
    </div>
  </div>
</template>

<style scoped lang="scss">
.learnware-list-container {
  @apply relative p-2 grid xl: grid-cols-2 lg:grid-cols-2 gap-3;

  .card {
    @apply border-1 hover: (border-1 border-purple-500);

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
    @apply lg: '!text-1rem' '!text-0.8rem';
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