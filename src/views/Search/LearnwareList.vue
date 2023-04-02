<script setup>
const props = defineProps({
  items: {
    type: Array,
    required: true,
  }
})
</script>

<template>
  <div class="learnware-list-container">
    <TransitionGroup name="fade">
      <v-card flat v-for="(item, i) in items" :key="i">
        <div class="first-row">
          <v-card-title class="title">{{ item.title }}</v-card-title>
          <v-card-text class="card-text">
            <div>{{ item.dataType }}</div>
            <div>{{ item.taskType }}</div>
            <div>{{ item.requirementType }}</div>
          </v-card-text>
        </div>
        <v-card-text class="card-text">
          <div>{{ item.description }}</div>
        </v-card-text>
      </v-card>
    </TransitionGroup>
  </div>
</template>

<style scoped lang="scss">
.learnware-list-container {
  @apply p-2 grid xl: grid-cols-2 grid-cols-1 gap-3;

  .first-row {
    @apply md: flex items-center;

    .title {
      @apply xl: text-xl lg:text-lg md:text-1rem text-sm;
    }

    .card-text * {
      @apply px-2 py-1 border-1 border-gray-700 text-gray-700 rounded-1em;
    }
  }

  .card-text {
    @apply flex flex-wrap py-2 text-gray-700;

    * {
      @apply mr-3;
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