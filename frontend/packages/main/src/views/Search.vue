<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { useDisplay } from "vuetify";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { searchLearnware } from "../request/engine";
import { deleteLearnware } from "../request/admin";
import ConfirmDialog from "../components/Dialogs/ConfirmDialog.vue";
import UserRequirement from "../components/Search/UserRequirement.vue";
import PageLearnwareList from "../components/Learnware/PageLearnwareList.vue";
import MultiRecommendedLearnwareList from "../components/Learnware/MultiRecommendedLearnwareList.vue";
import type { Filter, LearnwareCardInfo } from "@beiming-system/types/learnware";
import { promiseReadFile } from "../utils";

export interface SearchProps {
  isAdmin?: boolean;
}

withDefaults(defineProps<SearchProps>(), {
  isAdmin: false,
});

const display = useDisplay();

const route = useRoute();
const router = useRouter();

const { t } = useI18n();

const filters = ref<Filter>({
  id: "",
  name: "",
  dataType: "",
  taskType: "",
  libraryType: "",
  scenarioList: [],
  files: [],
  dataTypeDescription: { Dimension: 0, Description: {} },
  taskTypeDescription: { Dimension: 0, Description: {} },
});

const multiRecommendedLearnwareItems = ref<LearnwareCardInfo[]>([]);
const multiRecommendedMatchScore = ref<number>(0);
const singleRecommendedLearnwarePage = ref(1);
const singleRecommendedLearnwarePageNum = ref(1);
const singleRecommendedLearnwarePageSize = ref(Math.ceil(display.height.value / 900) * 10);
const singleRecommendedLearnwareItems = ref<LearnwareCardInfo[]>([]);
const isHeterogeneous = ref<boolean>(false);
const rkmeTypeTable = ref<boolean>(false);
const loading = ref(false);
const isVerified = ref(route.query.is_verified ? route.query.is_verified === "true" : true);

const showError = ref(false);
const errorMsg = ref("");
const errorTimer = ref();

const dialog = ref<InstanceType<typeof ConfirmDialog>>();
const deleteId = ref("");
const deleteName = ref("");

const anchorRef = ref<HTMLElement>();

const showMultiRecommended = computed(
  () =>
    multiRecommendedLearnwareItems.value &&
    multiRecommendedLearnwareItems.value.length > 1 &&
    singleRecommendedLearnwarePage.value === 1,
);
const multiRecommendedTips = ref(true);
const singleRecommendedTips = ref(true);

const showHeterogeneousSearchSwitch = computed(
  () =>
    singleRecommendedLearnwareItems.value?.length === 0 &&
    multiRecommendedLearnwareItems.value?.length === 0 &&
    ["Classification", "Regression"].includes(filters.value.taskType) &&
    rkmeTypeTable.value,
);

function pageChange(newPage: number): void {
  singleRecommendedLearnwarePage.value = newPage;
}

