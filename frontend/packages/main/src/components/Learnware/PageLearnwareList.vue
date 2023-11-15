<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader";
import LearnwareList from "./LearnwareList.vue";
import type { LearnwareCardInfo, Filter } from "@beiming-system/types/learnware";

export interface Props {
  items: LearnwareCardInfo[];
  filters?: Filter;
  isAdmin?: boolean;
  page: number;
  pageSize?: number;
  pageNum: number;
  loading: boolean;
  showPagination: boolean;
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
}

const display = useDisplay();

const emit = defineEmits(["click:edit", "click:delete", "pageChange"]);

const props = withDefaults(defineProps<Props>(), {
  filters: () => ({
    id: "",
    name: "",
    dataType: "",
    taskType: "",
    libraryType: "",
    scenarioList: [],
    files: [],
  }),
  isAdmin: false,
  pageSize: 10,
  cols: 2,
  md: 1,
  sm: 1,
  xs: 1,
});

const realCols = computed(() => {
  if (display.name.value === "xs") {
    return props.xs;
  } else if (display.name.value === "sm") {
    return props.sm;
  } else if (display.name.value === "md") {
    return props.md;
  } else {
    return props.cols;
  }
});

const greaterThanXs = computed(() => display.name.value !== "xs");

function jumpPage(newPage: number): void {
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

function handleClickEdit(id: string): void {
  emit("click:edit", id);
}

function handleClickDelete(id: string): void {
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
      class="grid gap-3 p-2"
      :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
    >
      <v-skeleton-loader
        v-for="(_item, i) in pageSize"
        :key="i"
        class="w-full"
        :type="
          items && items[0] && items[0].matchScore && items[0].matchScore >= 0
            ? 'article, table-tfoot'
            : 'article'
        "
      ></v-skeleton-loader>
    </div>

    <div v-if="showPagination" class="my-5 flex items-center justify-center">
      <div v-if="pageNum <= 7">
        <v-btn icon="mdi-arrow-left" color="primary" @click="formerPage"></v-btn>
        <v-btn
          v-for="i in pageNum"
          :key="i"
          class="mx-1 !min-w-0 !px-2"
          :color="i === page ? 'primary' : 'default'"
          variant="flat"
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
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="jumpPage(1)"
          >1</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page === 4"
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="jumpPage(2)"
          >2</v-btn
        >
        <v-btn v-if="greaterThanXs && page > 4" class="mx-2 !min-w-0 !px-2" variant="text"
          >...</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page > pageNum - 1"
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="() => jumpPage(page - 4)"
        >
          {{ page - 4 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page > pageNum - 2"
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="() => jumpPage(page - 3)"
        >
          {{ page - 3 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page > pageNum - 3"
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="() => jumpPage(page - 2)"
        >
          {{ page - 2 }}
        </v-btn>
        <v-btn
          v-if="page > 1"
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="() => jumpPage(page - 1)"
        >
          {{ page - 1 }}
        </v-btn>
        <v-btn class="mx-2 !min-w-0 !px-2" color="primary">{{ page }}</v-btn>
        <v-btn
          v-if="page < pageNum"
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="() => jumpPage(page + 1)"
        >
          {{ page + 1 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page < 4"
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="() => jumpPage(page + 2)"
        >
          {{ page + 2 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page < 3"
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="() => jumpPage(page + 3)"
        >
          {{ page + 3 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page < 2"
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="() => jumpPage(page + 4)"
        >
          {{ page + 4 }}
        </v-btn>
        <v-btn v-if="greaterThanXs && page < pageNum - 3" class="mx-2 !min-w-0 !px-2" variant="text"
          >...</v-btn
        >
        <v-btn
          v-if="greaterThanXs && page === pageNum - 3"
          class="mx-2 !min-w-0 !px-2"
          variant="text"
          @click="() => jumpPage(pageNum - 1)"
        >
          {{ pageNum - 1 }}
        </v-btn>
        <v-btn
          v-if="greaterThanXs && page < pageNum - 1"
          class="mx-2 !min-w-0 !px-2"
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
