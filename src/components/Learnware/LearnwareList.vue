<script setup>
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useRouter } from "vue-router";
import LearnwareCard from "./LearnwareCard.vue";
import oopsImg from "../../assets/images/oops.svg";

const emit = defineEmits(["click:delete"]);

const display = useDisplay();

const router = useRouter();

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
  filters: {
    type: Object,
    default: () => ({}),
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
  cols: {
    type: Number,
    default: 2,
  },
  md: {
    type: Number,
    default: 1,
  },
  sm: {
    type: Number,
    default: 1,
  },
  xs: {
    type: Number,
    default: 1,
  },
});

const realCols = computed(() => props[display.name.value] || props.cols);

function handleClickDelete(id) {
  emit("click:delete", id);
}

function showLearnwareDetail(id) {
  router.push({ path: "/learnwaredetail", query: { id } });
}
</script>

<template>
  <div
    class="learnware-list-container"
    :class="items.length === 0 ? ['!grid-cols-1', 'h-1/1'] : []"
    :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
  >
    <TransitionGroup name="fade">
      <template v-for="(item, i) in items" :key="i">
        <learnware-card
          :item="item"
          :filters="filters"
          :is-admin="isAdmin"
          @click="showLearnwareDetail(item.id)"
          @click:delete="(id) => handleClickDelete(id)"
        />
      </template>
    </TransitionGroup>
    <div v-if="items.length === 0" flat class="no-learnware">
      <v-img class="oops-img" width="100" :src="oopsImg"></v-img>
      Oops! There are no learnwares.
    </div>
  </div>
</template>

<style scoped lang="scss">
.learnware-list-container {
  @apply relative sm:p-2 p-1 grid xl: grid-cols-2 lg:grid-cols-2 sm:gap-3;

  .score {
    @apply lg: '!text-1rem' '!text-0.8rem';
  }

  .no-learnware {
    @apply py-5 w-1/1 text-center text-2xl;

    .oops-img {
      @apply mx-auto;
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