function fetchByFilterAndPage(
  filters: Filter,
  page: number,
  isVerified: boolean = false,
  isHeterogeneous: boolean = false,
): void {
  showError.value = false;
  loading.value = true;

  searchLearnware({
    id: filters.id,
    name: filters.name,
    dataType: filters.dataType,
    taskType: filters.taskType,
    libraryType: filters.libraryType,
    scenarioList: filters.scenarioList,
    files: filters.files,
    isVerified,
    input: isHeterogeneous ? filters.dataTypeDescription : undefined,
    output: isHeterogeneous ? filters.taskTypeDescription : undefined,
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
            scenarioList: item.semantic_specification.Scenario.Values,
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
            scenarioList: item.semantic_specification.Scenario.Values,
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

function handleConfirmDeleteLearnware(id: string): void {
  showError.value = false;

  deleteLearnware(id)
    .then((res) => {
      switch (res.code) {
        case 0: {
          fetchByFilterAndPage(
            filters.value,
            singleRecommendedLearnwarePage.value - 1,
            isVerified.value,
          );
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
  if (dialog.value) {
    dialog.value.confirm();
    deleteId.value = id;
    deleteName.value = (
      singleRecommendedLearnwareItems.value.find((item) => item.id === id) as { name: string }
    ).name;
  }
}

watch(
  () => singleRecommendedLearnwarePage.value,
  () => {
    if (display.smAndDown.value) {
      if (anchorRef.value) {
        const layoutTop = Number(
          getComputedStyle(anchorRef.value).getPropertyValue("--v-layout-top").replace("px", ""),
        );
        const offset = anchorRef.value?.offsetTop - layoutTop;
        if (offset) {
          window.scrollTo(0, offset);
        }
      }
    } else {
      window.scrollTo(0, 0);
    }
  },
);

watch(
  () => filters.value,
  () => {
    singleRecommendedLearnwarePage.value = 1;
  },
  { deep: true },
);

watch(
  () => [
    filters.value,
    singleRecommendedLearnwarePage.value,
    isVerified.value,
    isHeterogeneous.value,
  ],
  (newVal) => {
    const [newFilters, newPage, newIsVerified, newIsHeterogeneous] = newVal as [
      Filter,
      number,
      boolean,
      boolean,
    ];

    fetchByFilterAndPage(newFilters, newPage - 1, newIsVerified, newIsHeterogeneous);
  },
  { deep: true },
);

watch(
  () => filters.value.files,
  (newVal) => {
    rkmeTypeTable.value = false;
    if (newVal.length > 0) {
      promiseReadFile(newVal[0])
        .then((res: ArrayBuffer) => new TextDecoder("ascii").decode(res))
        .then((res) => JSON.parse(res))
        .then((res) => {
          if (!res.type || res.type === "RKMETableSpecification") {
            rkmeTypeTable.value = true;
          }
        })
        .catch((err) => {
          console.error(err);
        });
    }
  },
  { deep: true },
);

watch(
  () => isVerified.value,
  (newVal) => {
    router.replace({
      path: route.path,
      query: {
        is_verified: String(newVal),
      },
    });
  },
);

function init(): void {
  fetchByFilterAndPage(
    filters.value,
    singleRecommendedLearnwarePage.value - 1,
    isVerified.value,
    isHeterogeneous.value,
  );
}

onMounted(() => init());
</script>

<template>
  <div class="mx-auto w-full lg:flex">
    <v-scroll-y-transition>
      <div v-if="showError" class="fixed z-10 w-full">
        <v-alert
          class="z-10 mx-auto max-w-[900px]"
          closable
          :text="errorMsg"
          type="error"
          @click:close="showError = false"
        />
      </div>
    </v-scroll-y-transition>

    <div class="w-full lg:max-w-[460px]">
      <user-requirement
        v-model="filters"
        class="bottom-0 w-full lg:fixed lg:max-w-[460px]"
        style="top: var(--v-layout-top)"
        :is-admin="isAdmin"
        :is-heterogeneous="isHeterogeneous"
      >
        <template #prepend>
          <v-btn
            v-if="isHeterogeneous"
            block
            variant="outlined"
            color="red"
            @click="() => (isHeterogeneous = false)"
          >
            {{ t("Search.TurnOffHeterogeneousSearch") }}
          </v-btn>
          <v-btn
            v-if="isAdmin"
            block
            class="mr-2"
            :color="isVerified ? 'primary' : 'error'"
            @click="() => (isVerified = !isVerified)"
          >
            {{ isVerified ? t("AllLearnware.ShowVerified") : t("AllLearnware.ShowUnverified") }}
          </v-btn>
        </template>
      </user-requirement>
    </div>

    <div ref="anchorRef" class="flex-1">
      <v-card v-if="showMultiRecommended" flat class="mt-4 bg-transparent sm:m-2">
        <v-card-title v-if="!multiRecommendedTips">
          {{ t("Search.RecommendedMultipleLearnware") }}
        </v-card-title>
        <v-card-text v-if="multiRecommendedTips" class="!p-2">
          <v-alert
            v-model="multiRecommendedTips"
            :title="t('Search.RecommendedMultipleLearnware')"
            :text="t('Search.RecommendedMultipleLearnwareTips')"
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
      <v-card flat class="mt-4 bg-transparent sm:m-2">
        <v-card-title v-if="showMultiRecommended && !singleRecommendedTips">
          {{ t("Search.RecommendedSingleLearnware") }}
        </v-card-title>
        <v-card-text v-if="showMultiRecommended && singleRecommendedTips" class="!p-2">
          <v-alert
            v-model="singleRecommendedTips"
            :title="t('Search.RecommendedSingleLearnware')"
            :text="t('Search.RecommendedSingleLearnwareTips')"
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
          :is-admin="isAdmin"
          :show-pagination="singleRecommendedLearnwarePageNum > 1"
          @page-change="pageChange"
          @click:edit="(id) => handleClickEdit(id)"
          @click:delete="(id) => handleClickDelete(id)"
        />
      </v-card>

      <div v-if="showHeterogeneousSearchSwitch && !isHeterogeneous" class="text-center">
        <v-btn class="px-8" variant="outlined" color="red" @click="() => (isHeterogeneous = true)">
          {{ t("Search.HeterogeneousSearch") }}
        </v-btn>
      </div>
    </div>

    <confirm-dialog ref="dialog" @confirm="() => handleConfirmDeleteLearnware(deleteId)">
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
