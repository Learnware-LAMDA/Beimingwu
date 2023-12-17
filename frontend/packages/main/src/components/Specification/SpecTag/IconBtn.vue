<script setup lang="ts">
const emit = defineEmits(["click"]);

defineProps({
  title: {
    type: String,
    default: "Button",
  },
  showTitle: {
    type: Boolean,
    default: true,
  },
  active: {
    type: Boolean,
    require: true,
  },
});
</script>

<template>
  <div
    class="btn"
    :class="{ active, 'justify-center': !showTitle }"
    flat
    @click="($event) => emit('click', $event)"
  >
    <v-responsive
      class="responsive"
      :aspect-ratio="1 / 1"
    >
      <slot />
    </v-responsive>
    <div class="my-title">
      <span v-if="showTitle">{{ title }}</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.btn {
  @apply dark:bg-inactive-dark bg-inactive-light flex h-full cursor-pointer items-center justify-start rounded-lg border py-3 text-[0.9rem] text-white transition dark:border  dark:text-gray-300;

  .responsive {
    @apply ml-3 mr-4 w-full max-w-[1.25rem] sm:mr-1 sm:max-w-[1.5rem] md:mr-5 md:max-w-[1.8rem] lg:max-w-[1.8rem];

    .icon {
      @apply h-full w-full fill-white dark:fill-gray-300;
    }
  }

  .my-title {
    @apply text-xs sm:text-sm lg:text-base;
    @apply leading-5;
  }
}

.btn.active {
  @apply bg-primary-light dark:bg-primary-dark;
}
</style>
