<script setup lang="ts">
import { ref, onMounted, nextTick, watch, onActivated } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { deleteLearnware, getLearnwareList } from "../request/user";
import { listLearnware } from "../request/admin";
import PageLearnwareList from "../components/Learnware/PageLearnwareList.vue";
import ConfirmDialog from "../components/Dialogs/ConfirmDialog.vue";
import { Learnware } from "types";
import { LearnwareDetailInfo } from "types/response";

const store = useStore();

const route = useRoute();
const router = useRouter();

const dialog = ref<InstanceType<typeof ConfirmDialog>>();
const deleteId = ref("");
const deleteName = ref("");

const learnwareItems = ref<Learnware.LearnwareCardInfo[]>([]);
const page = ref<number>(1);
const pageNum = ref<number>(1);
const pageSize = ref<number>(10);

const loading = ref(false);

const contentRef = ref<HTMLDivElement | null>(null);
const scrollTop = ref(0);

const showError = ref(false);
const errorMsg = ref("");

function handleConfirm(): Promise<void> {
  showError.value = false;

  return deleteLearnware({ id: deleteId.value })
    .then((res) => {
      switch (res.code) {
        case 0: {
          learnwareItems.value.splice(
            learnwareItems.value.findIndex((item) => item.id === deleteId.value),
            1,
          );
          fetchByFilterAndPage(page.value);
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
    });
}

function pageChange(newPage: number): void {
  page.value = newPage;
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
  dialog.value && dialog.value.confirm();
  deleteId.value = id;
  deleteName.value = learnwareItems.value.find((item) => item.id === id)?.name as string;
}

function fetchByFilterAndPage(page: number): void {
  if (contentRef.value) {
    contentRef.value.scrollTop = 0;
  }

  showError.value = false;
  loading.value = true;

  interface ResponseType {
    code: number;
    msg: string;
    data: {
      learnware_list: LearnwareDetailInfo[];
      page: number;
      limit: number;
      total_pages: number;
    };
  }
  let getLearnwareListAPI: () => Promise<ResponseType>;
  if (route.query.user_id) {
    getLearnwareListAPI = (): Promise<ResponseType> =>
      listLearnware({
        page: page - 1,
        limit: pageSize.value,
        userId: route.query.user_id?.toString() as string,
      });
  } else {
    getLearnwareListAPI = (): Promise<ResponseType> =>
      getLearnwareList({
        page: page - 1,
        limit: pageSize.value,
      });
  }

  getLearnwareListAPI()
    .then((res) => {
      switch (res.code) {
        case 0: {
          loading.value = false;
          learnwareItems.value = res.data.learnware_list.map((item) => ({
            id: item.learnware_id,
            verifyStatus: item.verify_status,
            lastModify: item.last_modify,
            name: item.semantic_specification.Name.Values,
            description: item.semantic_specification.Description.Values,
            dataType: item.semantic_specification.Data.Values[0],
            taskType: item.semantic_specification.Task.Values[0],
            libraryType: item.semantic_specification.Library.Values[0],
            tagList: item.semantic_specification.Scenario.Values,
          }));
          pageNum.value = res.data.total_pages;
          console.log(pageNum.value);
          return;
        }
        case 11: {
          store.commit("setLoggedIn", false);
          setTimeout(() => {
            router.push("/login");
          }, 1000);
          break;
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
    });
}

watch(
  () => page.value,
  (newPage) => {
    fetchByFilterAndPage(newPage);
  },
  { deep: true },
);

onActivated(() => {
  contentRef.value && (contentRef.value.scrollTop = scrollTop.value);
  fetchByFilterAndPage(page.value);
});

onMounted(() => {
  nextTick(() => {
    contentRef.value &&
      contentRef.value.addEventListener("scroll", () => {
        contentRef.value && (scrollTop.value = contentRef.value.scrollTop);
      });
    fetchByFilterAndPage(page.value);
  });
});
</script>

<template>
  <div ref="contentRef" class="fixed learnware-container">
    <confirm-dialog ref="dialog" @confirm="handleConfirm">
      <template #title>
        Confirm to delete &nbsp; <b>{{ deleteName }}</b
        >?
      </template>
      <template #text>
        Your learnware <b>{{ deleteName }}</b> will be deleted in the learnware market
        <i>permanently</i>. Do you really want to delete?
      </template>
    </confirm-dialog>
    <v-scroll-y-transition>
      <v-card-actions v-if="showError">
        <v-alert closable :text="errorMsg" type="error" @click:close="showError = false" />
      </v-card-actions>
    </v-scroll-y-transition>
    <div class="w-1/1 max-w-900px">
      <page-learnware-list
        :show-pagination="pageNum > 1"
        :items="learnwareItems"
        :page="page"
        :page-num="pageNum"
        :page-size="pageSize"
        :loading="loading"
        :cols="1"
        :is-admin="true"
        @page-change="pageChange"
        @click:edit="(id) => handleClickEdit(id)"
        @click:delete="(id) => handleClickDelete(id)"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.learnware-container {
  @apply flex flex-col w-1/1 overflow-y-scroll justify-start items-center;
}
.fixed {
  height: calc(100% - var(--v-layout-top));
}
</style>
