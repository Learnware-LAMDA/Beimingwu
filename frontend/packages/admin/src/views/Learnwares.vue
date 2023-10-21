<script setup lang="ts">
import { ref, watch, onMounted, nextTick, onActivated } from "vue";
import { useDisplay } from "vuetify";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { fetchex } from "../utils/fetchex";
import UserRequirement from "@main/components/Search/UserRequirement.vue";
import PageLearnwareList from "@main/components/Learnware/PageLearnwareList.vue";
import ConfirmDialog from "@/components/Dialogs/ConfirmDialog.vue";
import type { Filter, LearnwareCardInfo } from "@beiming-system/types/learnware";

const display = useDisplay();

const router = useRouter();

const { t } = useI18n();

const dialog = ref<InstanceType<typeof ConfirmDialog>>();
const deleteId = ref("");
const deleteName = ref("");

const filters = ref<Filter>({
  name: "",
  dataType: "",
  taskType: "",
  libraryType: "",
  tagList: [],
  files: [],
});

const page = ref(1);
const pageSize = ref(Math.ceil(display.height.value / 900) * 10);
const pageNum = ref(1);
const learnwareItems = ref<LearnwareCardInfo[]>([]);
const isVerify = ref(true);

const loading = ref(false);

const contentRef = ref<HTMLElement | null>(null);

const scrollTop = ref(0);

const success = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const successTimer = ref<string | number | undefined>();
const errorTimer = ref<string | number | undefined>();

function deleteLearnware(id: string): void {
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
      if (res && res.status === 200) {
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
            1,
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

function pageChange(newPage: number): void {
  page.value = newPage;
  contentRef.value && (contentRef.value.scrollTop = 0);
}

function fetchLearnware(
  isVerify: boolean,
  page: number,
  limit: number,
  fd: FormData,
): Promise<Response | undefined> {
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

function fetchByFilterAndPage(filters: Filter, page: number): void {
  if (contentRef.value) {
    contentRef.value.scrollTop = 0;
  }

  showError.value = false;
  loading.value = true;

  fetchex("/api/engine/semantic_specification")
    .then((res) => {
      if (res) {
        return res.json();
      }
      throw new Error("Network error");
    })
    .then((res) => {
      const semanticSpec = res.data.semantic_specification;
      semanticSpec.Name.Values = filters.name;
      semanticSpec.Data.Values = filters.dataType ? [filters.dataType] : [];
      semanticSpec.Task.Values = filters.taskType ? [filters.taskType] : [];
      semanticSpec.Library.Values = filters.libraryType ? [filters.libraryType] : [];
      semanticSpec.Scenario.Values = filters.tagList;
      semanticSpec.Description.Values = "";

      const fd = new FormData();
      fd.append("semantic_specification", JSON.stringify(semanticSpec));
      fd.append("statistical_specification", "");
      fd.append("limit", String(pageSize.value));
      fd.append("page", String(page - 1));
      return fd;
    })
    .then((fd) => {
      return fetchLearnware(isVerify.value, page, pageSize.value, fd)
        .then((res) => {
          if (res && res.status === 200) {
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
                (item: {
                  learnware_id: string;
                  username: string;
                  last_modify: string;
                  semantic_specification: {
                    Name: { Values: string };
                    Description: { Values: string };
                    Data: { Values: string[] };
                    Task: { Values: string[] };
                    Library: { Values: string[] };
                    Scenario: { Values: string[] };
                  };
                }) => ({
                  id: item.learnware_id,
                  username: item.username,
                  lastModify: item.last_modify,
                  name: item.semantic_specification.Name.Values,
                  description: item.semantic_specification.Description.Values,
                  dataType: item.semantic_specification.Data.Values[0],
                  taskType: item.semantic_specification.Task.Values[0],
                  libraryType: item.semantic_specification.Library.Values[0],
                  tagList: item.semantic_specification.Scenario.Values,
                }),
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

function handleClickEdit(id: string): void {
  router.push({
    path: "/submit",
    query: {
      edit: "true",
      id,
    },
  });
}

function handleClickDelete(id: string): void {
  dialog.value.confirm();
  deleteId.value = id;
  deleteName.value = (learnwareItems.value.find((item) => item.id === id) as { name: string }).name;
}

watch(
  () => filters.value,
  () => {
    page.value = 1;
  },
  { deep: true },
);

watch(
  () => isVerify.value,
  () => {
    page.value = 1;
    fetchByFilterAndPage(filters.value, page.value);
  },
);

watch(
  () => filters.value,
  () => (page.value = 1),
  { deep: true },
);

watch(
  () => page.value,
  () => {
    if (contentRef.value) {
      contentRef.value.scrollIntoView();
    }
  },
);

watch(
  () => [filters.value, page.value],
  (newVal) => {
    const [newFilters, newPage] = newVal as [Filter, number];

    fetchByFilterAndPage(newFilters, newPage);
  },
  { deep: true },
);

onActivated(() => {
  if (contentRef.value) {
    contentRef.value.scrollTop = scrollTop.value;
  }
  fetchByFilterAndPage(filters.value, page.value);
});

onMounted(() => {
  nextTick(() => {
    if (contentRef.value) {
      contentRef.value.addEventListener("scroll", () => {
        if (contentRef.value) scrollTop.value = contentRef.value.scrollTop;
      });
    }
  });
});
</script>

<template>
  <div class="search-container">
    <user-requirement v-model:value="filters" class="max-w-[450px]">
      <template #prepend>
        <v-btn
          block
          class="mr-2"
          :color="isVerify ? 'primary' : 'error'"
          @click="() => (isVerify = !isVerify)"
        >
          {{ isVerify ? t("AllLearnware.ShowVerified") : t("AllLearnware.ShowUnverified") }}
        </v-btn>
      </template>
    </user-requirement>

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
          <v-alert closable text="Delete success" type="success" @click:close="success = false" />
        </v-card-actions>
      </v-scroll-y-transition>
      <page-learnware-list
        :items="learnwareItems"
        :filters="filters"
        :page="page"
        :page-num="pageNum"
        :page-size="pageSize"
        :loading="loading"
        :is-admin="true"
        :show-pagination="pageNum > 1"
        @page-change="pageChange"
        @click:edit="(id) => handleClickEdit(id)"
        @click:delete="(id) => handleClickDelete(id)"
      />
    </div>

    <confirm-dialog ref="dialog" @confirm="() => deleteLearnware(deleteId)">
      <template #title>
        Confirm to delete &nbsp; <b>{{ deleteName }}</b
        >?
      </template>
      <template #text>
        The learnware <b>{{ deleteName }}</b> will be deleted in the learnware market
        <i>permanently</i>. Do you really want to delete?
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
