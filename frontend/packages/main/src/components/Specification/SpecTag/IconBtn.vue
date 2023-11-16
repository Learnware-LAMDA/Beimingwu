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
  @apply flex h-full cursor-pointer items-center justify-start rounded-lg border bg-gray-400 py-4 text-[0.9rem] transition;
  color: rgb(var(--v-theme-on-primary));

  .responsive {
    @apply ml-3 mr-4 w-full max-w-[1.25rem] sm:mr-1 sm:max-w-[1.5rem] md:mr-5 md:max-w-[2rem] lg:max-w-[1.5rem];

    .icon {
      @apply h-full w-full;
      fill: rgb(var(--v-theme-on-primary));
    }
  }

  .my-title {
    @apply text-xs sm:text-sm lg:text-base;
    @apply leading-5;
  }
}

.btn.active {
  background-color: rgb(var(--v-theme-primary));
}
</style>
