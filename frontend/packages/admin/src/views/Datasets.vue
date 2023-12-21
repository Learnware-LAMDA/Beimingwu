<script setup lang="ts">
import { ref, onActivated } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { fetchex } from "../utils";
import { BACKEND_URL } from "@main/constants";
import { useProgressedFetch } from "@main/request/utils";
import SubmitingDialog from "@main/components/Dialogs/SubmitingDialog.vue";

const store = useStore();
const router = useRouter();

const { t } = useI18n();

const showUploadDialog = ref(false);

const datasetFiles = ref<File[] | undefined>(undefined);
const remoteFolder = ref<string>("");
const submiting = ref(false);
const uploadProgress = ref(0);

const showError = ref(false);
const errorMsg = ref("");
const errorTimer = ref<number>();

const datasetItems = ref<string[]>([]);

const loading = ref(false);

function fetchItems(): Promise<void> {
  loading.value = true;
  showError.value = false;

  return fetchex(BACKEND_URL + "/datasets/list_datasets", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
  })
    .then((res) => {
      if (res && res.status === 200) {
        return res;
      }
      throw new Error("Network error");
    })
    .then((res) => res.json())
    .then(
      (res: {
        code: number;
        msg: string;
        data: {
          datasets: string[];
        };
      }) => {
        if (res.code === 0) {
          if (res.data && res.data.datasets) {
            return res;
          }
        }
        if (res.code === 11 || res.code === 12) {
          store.dispatch("logout");
          router.go(0);
        }
        throw new Error(res.msg);
      },
    )
    .then((res) => {
      datasetItems.value = res.data.datasets;
      loading.value = false;
    })
    .catch((err) => {
      loading.value = false;
      showError.value = true;
      errorMsg.value = err.message;
    });
}

function deleteDataset(dataset_name: string): Promise<void> {
  return fetchex(BACKEND_URL + "/datasets/delete_datasets", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      dataset: dataset_name,
    }),
  })
    .then((res) => {
      if (res && res.status === 200) {
        return res;
      }
      throw new Error("Network error");
    })
    .then((res) => res.json())
    .then((res: { code: number; msg: string }) => {
      if (res.code === 0) {
        return res;
      }
      throw new Error(res.msg);
    })
    .then(() => {
      store.commit("setShowGlobalError", true);
      store.commit("setGlobalErrorMsg", "Delete successfully.");

      fetchItems();
    })
    .catch((err) => {
      console.error(err);
      showError.value = true;
      errorMsg.value = err.message;
      clearTimeout(errorTimer.value);
      errorTimer.value = Number(
        setTimeout(() => {
          showError.value = false;
        }, 3000),
      );
    });
}

function downloadDataset(dataset_name: string): void {
  window.open(BACKEND_URL + "/datasets/download_datasets?dataset=" + dataset_name);
}

function onProgress(progress: number): void {
  uploadProgress.value = progress * 100;
}

function uploadDataset(): void {
  if (!datasetFiles.value || datasetFiles.value.length === 0) {
    showError.value = true;
    errorMsg.value = "Please select a dataset file.";
    clearTimeout(errorTimer.value);
    errorTimer.value = Number(
      setTimeout(() => {
        showError.value = false;
      }, 3000),
    );
    return;
  }

  const { progressedFetch } = useProgressedFetch(onProgress);

  const file = datasetFiles.value[0];

  const formData = new FormData();
  formData.append("file", file);
  formData.append("file_path", remoteFolder.value + "/" + file.name);

  submiting.value = true;
  showUploadDialog.value = false;

  progressedFetch(BACKEND_URL + "/datasets/upload_dataset", {
    method: "POST",
    body: formData,
  })
    .then((res: Response) => {
      if (res && res.status === 200) {
        return res;
      }
      throw new Error("Network error");
    })
    .then((res: Response) => res.json())
    .then((res: { code: number; msg: string }) => {
      submiting.value = false;
      if (res.code === 0) {
        return res;
      }
      throw new Error(res.msg);
    })
    .then(() => {
      store.commit("setShowGlobalError", true);
      store.commit("setGlobalErrorMsg", "Upload successfully.");

      fetchItems();
    })
    .catch((err: { message: string }) => {
      submiting.value = false;
      console.error(err);
      showError.value = true;
      errorMsg.value = err.message;
      clearTimeout(errorTimer.value);
      errorTimer.value = Number(
        setTimeout(() => {
          showError.value = false;
        }, 3000),
      );
    });
}

onActivated(() => {
  fetchItems();
});
</script>

