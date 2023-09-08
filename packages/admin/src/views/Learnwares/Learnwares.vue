<script setup>
import { ref, computed, watch, onMounted, nextTick, onActivated } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchex } from "@/utils";
import DataType from "@main/components/Specification/SpecTag/DataType.vue";
import TaskType from "@main/components/Specification/SpecTag/TaskType.vue";
import LibraryType from "@main/components/Specification/SpecTag/LibraryType.vue";
import TagList from "@main/components/Specification/SpecTag/TagList.vue";
import PageLearnwareList from "@main/components/Learnware/PageLearnwareList.vue";
import ConfirmDialog from "@/components/Dialogs/ConfirmDialog.vue";

const route = useRoute();
const router = useRouter();

const dialog = ref(null);
const deleteId = ref("");
const deleteName = ref("");

const search = ref(route.query.search || "");
const dataType = ref(route.query.dataType || "");
const taskType = ref(route.query.taskType || "");
const libraryType = ref(route.query.libraryType || "");
let _tagList;
try {
  _taglist = JSON.parse(route.query.tagList);
} catch {
  _tagList = [];
}
const tagList = ref(_tagList);

const page = ref(1);
const pageSize = ref(10);
const pageNum = ref(1);
const learnwareItems = ref([]);
const isVerify = ref(true);

const loading = ref(false);

const contentRef = ref(null);

const scrollTop = ref(0);

const success = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const successTimer = ref(null);
const errorTimer = ref(null);

function deleteLearnware(id) {
  showError.value = false;

  fetchex("/api/admin/delete_learnware", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      learnware_id: id,
    }),
  })
    .then((res) => {
      if (res.status === 200) {
        return res;
      }
      throw new Error("Network error");
    })
    .then((res) => res.json())
    .then((res) => {
      switch (res.code) {
        case 0: {
          learnwareItems.value.splice(
            learnwareItems.value.findIndex((item) => item.id === id),
            1
          );
          if (learnwareItems.value.length === 0 && page.value > 1) {
            page.value--;
          }
          fetchByFilterAndPage(filters.value, page.value);
          success.value = true;
          clearTimeout(successTimer.value);
          setTimeout(() => (success.value = false), 2000);
          return;
        }
        default: {
          throw new Error(res.msg);
        }
      }
    })
    .catch((err) => {
      console.error(err);
      loading.value = false;
      showError.value = true;
      errorMsg.value = err.message;
      clearTimeout(errorTimer.value);
      setTimeout(() => (showError.value = false), 2000);
    });
}

const filters = computed(() => ({
  name: search.value,
  dataType: dataType.value,
  taskType: taskType.value,
  libraryType: libraryType.value,
  tagList: tagList.value,
}));

function loadQuery() {
  if (route.query.search) {
    search.value = route.query.search;
  }
  if (route.query.dataType) {
    dataType.value = route.query.dataType;
  }
  if (route.query.taskType) {
    taskType.value = route.query.taskType;
  }
  if (route.query.libraryType) {
    libraryType.value = route.query.libraryType;
  }
  if (route.query.tagList) {
    tagList.value = JSON.parse(route.query.tagList);
  }
}

function saveQuery() {
  router.replace({
    query: {
      search: search.value,
      dataType: dataType.value,
      taskType: taskType.value,
      libraryType: libraryType.value,
      tagList: JSON.stringify(tagList.value),
    },
  });
}

function pageChange(newPage) {
  page.value = newPage;
  contentRef.value && (contentRef.value.scrollTop = 0);
}

function fetchLearnware(isVerify, page, limit, fd) {
  if (isVerify) {
    return fetchex("/api/engine/search_learnware", {
      method: "POST",
      body: fd,
    });
  } else {
    return fetchex("/api/admin/list_learnware", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        page: page - 1,
        limit,
        is_verified: isVerify,
      }),
    });
  }
}

function fetchByFilterAndPage(filters, page) {
  if (contentRef.value) {
    contentRef.value.scrollTop = 0;
  }

  showError.value = false;
  loading.value = true;

  fetchex("/api/engine/semantic_specification")
    .then((res) => res.json())
    .then((res) => {
      const semanticSpec = res.data.semantic_specification;
      semanticSpec.Name.Values = filters.name;
      semanticSpec.Data.Values = filters.dataType ? [filters.dataType] : [];
      semanticSpec.Task.Values = filters.taskType ? [filters.taskType] : [];
      semanticSpec.Library.Values = filters.libraryType
        ? [filters.libraryType]
        : [];
      semanticSpec.Scenario.Values = filters.tagList;
      semanticSpec.Description.Values = "";

      const fd = new FormData();
      fd.append("semantic_specification", JSON.stringify(semanticSpec));
      fd.append("statistical_specification", null);
      fd.append("limit", pageSize.value);
      fd.append("page", page - 1);
      return fd;
    })
    .then((fd) => {
      return fetchLearnware(isVerify.value, page, pageSize.value, fd)
        .then((res) => {
          if (res.status === 200) {
            return res;
          }
          throw new Error("Network error");
        })
        .then((res) => res.json())
        .then((res) => {
          switch (res.code) {
            case 0: {
              loading.value = false;
              learnwareItems.value = res.data.learnware_list_single.map(
                (item) => ({
                  id: item.learnware_id,
                  username: item.username,
                  lastModify: item.last_modify,
                  name: item.semantic_specification.Name.Values,
                  description: item.semantic_specification.Description.Values,
                  dataType: item.semantic_specification.Data.Values[0],
                  taskType: item.semantic_specification.Task.Values[0],
                  libraryType: item.semantic_specification.Library.Values[0],
                  tagList: item.semantic_specification.Scenario.Values,
                })
              );
              pageNum.value = res.data.total_pages;
              return;
            }
            default: {
              throw new Error(res.msg);
            }
          }
        })
        .catch((err) => {
          console.error(err);
          loading.value = false;
          showError.value = true;
          clearTimeout(errorTimer.value);
          setTimeout(() => (showError.value = false), 2000);
          errorMsg.value = err.message;
        });
    });
}

