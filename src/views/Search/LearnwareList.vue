<script setup>
const props = defineProps({
  items: {
    type: Array,
    required: true,
  }
})
</script>

<template>
  <div class="learnware-list-container" :class="items.length === 0 ? ['!grid-cols-1', 'h-1/1'] : null">
    <TransitionGroup name="fade">
      <v-card flat v-for="(item, i) in items" :key="i">
        <div class="first-row">
          <v-card-title class="title">{{ item.title }}</v-card-title>
        </div>
        <v-card-text class="card-text">
          <div class="label">{{ item.dataType }}</div>
          <div class="label">{{ item.taskType }}</div>
          <div class="label">{{ item.requirementType }}</div>
        </v-card-text>
        <v-card-text class="card-text">
          <div class="tag" v-for="(tag, i) in item.tagList" :key="i">{{ tag }}</div>
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
  @apply relative p-2 grid xl: grid-cols-3 lg:grid-cols-2 gap-3;

  .first-row {
    @apply flex items-center;

    .title {
      @apply xl: text-xl lg:text-lg text-1rem;
    }
  }

  .card-text {
    @apply flex flex-wrap pt-0 pb-2 text-gray-700;

    * {
      @apply mr-3;
    }

    .label {
      @apply px-2 mr-2 border-1 border-gray-700 text-sm text-gray-700 rounded;
    }

    .tag {
      @apply mt-1 px-2 border-1 border-gray-700 rounded-1em;
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