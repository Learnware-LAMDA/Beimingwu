<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick, onActivated } from "vue";
import { useDisplay } from "vuetify";
import { searchLearnware } from "../request/engine";
import UserRequirement from "../components/Search/UserRequirement.vue";
import PageLearnwareList from "../components/Learnware/PageLearnwareList.vue";
import MultiRecommendedLearnwareList from "../components/Learnware/MultiRecommendedLearnwareList.vue";
import { Learnware } from "types";

const display = useDisplay();

const filters = ref<Learnware.Filter>({
  name: "",
  dataType: "",
  taskType: "",
  libraryType: "",
  tagList: [],
  files: [],
});

const multiRecommendedLearnwareItems = ref<Learnware.LearnwareCardInfo[]>([]);
const multiRecommendedMatchScore = ref<number>(0);
const singleRecommendedLearnwarePage = ref(1);
const singleRecommendedLearnwarePageNum = ref(1);
const singleRecommendedLearnwarePageSize = ref(Math.ceil(display.height.value / 900) * 10);
const singleRecommendedLearnwareItems = ref<Learnware.LearnwareCardInfo[]>([]);
const loading = ref(false);

const contentRef = ref<HTMLDivElement | null>(null);
const anchorRef = ref<HTMLDivElement | null>(null);

const scrollTop = ref(0);

const showError = ref(false);
const errorMsg = ref("");
const errorTimer = ref();

const showMultiRecommended = computed(
  () =>
    multiRecommendedLearnwareItems.value &&
    multiRecommendedLearnwareItems.value.length > 1 &&
    singleRecommendedLearnwarePage.value === 1,
);
const multiRecommendedTips = ref(true);
const singleRecommendedTips = ref(true);

function pageChange(newPage: number): void {
  singleRecommendedLearnwarePage.value = newPage;
}

function fetchByFilterAndPage(filters: Learnware.Filter, page: number): void {
  showError.value = false;
  loading.value = true;

  searchLearnware({
    name: filters.name,
    dataType: filters.dataType,
    taskType: filters.taskType,
    libraryType: filters.libraryType,
    tagList: filters.tagList,
    files: filters.files,
    page,
    limit: singleRecommendedLearnwarePageSize.value,
  })
    .then((res) => {
      switch (res.code) {
        case 0: {
          multiRecommendedLearnwareItems.value = res.data.learnware_list_multi.map((item) => ({
            id: item.learnware_id,
            username: item.username,
            lastModify: item.last_modify,
            name: item.semantic_specification.Name.Values,
            description: item.semantic_specification.Description.Values,
            dataType: item.semantic_specification.Data.Values[0],
            taskType: item.semantic_specification.Task.Values[0],
            libraryType: item.semantic_specification.Library.Values[0],
            tagList: item.semantic_specification.Scenario.Values,
          }));
          if (res.data.learnware_list_multi.length > 0) {
            multiRecommendedMatchScore.value = Math.floor(
              res.data.learnware_list_multi[0].matching * 100,
            );
          }

          singleRecommendedLearnwareItems.value = res.data.learnware_list_single.map((item) => ({
            id: item.learnware_id,
            username: item.username,
            lastModify: item.last_modify,
            name: item.semantic_specification.Name.Values,
            description: item.semantic_specification.Description.Values,
            dataType: item.semantic_specification.Data.Values[0],
            taskType: item.semantic_specification.Task.Values[0],
            libraryType: item.semantic_specification.Library.Values[0],
            tagList: item.semantic_specification.Scenario.Values,
            matchScore: filters.files?.length > 0 ? Math.floor(item.matching * 100) : -1,
          }));
          singleRecommendedLearnwarePageNum.value = res.data.total_pages;
          return;
        }
        default: {
          throw new Error(res.msg);
        }
      }
    })
    .catch((err) => {
      console.error(err);
      showError.value = true;
      clearTimeout(errorTimer.value);
      setTimeout(() => (showError.value = false), 2000);
      errorMsg.value = err.message;
    })
    .finally(() => {
      loading.value = false;
    });
}