<template>
  <div class="main-container">
    <v-dialog
      v-model="showUploadDialog"
      max-width="600"
    >
      <v-card>
        <v-card-title class="text-h5">
          {{ "Upload Dataset" }}
        </v-card-title>
        <v-card-text>
          <div class="flat">
            {{ "Remote Folder" }}
            <v-text-field
              v-model="remoteFolder"
              label="Remote Folder"
              hint="The remote folder to store the dataset."
              single-line
            />
          </div>
        </v-card-text>
        <v-card-text>
          {{ "Dataset File" }}
          <v-file-input
            v-model="datasetFiles"
            :rules="[(v) => !!v || 'File is required']"
            label="Dataset"
            variant="outlined"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="blue-darken-1"
            @click="showUploadDialog = false"
          >
            {{ "Cancel" }}
          </v-btn>
          <v-btn
            color="blue-darken-1"
            @click="uploadDataset"
          >
            {{ "Upload" }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-scroll-y-transition class="fixed left-0 right-0 z-50">
      <v-card-actions v-if="showError">
        <v-alert
          class="mx-auto w-full max-w-[900px]"
          closable
          :text="errorMsg"
          type="error"
          @click:close="showError = false"
        />
      </v-card-actions>
    </v-scroll-y-transition>
    <v-card
      flat
      class="search"
    >
      <v-card-actions>
        <div>
          <v-btn
            append-icon="mdi-upload"
            variant="outlined"
            @click="showUploadDialog = true"
          >
            {{ "Upload Dataset" }}
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
    <submiting-dialog
      v-if="submiting"
      :progress="uploadProgress"
    >
      <template #title>
        <span>{{ "Uploading" }}</span>
      </template>
    </submiting-dialog>
    <div
      class="user-list-container bg-surface dark:bg-surface-dark"
      :class="datasetItems.length === 0 ? ['grid-cols-1', 'h-full'] : null"
      :style="{ gridTemplateColumns: `repeat(2, minmax(0, 1fr))` }"
    >
      <TransitionGroup name="fade">
        <div
          v-if="datasetItems && datasetItems.length > 0"
          flat
          class="item"
        >
          <div class="row">
            <div class="columns">
              <div class="my-title">
                {{ "Dataset Files" }}
              </div>
            </div>
            <v-card-actions class="actions">
              <v-btn
                class="opacity-0"
                icon="mdi-lock-reset"
              />
              <v-btn
                class="opacity-0"
                icon="mdi-lock-reset"
              />
            </v-card-actions>
          </div>
        </div>
        <div
          v-for="(item, i) in datasetItems"
          :key="i"
          class="item"
        >
          <div class="row">
            <div class="columns">
              <div class="my-title">
                {{ item }}
              </div>
            </div>
            <v-card-actions class="actions">
              <v-btn
                icon="mdi-download"
                @click.stop="() => downloadDataset(item)"
              />
              <v-btn
                icon="mdi-delete"
                @click.stop="() => deleteDataset(item)"
              />
            </v-card-actions>
          </div>
        </div>
      </TransitionGroup>
    </div>
    <div
      v-if="datasetItems.length === 0"
      flat
      class="no-user"
    >
      <oops-img
        class="oops-img block"
        width="100"
        height="100"
      />
      {{ t("Dataset.OopsNoUser") }}
    </div>
  </div>
</template>

<style scoped lang="scss">
.main-container {
  @apply mx-auto h-full w-full max-w-[1500px] overflow-hidden;

  .search {
    @apply mt-3 w-full max-w-[1500px] border;

    .table-action {
      @apply grid grid-cols-2;
    }
  }
}

.user-list-container {
  @apply relative p-1;

  .item:nth-child(1) {
    @apply hidden border-t sm:block;

    .columns {
      @apply font-bold;
    }
  }

  .item:nth-child(2) {
    @apply border-t sm:border-t-0;
  }

  .item {
    @apply border border-t-0 px-3 py-3 sm:py-0;

    .row {
      @apply flex items-center;

      .columns {
        @apply grid w-full sm:grid-cols-[3fr,3fr,1fr,1fr,1fr];

        .my-title {
          @apply text-sm sm:flex sm:flex-col sm:items-start sm:justify-center lg:text-lg xl:text-base;
          .link {
            @apply underline;
          }
          .small-title {
            @apply font-bold sm:hidden;
          }
        }
      }

      .actions {
        @apply justify-end p-0;
      }
    }
  }

  .no-user {
    @apply bottom-0 flex w-full flex-col items-center justify-center text-2xl;

    .oops-img {
      @apply mx-auto fill-gray-800 dark:fill-gray-300;
    }
  }
}
</style>
