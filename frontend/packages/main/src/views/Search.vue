<script setup lang="ts">
import { ref, computed, onMounted, onActivated, watch } from "vue";
import { watchDebounced } from "@vueuse/core";
import { useDisplay } from "vuetify";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { marked } from "marked";
import { searchLearnware } from "../request/engine";
import { deleteLearnware } from "../request/admin";
import ConfirmDialog from "../components/Dialogs/ConfirmDialog.vue";
import UserRequirement from "../components/Search/UserRequirement.vue";
import PageLearnwareList from "../components/Learnware/PageLearnwareList.vue";
import MultiRecommendedLearnwareList from "../components/Learnware/MultiRecommendedLearnwareList.vue";
import type { Filter, LearnwareCardInfo } from "@beiming-system/types/learnware";
import { downloadLearnwareSync, promiseReadFile } from "../utils";

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
  licenseList: [],
  files: [],
  inputDescription: { Dimension: 0, Description: {} },
  outputDescription: { Dimension: 0, Description: {} },
});

const multiRecommendedLearnwareItems = ref<LearnwareCardInfo[]>([]);
const multiRecommendedMatchScore = ref<number>(0);
const singleRecommendedLearnwarePage = ref(1);
const singleRecommendedLearnwarePageNum = ref(1);
const singleRecommendedLearnwarePageSize = ref(Math.ceil(display.height.value / 900) * 10);
const singleRecommendedLearnwareItems = ref<LearnwareCardInfo[]>([]);

const rkmeTypeTable = ref<boolean>(false);
const loading = ref(false);
const isVerified = ref<boolean>(true);

const showError = ref(false);
const errorMsg = ref("");
const errorTimer = ref();

const isShowDeployTips = ref(false);
const isShownDeployTips = ref(false);

const showDialog = ref(false);
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

const isHetero = ref<boolean>(false);
const allowHetero = computed(
  () => ["", "Table"].includes(filters.value.dataType) && rkmeTypeTable.value,
);
const heteroDialog = ref<boolean>(false);
const remindHetero = computed(
  () =>
    !loading.value &&
    allowHetero.value &&
    !isHetero.value &&
    multiRecommendedLearnwareItems.value.length === 0 &&
    singleRecommendedLearnwareItems.value.length === 0,
);
const heteroNotWorking = ref<boolean>(false);

function pageChange(newPage: number): void {
  singleRecommendedLearnwarePage.value = newPage;
}

