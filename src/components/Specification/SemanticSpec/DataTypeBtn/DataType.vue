<script setup>
import { ref, watch } from 'vue'
import AudioBtn from './DataTypeBtn/AudioBtn.vue'
import VideoBtn from './DataTypeBtn/VideoBtn.vue'
import TextBtn from './DataTypeBtn/TextBtn.vue'
import ImageBtn from './DataTypeBtn/ImageBtn.vue'
import TableBtn from './DataTypeBtn/TableBtn.vue'

const props = defineProps({
  dataType: {
    type: String,
    require: true,
  },
})

const emit = defineEmits(['update:dataType'])

const value = ref(props.dataType)

const dataTypeBtns = [
  {
    title: 'Audio',
    icon: AudioBtn,
  },
  {
    title: 'Video',
    icon: VideoBtn,
  },
  {
    title: 'Text',
    icon: TextBtn,
  },
  {
    title: 'Image',
    icon: ImageBtn,
  },
  {
    title: 'Table',
    icon: TableBtn,
  }
]

function clickBtn(btn) {
  value.value = (btn.title === value.value) ? '' : btn.title
}

watch(
  () => value.value,
  (newValue) => {
    emit('update:dataType', newValue)
  }
)
</script>

<template>
  <div class="data-type">
    <div class="data-type-title">Data type</div>
    <div class="data-type-btn">
      <v-responsive v-for="(btn, i) in dataTypeBtns" :key="i" @click="clickBtn(btn)">
        <div class="btn-container" :class="{ active: btn.title === value }">
          <component :is="btn.icon" />
          {{ btn.title }}
        </div>
      </v-responsive>
    </div>
  </div>
</template>

<style scoped lang="scss">
.data-type {
  .data-type-title {
    @apply text-lg;
  }

  .data-type-btn {
    @apply grid grid-cols-5 gap-2 cursor-pointer;

    .btn-container {
      @apply flex flex justify-start items-center h-full rounded-lg bg-gray-400 border-1 transition text-0.9rem;
      color: rgb(var(--v-theme-on-primary));

      svg {
        @apply w-1/2 h-1/2;
        fill: rgb(var(--v-theme-on-primary));
      }
    }

    .btn-container.active {
      background-color: rgb(var(--v-theme-primary));

      svg {
        stroke: rgb(var(--v-theme-primary));
      }
    }
  }
}
</style>