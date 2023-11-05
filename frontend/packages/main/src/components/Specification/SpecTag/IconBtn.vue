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
    <v-responsive class="responsive" :aspect-ratio="1 / 1">
      <slot />
    </v-responsive>
    <div class="my-title">
      <span v-if="showTitle">{{ title }}</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.btn {
  @apply flex justify-start items-center py-4 h-full rounded-lg bg-gray-400 border transition text-[0.9rem] cursor-pointer;
  color: rgb(var(--v-theme-on-primary));

  .responsive {
    @apply w-full lg:max-w-[1.5rem] md:max-w-[2rem] sm:max-w-[1.5rem] max-w-[1.25rem] md:mr-5 ml-3 sm:mr-1 mr-4;

    .icon {
      @apply w-full h-full;
      fill: rgb(var(--v-theme-on-primary));
    }
  }

  .my-title {
    @apply lg:text-base sm:text-sm text-xs;
    @apply leading-5;
  }
}

.btn.active {
  background-color: rgb(var(--v-theme-primary));
}
</style>
