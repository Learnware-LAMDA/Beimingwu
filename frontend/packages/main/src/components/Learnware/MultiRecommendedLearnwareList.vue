<script setup lang="ts">
import { ref, computed } from "vue";
import { useDisplay } from "vuetify";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { downloadLearnware } from "../../request/engine";
import JSZip from "jszip";
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader";
import colors from "vuetify/lib/util/colors";
import LearnwareCard from "./LearnwareCard.vue";
import oopsImg from "../../assets/images/public/oops.svg?url";

const display = useDisplay();

const router = useRouter();

const store = useStore();

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
  matchScore: {
    type: Number,
    required: true,
  },
  filters: {
    type: Object,
    default: () => ({}),
  },
  showActions: {
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
  loading: {
    type: Boolean,
    default: false,
  },
});

const downloading = ref(false);

const realCols = computed(() => props[display.name.value] || props.cols);

function showLearnwareDetail(id): void {
  router.push({ path: "/learnwaredetail", query: { id } });
}

function downloadAll(): void {
  downloading.value = true;

  const zip = new JSZip();
  Promise.all(
    props.items.map((item) =>
      downloadLearnware({ id: item.id })
        .then((res) => res.arrayBuffer())
        .then((arrayBuffer) => {
          zip.file(`${item.name}.zip`, arrayBuffer);
        }),
    ),
  )
    .then(() => zip.generateAsync({ type: "blob" }))
    .then((blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "learnwares.zip";
      a.click();
    })
    .catch((err) => {
      console.error(err);
      store.commit("setShowGlobalError", true);
      store.commit("setGlobalErrorMsg", err.message);
    })
    .finally(() => {
      downloading.value = false;
    });
}

function getColorByScore(score): string {
  if (score > 80) return colors.green.base;
  if (score > 50) return colors.orange.base;
  return colors.red.base;
}
</script>

<template>
  <div
    v-if="!loading"
    class="m-2 p-2 rounded-lg hover:border-purple-500"
    :class="items.length > 0 ? ['border-1'] : []"
  >
    <div v-if="items.length > 0" class="flex justify-between">
      <v-card-title v-if="matchScore" class="score">
        Total specification score
        <span class="ml-2" :style="`color: ${getColorByScore(matchScore)}`">{{ matchScore }}</span>
      </v-card-title>
      <v-btn
        variant="flat"
        class="!px-4 text-body-2 !text-1em border-1"
        @click.stop="() => downloadAll()"
      >
        size="x-large">
        <span v-if="!downloading">
          <v-icon icon="mdi-download"></v-icon>
          Download All
        </span>
        <span v-else class="flex items-center">
          <v-progress-circular class="mr-3" indeterminate></v-progress-circular>
          Downloading ...
        </span>
      </v-btn>
    </div>
    <v-card
      flat
      class="learnware-list-container"
      :class="items.length === 0 ? ['!grid-cols-1', 'h-1/1'] : null"
      :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
    >
      <TransitionGroup name="fade">
        <learnware-card
          v-for="(item, i) in items"
          :key="i"
          :item="item"
          :filters="filters"
          :show-download="false"
          @click="() => showLearnwareDetail(item.id)"
        />
      </TransitionGroup>
      <div v-if="items.length === 0" flat class="no-learnware">
        <v-img class="oops-img" width="100" :src="oopsImg"></v-img>
        Oops! There are no learnwares.
      </div>
    </v-card>
  </div>
  <div
    v-else
    class="grid p-2 gap-3"
    :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
  >
    <v-skeleton-loader
      v-for="(item, index) in 4"
      :key="index"
      class="w-1/1"
      type="article"
    ></v-skeleton-loader>
  </div>
</template>

<style scoped lang="scss">
.learnware-list-container {
  @apply relative m-2 grid xl: grid-cols-2 lg:grid-cols-2 gap-3 bg-transparent;

  .card {
    @apply border-1;

    .first-row {
      @apply flex justify-between items-center;

      .title {
        @apply xl: text-xl lg:text-lg text-1rem;
      }

      .actions {
        @apply justify-end mt-1;
      }
    }

    .card-text {
      @apply flex flex-wrap items-center pt-0 pb-2 text-gray-700;

      * {
        @apply mr-2 mt-1;
      }

      .label {
        @apply px-2 border-gray-700 bg-gray-200 text-xs text-black rounded;
      }

      .tag {
        @apply px-2 border-gray-700 bg-gray-200 text-xs text-black rounded-1em;
      }

      .label.active {
        @apply bg-gray-100 border-0;
        color: rgb(var(--v-theme-primary));
      }

      .tag.active {
        @apply bg-gray-100 text-orange-600 border-0;
      }

      .description {
        @apply truncate;
      }
    }

    .placeholder {
      @apply opacity-0;
    }
  }

  .score {
    @apply my-2 lg: '!text-1.3rem' '!text-0.8rem';
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