function fetchByFilterAndPage(
  filters: Filter,
  page: number,
  isVerified: boolean = false,
  isHetero: boolean = false,
): void {
  showError.value = false;
  loading.value = true;

  heteroNotWorking.value = false;
  multiRecommendedLearnwareItems.value = [];
  singleRecommendedLearnwareItems.value = [];
  singleRecommendedLearnwarePageNum.value = 1;

  searchLearnware({
    id: filters.id,
    name: filters.name,
    dataType: filters.dataType,
    taskType: filters.taskType,
    libraryType: filters.libraryType,
    scenarioList: filters.scenarioList,
    licenseList: filters.licenseList,
    files: filters.files,
    isVerified,
    input: isHetero ? filters.inputDescription : undefined,
    output: isHetero ? filters.outputDescription : undefined,
    page,
    limit: singleRecommendedLearnwarePageSize.value,
  })
    .then((res) => {
      switch (res.code) {
        case 0: {
          if (isHetero && !res.data.is_hetero) {
            heteroNotWorking.value = true;
            return;
          }

          multiRecommendedLearnwareItems.value = res.data.learnware_list_multi.map((item) => ({
            id: item.learnware_id,
            username: item.username,
            lastModify: item.last_modify,
            name: item.semantic_specification.Name.Values,
            description:
              new DOMParser().parseFromString(
                marked(item.semantic_specification.Description.Values, { async: false }) as string,
                "text/html",
              ).body.textContent ?? "",
            dataType: item.semantic_specification.Data.Values[0],
            taskType: item.semantic_specification.Task.Values[0],
            libraryType: item.semantic_specification.Library.Values[0],
            scenarioList: item.semantic_specification.Scenario.Values,
            licenseList: item.semantic_specification.License.Values,
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
            description:
              new DOMParser().parseFromString(
                marked(item.semantic_specification.Description.Values, { async: false }) as string,
                "text/html",
              ).body.textContent ?? "",
            dataType: item.semantic_specification.Data.Values[0],
            taskType: item.semantic_specification.Task.Values[0],
            libraryType: item.semantic_specification.Library.Values[0],
            scenarioList: item.semantic_specification.Scenario.Values,
            licenseList: item.semantic_specification.License.Values,
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
            isHetero.value,
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

function handleClickDownload(id: string): void {
  if (id) {
    downloadLearnwareSync(id);

    showDeployTips();
  }
}

function showDeployTips(): void {
  if (!isShownDeployTips.value) {
    isShownDeployTips.value = true;
    isShowDeployTips.value = true;
  }
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
  showDialog.value = true;
  deleteId.value = id;
  deleteName.value = (
    singleRecommendedLearnwareItems.value.find((item) => item.id === id) as { name: string }
  ).name;
}

watchDebounced(
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
  { debounce: 300 },
);

watchDebounced(
  () => filters.value,
  () => {
    singleRecommendedLearnwarePage.value = 1;
  },
  { deep: true, debounce: 300 },
);

watchDebounced(
  () => [filters.value, singleRecommendedLearnwarePage.value, isVerified.value, isHetero.value],
  (newVal) => {
    const [newFilters, newPage, newIsVerified, newIsHetero] = newVal as [
      Filter,
      number,
      boolean,
      boolean,
    ];

    fetchByFilterAndPage(newFilters, newPage - 1, newIsVerified, newIsHetero);
  },
  { deep: true, debounce: 300 },
);

watchDebounced(
  () => filters.value.files,
  (newVal) => {
    if (newVal.length > 0) {
      return promiseReadFile(newVal[0])
        .then((res: ArrayBuffer) => new TextDecoder("ascii").decode(res))
        .then((res) => JSON.parse(res))
        .then((res) => {
          if (!res.type || res.type === "RKMETableSpecification") {
            rkmeTypeTable.value = true;
          } else {
            rkmeTypeTable.value = false;
          }
        })
        .catch((err) => {
          console.error(err);
        });
    } else {
      rkmeTypeTable.value = false;
    }
  },
  { debounce: 300 },
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

watch(
  () => allowHetero.value,
  (newVal) => {
    if (!newVal) {
      isHetero.value = false;
    }
  },
);

function init(): void {
  fetchByFilterAndPage(
    filters.value,
    singleRecommendedLearnwarePage.value - 1,
    isVerified.value,
    isHetero.value,
  );
}

onMounted(() => init());

onActivated(() => {
  isVerified.value = route.query.is_verified ? route.query.is_verified === "true" : true;
});
</script>

<template>
  <div class="mx-auto w-full lg:flex">
    <v-scroll-y-transition>
      <div
        v-if="showError"
        class="fixed z-10 w-full"
      >
        <v-alert
          class="z-10 mx-auto max-w-[900px]"
          closable
          :text="errorMsg"
          type="error"
          @click:close="showError = false"
        />
      </div>

      <div
        v-if="isShowDeployTips"
        class="fixed z-10 w-full"
      >
        <v-alert
          class="mx-auto max-w-[900px] text-sm md:text-base"
          :density="display.mdAndUp.value ? 'default' : 'compact'"
          closable
          type="info"
          @click:close="isShowDeployTips = false"
        >
          <a
            class="underline"
            :href="t('Url.Docs.DeployLearnwareGuide')"
            target="_blank"
          >
            {{ t("Search.ClickHere") }}
          </a>
          {{ t("Search.ToLearnHowToDeployTheLearnware") }}
        </v-alert>
      </div>
    </v-scroll-y-transition>

    <div class="w-full lg:max-w-[460px]">
      <user-requirement
        v-model="filters"
        v-model:allow-hetero="allowHetero"
        v-model:is-hetero="isHetero"
        v-model:hetero-dialog="heteroDialog"
        class="bottom-0 w-full lg:fixed lg:max-w-[460px]"
        style="top: var(--v-layout-top)"
        :is-admin="isAdmin"
      >
        <template #prepend>
          <v-btn
            v-if="isAdmin"
            block
            :color="isVerified ? 'primary' : 'error'"
            @click="() => (isVerified = !isVerified)"
          >
            {{ isVerified ? t("AllLearnware.ShowVerified") : t("AllLearnware.ShowUnverified") }}
          </v-btn>
        </template>
      </user-requirement>
    </div>

    <div
      ref="anchorRef"
      class="flex-1"
    >
      <div v-if="heteroNotWorking">
        <v-alert
          type="info"
          class="mx-auto max-w-[600px]"
        >
          {{ t("Search.HeterogeneousNotWorkingTips") }}
          <a
            class="underline"
            :href="t('Url.Docs.HeteroSearchGuide')"
            target="_blank"
          >
            {{ t("Search.HeterogeneousNotWorkingTips2") }}
          </a>
        </v-alert>
      </div>

      <div
        v-if="showMultiRecommended"
        flat
        class="mt-4 bg-transparent sm:mt-2"
      >
        <div
          v-if="multiRecommendedTips"
          class="px-2"
        >
          <v-alert
            v-model="multiRecommendedTips"
            closable
            color="success"
          >
            <template #prepend>
              <v-icon
                icon="mdi-hexagon-multiple"
                :size="display.smAndUp.value ? 'large' : 'small'"
              />
            </template>
            <template #title>
              <span class="text-base md:text-xl">
                {{ t("Search.RecommendedMultipleLearnware") }}</span
              >
            </template>
            <template #text>
              <span class="text-xs leading-tight md:text-base">
                {{ t("Search.RecommendedMultipleLearnwareTips") }}
              </span>
            </template>
          </v-alert>
        </div>
        <div
          v-else
          class="p-2 text-base font-medium md:text-xl"
        >
          <v-icon>mdi-hexagon-multiple</v-icon>
          {{ t("Search.RecommendedMultipleLearnware") }}
        </div>
        <multi-recommended-learnware-list
          :items="multiRecommendedLearnwareItems"
          :match-score="multiRecommendedMatchScore"
          :filters="filters"
          :loading="loading"
          @page-change="pageChange"
          @download="() => showDeployTips()"
        />
      </div>

      <div
        flat
        class="mt-4 bg-transparent sm:m-0"
      >
        <template v-if="showMultiRecommended">
          <div
            v-if="singleRecommendedTips"
            class="px-2 py-0"
          >
            <v-alert
              v-model="singleRecommendedTips"
              closable
              color="info"
            >
              <template #prepend>
                <v-icon
                  icon="mdi-hexagon"
                  :size="display.smAndUp.value ? 'x-large' : 'default'"
                />
              </template>
              <template #title>
                <span class="text-base md:text-xl">
                  {{ t("Search.RecommendedSingleLearnware") }}
                </span>
              </template>
              <template #text>
                <span class="text-xs md:text-base">
                  {{ t("Search.RecommendedSingleLearnwareTips") }}
                </span>
              </template>
            </v-alert>
          </div>
          <div
            v-else
            class="p-2 text-base font-medium md:text-xl"
          >
            <v-icon>mdi-hexagon</v-icon>
            {{ t("Search.RecommendedSingleLearnware") }}
          </div>
        </template>
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
          @click:download="(id) => handleClickDownload(id)"
          @click:edit="(id) => handleClickEdit(id)"
          @click:delete="(id) => handleClickDelete(id)"
        />
      </div>

      <div
        v-if="remindHetero"
        class="text-center"
      >
        <v-btn
          class="px-8"
          variant="flat"
          color="primary"
          @click="() => (heteroDialog = true)"
        >
          {{ t("Search.StartHeterogeneousSearch") }}
        </v-btn>
      </div>
    </div>

    <confirm-dialog
      v-model="showDialog"
      @confirm="() => handleConfirmDeleteLearnware(deleteId)"
    >
      <template #title>
        <div class="ml-1 flex-1 overflow-hidden text-ellipsis">
          {{ t("MyLearnware.ConfirmToDelete") }}
        </div>
      </template>
      <template #text>
        {{ t("AllLearnware.Learnware") }} <b>{{ deleteName }}</b>
        {{ t("MyLearnware.DeleteContinue") }}
      </template>
    </confirm-dialog>
  </div>
</template>
