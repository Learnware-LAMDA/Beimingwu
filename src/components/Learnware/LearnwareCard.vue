<script setup>
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import AudioBtn from '@/components/Specification/SpecTag/DataTypeBtn/AudioBtn.vue'
import VideoBtn from '@/components/Specification/SpecTag/DataTypeBtn/VideoBtn.vue'
import TextBtn from '@/components/Specification/SpecTag/DataTypeBtn/TextBtn.vue'
import ImageBtn from '@/components/Specification/SpecTag/DataTypeBtn/ImageBtn.vue'
import TableBtn from '@/components/Specification/SpecTag/DataTypeBtn/TableBtn.vue'
import { downloadLearnware } from '@/utils'
import colors from 'vuetify/lib/util/colors'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  filters: {
    type: Object,
  },
  showDownload: {
    type: Boolean,
    default: true
  },
  isAdmin: {
    type: Boolean,
    default: false,
  }
})

const emit = defineEmits(['click:delete'])

const display = useDisplay()

const greaterThanXs = computed(() => {
  return display.name.value !== 'xs'
})

const greaterThanSm = computed(() => {
  return display.name.value !== 'xs' && display.name.value !== 'sm'
})

const dataTypeBtns = {
  'Table': TableBtn,
  'Image': ImageBtn,
  'Text': TextBtn,
  'Video': VideoBtn,
  'Audio': AudioBtn,
}

function getColorByScore(score) {
  if (score > 80) return colors.green.base
  if (score > 50) return colors.orange.base
  return colors.red.base
}

function handleClickDelete(id) {
  emit('click:delete', id)
}
</script>

<template>
  <v-card flat :density="greaterThanXs ? 'comfortable' : 'compact'" class="card" :class="typeof (item.matchScore) === 'number' ? ['pt-2'] : ['py-2']">
    <div class="first-row">
      <v-card-title class="title">
        <v-avatar :size="greaterThanSm ? 'default' : 'small'">
          <component class="w-4/5 opacity-70" :is="dataTypeBtns[item.dataType]" />
        </v-avatar>
        {{ `${item.username ? item.username + '/' : ''}${item.name}` }}
      </v-card-title>
    </div>
    <v-card-text class="card-text">
      <div class="label"
        :class="filters && filters.dataType && filters.dataType.includes(item.dataType) ? 'active' : undefined">{{
          item.dataType }}</div>
      <div class="label"
        :class="filters && filters.taskType && filters.taskType.includes(item.taskType) ? 'active' : undefined">{{
          item.taskType }}</div>
      <div v-for="deviceType in item.deviceType" class="label"
        :class="filters && filters.deviceType && filters.deviceType.includes(deviceType) ? 'active' : undefined">
        {{ deviceType }}</div>
      <div class="tag" :class="filters && filters.tagList && filters.tagList.includes(tag) ? 'active' : undefined"
        v-for="(tag, i) in item.tagList" :key="i">{{ tag }}</div>
    </v-card-text>
    <v-card-text class="card-text">
      <div class="description">{{ item.description }}</div>
    </v-card-text>
    <v-card-title class="last-row" :class="typeof (item.matchScore) === 'number' ? ['justify-between']: isAdmin ? ['justify-end'] : ['absolute', 'right-0', 'bottom-0']">
      <div v-if="typeof (item.matchScore) === 'number'" class="xl: text-xl lg:text-lg text-1rem">
        Specification score <span class="ml-2 text-xl" :style="`color: ${getColorByScore(item.matchScore)}`">{{
          item.matchScore
        }}</span>
      </div>
      <div class="actions">
        <v-tooltip v-model="item.showEditTips" location="top">
          <template v-slot:activator="{ props }">
            <v-btn flat v-if="isAdmin" icon="mdi-pencil" @click.stop="() => { }" v-bind="props"
              :size="greaterThanXs ? undefined : 'small'"></v-btn>
          </template>
          <span>Not availble</span>
        </v-tooltip>
        <v-btn flat v-if="showDownload" icon="mdi-download" @click.stop="() => downloadLearnware(item.id)"
          :size="greaterThanXs ? undefined : 'small'"></v-btn>
        <v-btn flat v-if="isAdmin" icon="mdi-delete" @click.stop="handleClickDelete(item.id)"
          :size="greaterThanXs ? undefined : 'small'"></v-btn>
      </div>
    </v-card-title>
  </v-card>
</template>

<style scoped lang="scss">
.card {
  @apply sm: (border-1 hover: (border-1 border-purple-500)) <sm: (border-b-1 rounded-0px);

  .first-row {
    @apply flex justify-between items-start;

    .title {
      @apply xl: text-xl lg:text-lg text-1rem;
    }
  }

  .last-row {
    @apply flex items-center;

    .actions {
      @apply flex flex-row justify-end;

      * {
        @apply <sm: mx-0;
      }
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
</style>