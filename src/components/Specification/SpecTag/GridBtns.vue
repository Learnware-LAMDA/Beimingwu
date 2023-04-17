<script setup>
import { ref, computed, watch } from 'vue'
import { useDisplay } from 'vuetify'
import IconBtn from './IconBtn.vue'

const display = useDisplay()

const props = defineProps({
  value: {
    type: String,
    require: true,
  },
  btns: {
    type: Array,
    require: true,
  },
  title: {
    type: String,
    default: 'title',
  },
  cols: {
    type: Number,
    default: 5,
  },
  md: {
    type: Number,
  },
  sm: {
    type: Number,
  },
  xs: {
    type: Number,
  }
})

const emit = defineEmits(['update:value'])

const value = ref(props.value)

const realCols = computed(() => {
  let cols = props.cols
  if (props.md && display.md.value) {
    cols = props.md
  } else if (props.sm && display.sm.value) {
    cols = props.sm
  } else if (props.xs && display.xs.value) {
    cols = props.xs
  }
  return cols
})

function clickBtn(btn) {
  value.value = (btn.title === value.value) ? '' : btn.title
}

watch(
  () => value.value,
  (newValue) => {
    emit('update:value', newValue)
  }
)
</script>

<template>
  <div class="grid-container">
    <div class="title text-h6 !text-1rem">{{ title }}</div>
    <div class="btn-container" :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }">
      <icon-btn class="btn" v-for="(btn, i) in btns" :icon-component="btn.icon" :title="btn.title"
        :active="btn.title === value" :key="i" @click="() => clickBtn(btn)" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.grid-container {
  .title {
    @apply mt-7 mb-5;
  }

  .btn-container {
    @apply grid gap-2;

    .btn {
      @apply pr-3;
    }
  }
}
</style>