function handleClickDelete(id) {
  dialog.value.confirm();
  deleteId.value = id;
  deleteName.value = learnwareItems.value.find((item) => item.id === id).name;
}

watch(
  () => isVerify.value,
  () => {
    page.value = 1;
    fetchByFilterAndPage(filters.value, page.value);
  }
)

watch(
  () => filters.value,
  () => (page.value = 1),
  { deep: true }
);

watch(
  () => page.value,
  () => {
    if (contentRef.value) {
      contentRef.value.scrollIntoView();
    }
  }
);

watch(
  () => [filters.value, page.value],
  (newVal) => {
    const [newFilters, newPage] = newVal;

    saveQuery();

    fetchByFilterAndPage(newFilters, newPage);
  },
  { deep: true }
);

onActivated(() => {
  contentRef.value.scrollTop = scrollTop.value;
  isVerify.value = route.query.is_verify !== "false";
  fetchByFilterAndPage(filters.value, page.value);
});

onMounted(() => {
  nextTick(() => {
    contentRef.value.addEventListener("scroll", () => {
      scrollTop.value = contentRef.value.scrollTop;
    });

    loadQuery();
  });
});
</script>

<template>
  <div class="search-container">
    <div class="filter">
      <v-switch
        v-model="isVerify"
        color="orange"
        :label="`${isVerify ? 'verified' : 'unverified'}`"
      />
      <div class="my-3 text-h6">Choose semantic specification</div>
      <div>
        <div class="mt-7 mb-3 text-h6 !text-1rem">Search by name</div>
        <v-text-field
          v-model="search"
          label="Type the words"
          hide-details=""
          append-inner-icon="mdi-close"
          @click:append-inner="search = ''"
        />
      </div>
      <data-type :cols="3" :md="2" :sm="2" :xs="2" v-model:value="dataType" />
      <task-type :cols="2" :md="2" :sm="2" :xs="2" v-model:value="taskType" />
      <library-type
        :cols="2"
        :md="2"
        :sm="2"
        :xs="2"
        v-model:value="libraryType"
      />
      <tag-list
        class="bg-transparent !text-1rem"
        v-model:value="tagList"
        :cols="2"
        :md="1"
        :sm="1"
      />
    </div>
    <div ref="contentRef" class="content">
      <v-scroll-y-transition class="fixed left-0 right-0 z-index-10">
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
      <v-scroll-y-transition class="fixed z-index-1000 left-2/10 right-2/10">
        <v-card-actions v-if="success">
          <v-alert
            closable
            text="Delete success"
            type="success"
            @click:close="success = false"
          />
        </v-card-actions>
      </v-scroll-y-transition>
      <page-learnware-list
        :items="learnwareItems"
        :filters="filters"
        @page-change="pageChange"
        :page="page"
        :page-num="pageNum"
        :page-size="pageSize"
        :loading="loading"
        :is-admin="true"
        :show-pagination="pageNum > 1"
        @click:delete="(id) => handleClickDelete(id)"
      />
    </div>

    <confirm-dialog ref="dialog" @confirm="() => deleteLearnware(deleteId)">
      <template #title>
        Confirm to delete &nbsp; <b>{{ deleteName }}</b
        >?
      </template>
      <template #text>
        The learnware <b>{{ deleteName }}</b> will be deleted in the learnware
        market <i>permanently</i>. Do you really want to delete?
      </template>
    </confirm-dialog>
  </div>
</template>

<style scoped lang="scss">
.search-container {
  @apply md: (fixed flex) mx-auto w-1/1;
  height: calc(100% - var(--v-layout-top));

  .filter {
    @apply p-2 w-1/1 md: (h-1/1 w-150 overflow-y-scroll) sm:px-5;

    * {
      @apply mt-2;
    }
  }

  .filter.hide {
    @apply h-0;
  }

  .content {
    @apply w-1/1 md: h-1/1 overflow-y-scroll;
  }
}
</style>