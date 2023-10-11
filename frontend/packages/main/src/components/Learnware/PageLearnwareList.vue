<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader";
import LearnwareList from "./LearnwareList.vue";

const display = useDisplay();

const emit = defineEmits(["click:edit", "click:delete", "pageChange"]);

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  filters: {
    type: Object,
    default: () => ({}),
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
  page: {
    type: Number,
    default: 1,
  },
  pageSize: {
    type: Number,
    default: 10,
  },
  pageNum: {
    type: Number,
    default: 10,
  },
  loading: {
    type: Boolean,
  },
  showPagination: {
    type: Boolean,
    default: true,
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

const greaterThanXs = computed(() => display.name.value !== "xs");

function jumpPage(newPage): void {
  if (newPage >= 1 && newPage <= props.pageNum) {
    emit("pageChange", newPage);
  }
}

function nextPage(): void {
  if (props.page < props.pageNum) {
    jumpPage(props.page + 1);
  }
}

function formerPage(): void {
  if (props.page > 1) {
    jumpPage(props.page - 1);
  }
}

function handleClickEdit(id): void {
  emit("click:edit", id);
}

function handleClickDelete(id): void {
  emit("click:delete", id);
}
</script>

<template>
  <div>
    <learnware-list
      v-if="!loading"
      :items="items"
      :filters="filters"
      :cols="cols"
      :md="md"
      :sm="sm"
      :xs="xs"
      :is-admin="isAdmin"
      @click:edit="(id) => handleClickEdit(id)"
      @click:delete="(id) => handleClickDelete(id)"
    />

    <div
      v-else
      class="grid p-2 gap-3"
      :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
    >
      <v-skeleton-loader
        v-for="(item, i) in pageSize"
        :key="i"
        class="w-1/1"
        :type="items && items[0] && items[0].matchScore ? 'article, table-tfoot' : 'article'"
      ></v-skeleton-loader>
    </div>

    <div v-if="showPagination" class="my-5 flex justify-center items-center">
      <div v-if="pageNum <= 7">
        <v-btn icon="mdi-arrow-left" color="primary" @click="formerPage"></v-btn>
        <v-btn
          v-for="i in pageNum"
          :key="i"
          class="mx-1 !px-2 !min-w-0"
          :color="i === page ? 'primary' : 'default'"
          flat
          @click="() => jumpPage(i)"
        >
          {{ i }}
        </v-btn>
        <v-btn icon="mdi-arrow-right" color="primary" @click="nextPage"></v-btn>
      </div>
      <div v-else>
        <v-btn icon="mdi-arrow-left" color="primary" @click="formerPage"></v-btn>
        <v-btn
          v-if="greaterThanXs && page > 2"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="jumpPage(1)"
          >1</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page === 4"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="jumpPage(2)"
          >2</v-btn
        >
        <v-btn v-if="greaterThanXs && page > 4" class="mx-2 !px-2 !min-w-0" variant="text"
          >...</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page > pageNum - 1"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page - 4)"
        >
          {{ page - 4 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page > pageNum - 2"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page - 3)"
        >
          {{ page - 3 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page > pageNum - 3"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page - 2)"
        >
          {{ page - 2 }}
        </v-btn>
        <v-btn
          v-if="page > 1"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page - 1)"
        >
          {{ page - 1 }}
        </v-btn>
        <v-btn class="mx-2 !px-2 !min-w-0" color="primary">{{ page }}</v-btn>
        <v-btn
          v-if="page < pageNum"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page + 1)"
        >
          {{ page + 1 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page < 4"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page + 2)"
        >
          {{ page + 2 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page < 3"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page + 3)"
        >
          {{ page + 3 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page < 2"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page + 4)"
        >
          {{ page + 4 }}
        </v-btn>
        <v-btn v-if="greaterThanXs && page < pageNum - 3" class="mx-2 !px-2 !min-w-0" variant="text"
          >...</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page === pageNum - 3"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(pageNum - 1)"
        >
          {{ pageNum - 1 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page < pageNum - 1"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(pageNum)"
        >
          {{ pageNum }}
        </v-btn>
        <v-btn icon="mdi-arrow-right" color="primary" @click="nextPage"></v-btn>
      </div>
    </div>
  </div>
</template>
