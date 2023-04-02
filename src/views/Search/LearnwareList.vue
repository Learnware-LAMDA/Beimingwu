<script setup>
const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
  filters: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div class="learnware-list-container" :class="items.length === 0 ? ['!grid-cols-1', 'h-1/1'] : null">
    <TransitionGroup name="fade">
      <v-card flat class="card" v-for="(item, i) in items" :key="i">
        <div class="first-row">
          <v-card-title class="title">{{ item.title }}</v-card-title>
        </div>
        <v-card-text class="card-text">
          <div class="label" :class="filters && filters.dataType && filters.dataType.includes(item.dataType) ? 'active' : null">{{ item.dataType }}</div>
          <div class="label" :class="filters && filters.taskType && filters.taskType.includes(item.taskType) ? 'active' : null">{{ item.taskType }}</div>
          <div class="label" :class="filters && filters.hardwareType && filters.hardwareType.includes(item.hardwareType) ? 'active' : null">{{ item.hardwareType }}</div>
          <div class="tag" :class="filters && filters.tagList && filters.tagList.includes(tag) ? 'active' : null" v-for="(tag, i) in item.tagList" :key="i">{{ tag }}</div>
        </v-card-text>
        <v-card-text class="card-text">
          <div>{{ item.description }}</div>
        </v-card-text>
      </v-card>
    </TransitionGroup>
    <div flat v-if="items.length === 0" class="no-learnware">
      Oops! There are no learnwares.
    </div>
  </div>
</template>

<style scoped lang="scss">
.learnware-list-container {
  @apply relative p-2 grid xl: grid-cols-2 lg:grid-cols-2 gap-3;

  .card {
    @apply border-1;
    .first-row {
      @apply flex items-center;

      .title {
        @apply xl: text-xl lg:text-lg text-1rem;
      }
    }

    .card-text {
      @apply flex flex-wrap items-center pt-0 pb-2 text-gray-700;

      * {
        @apply mr-2 mt-1;
      }

      .label {
        @apply px-2 border-gray-700 border-1 text-xs text-black rounded;
      }

      .tag {
        @apply px-2 border-gray-700 border-1 text-xs text-black rounded-1em;
      }

      .active {
        @apply bg-gray-100 border-0;
        color: rgb(var(--v-theme-primary));
      }
    }
  }

  .no-learnware {
    @apply absolute flex flex-col justify-center items-center w-1/1 h-1/1 text-2xl;
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