watch(
  () => filters.value,
  () => {
    singleRecommendedLearnwarePage.value = 1;
  },
  { deep: true },
);

watch(
  () => singleRecommendedLearnwarePage.value,
  () => {
    if (anchorRef.value) {
      if (display.name.value === "xs") {
        anchorRef.value.scrollIntoView();
      }
    }
  },
);

watch(
  () => [filters.value, singleRecommendedLearnwarePage.value],
  (newVal) => {
    const [newFilters, newPage] = newVal as [Learnware.Filter, number];

    fetchByFilterAndPage(newFilters, newPage - 1);

    if (contentRef.value) {
      if (display.name.value !== "xs") {
        contentRef.value.scrollTop = 0;
      }
    }
  },
  { deep: true },
);

onActivated(() => {
  if (contentRef.value) {
    contentRef.value.scrollTop = scrollTop.value;
  }
  fetchByFilterAndPage(filters.value, singleRecommendedLearnwarePage.value - 1);
});

onMounted(() => {
  nextTick(() => {
    if (contentRef.value) {
      contentRef.value.addEventListener("scroll", () => {
        if (contentRef.value) {
          scrollTop.value = contentRef.value.scrollTop;
        }
      });
    }
  });
});
</script>

<template>
  <div class="search-container">
    <v-scroll-y-transition class="fixed w-1/1 z-index-10">
      <v-card-actions v-if="showError">
        <v-alert
          class="w-1/1 max-w-900px mx-auto"
          closable
          :text="errorMsg"
          type="error"
          @click:close="showError = false"
        />
      </v-card-actions>
    </v-scroll-y-transition>

    <user-requirement v-model:value="filters" />

    <div ref="contentRef" class="content">
      <v-card v-if="showMultiRecommended" flat class="sm:m-2 mt-4 bg-transparent">
        <v-card-title v-if="!multiRecommendedTips">Recommended multiple learnwares</v-card-title>
        <v-card-text v-if="multiRecommendedTips" class="!p-2">
          <v-alert
            v-model="multiRecommendedTips"
            title="Recommended multiple learnwares"
            text="The learnwares listed below are highly recommended as they have the highest statistical specification similarity to your tasks. Combining these learnwares can lead to great effectiveness."
            closable
            color="success"
          >
            <template #prepend>
              <v-icon icon="mdi-hexagon-multiple" size="x-large"></v-icon>
            </template>
          </v-alert>
        </v-card-text>
        <multi-recommended-learnware-list
          :items="multiRecommendedLearnwareItems"
          :match-score="multiRecommendedMatchScore"
          :filters="filters"
          :loading="loading"
          @page-change="pageChange"
        />
      </v-card>
      <v-card flat class="sm:m-2 mt-4 bg-transparent">
        <v-card-title v-if="showMultiRecommended && !singleRecommendedTips"
          >Recommended single learnwares</v-card-title
        >
        <v-card-text v-if="showMultiRecommended && singleRecommendedTips" class="!p-2">
          <v-alert
            v-model="singleRecommendedTips"
            title="Recommended single learnware"
            text="The listed learnwares are not highly recommended as they may not precisely match your task requirements in terms of statistical specifications. However, they are still available for your use."
            closable
            color="info"
          >
            <template #prepend>
              <v-icon icon="mdi-hexagon" size="x-large"></v-icon>
            </template>
          </v-alert>
        </v-card-text>
        <page-learnware-list
          :items="singleRecommendedLearnwareItems"
          :filters="filters"
          :page="singleRecommendedLearnwarePage"
          :page-num="singleRecommendedLearnwarePageNum"
          :page-size="singleRecommendedLearnwarePageSize"
          :loading="loading"
          :show-pagination="singleRecommendedLearnwarePageNum > 1"
          @page-change="pageChange"
        />
      </v-card>
    </div>
  </div>
</template>

<style scoped lang="scss">
.search-container {
  @apply md: (fixed flex) mx-auto w-1/1;
  height: calc(100% - var(--v-layout-top));

  .content {
    @apply w-1/1 overflow-y-scroll;
  }
}
</style>
