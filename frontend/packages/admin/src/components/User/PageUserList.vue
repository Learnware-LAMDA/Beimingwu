<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import UserList from "./UserList.vue";
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader";
import { User } from "types";

export interface Props {
  items: User.User[];
  page: number;
  pageSize?: number;
  pageNum: number;
  loading?: boolean;
  showPagination?: boolean;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const display = useDisplay();

const emits = defineEmits(["click:reset", "click:delete", "click:export", "pageChange"]);

const props = withDefaults(defineProps<Props>(), {
  pageSize: 10,
  loading: false,
  showPagination: true,
  cols: 2,
  md: 1,
  sm: 1,
  xs: 1,
});

const realCols = computed(() => {
  if (display.name.value === "xs") {
    return props.xs;
  }
  if (display.name.value === "sm") {
    return props.sm;
  }
  if (display.name.value === "md") {
    return props.md;
  }
  return props.cols;
});

const greaterThanXs = computed(() => {
  return display.name.value !== "xs";
});

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

function jumpPage(newPage: number): void {
  if (newPage >= 1 && newPage <= props.pageNum) {
    emits("pageChange", newPage);
  }
}

function handleClickReset(id: string): void {
  emits("click:reset", id);
}

function handleClickDelete(id: string): void {
  emits("click:delete", id);
}

function handleClickExport(id: string): void {
  emits("click:export", id);
}
</script>

<template>
  <div>
    <user-list
      v-if="!loading"
      :items="items"
      :cols="cols"
      :md="md"
      :sm="sm"
      :xs="xs"
      @click:delete="handleClickDelete"
      @click:reset="handleClickReset"
      @click:export="handleClickExport"
    />

    <div
      v-else
      class="grid p-2 gap-3"
      :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
    >
      <v-skeleton-loader
        v-for="i in pageSize"
        :key="i"
        class="w-1/1"
        type="table-tfoot"
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
          >{{ i }}</v-btn
        >
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
          >{{ page - 4 }}</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page > pageNum - 2"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page - 3)"
          >{{ page - 3 }}</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page > pageNum - 3"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page - 2)"
          >{{ page - 2 }}</v-btn
        >
        <v-btn
          v-if="page > 1"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page - 1)"
          >{{ page - 1 }}</v-btn
        >
        <v-btn class="mx-2 !px-2 !min-w-0" color="primary">{{ page }}</v-btn>
        <v-btn
          v-if="page < pageNum"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page + 1)"
          >{{ page + 1 }}</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page < 4"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page + 2)"
          >{{ page + 2 }}</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page < 3"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page + 3)"
          >{{ page + 3 }}</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page < 2"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(page + 4)"
          >{{ page + 4 }}</v-btn
        >
        <v-btn v-if="greaterThanXs && page < pageNum - 3" class="mx-2 !px-2 !min-w-0" variant="text"
          >...</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page === pageNum - 3"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(pageNum - 1)"
          >{{ pageNum - 1 }}</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page < pageNum - 1"
          class="mx-2 !px-2 !min-w-0"
          variant="text"
          @click="() => jumpPage(pageNum)"
          >{{ pageNum }}</v-btn
        >
        <v-btn icon="mdi-arrow-right" color="primary" @click="nextPage"></v-btn>
      </div>
    </div>
  </div>
</template>
