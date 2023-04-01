<script setup>
const emit = defineEmits(['click'])

const props = defineProps({
  iconComponent: {
    type: Object,
    require: true,
  },
  title: {
    type: String,
    default: 'Button',
  },
  showTitle: {
    type: Boolean,
    default: true,
  },
  active: {
    type: Boolean,
    require: true,
  }
})
</script>

<template>
  <div class="btn" :class="{ active, 'justify-center': !showTitle }" @click="$event => emit('click', $event)">
    <v-responsive class="responsive" :aspect-ratio="1 / 1">
      <component class="icon" :is="iconComponent" />
    </v-responsive>
    <div class="title">
      <span v-if="showTitle">{{ title }}</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.btn {
  @apply flex justify-start items-center py-4 h-full rounded-lg bg-gray-400 border-1 transition text-0.9rem cursor-pointer;
  color: rgb(var(--v-theme-on-primary));

  .responsive {
    @apply w-1/1 lg:max-w-10 md:max-w-8 sm:max-w-6 max-w-5 md:mr-5 ml-3 sm:mr-1 mr-4;

    .icon {
      @apply w-1/1 h-1/1;
      fill: rgb(var(--v-theme-on-primary));
    }
  }

  .title {
    @apply lg:text-1rem sm:text-sm text-xs;
  }
}

.btn.active {
  background-color: rgb(var(--v-theme-primary));

  svg {
    stroke: rgb(var(--v-theme-primary));
  }
}
</style>