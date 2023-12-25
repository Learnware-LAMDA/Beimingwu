<script setup lang="ts">
import { ref, computed, onActivated } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { fetchex } from "../utils";
import { useField } from "@beiming-system/hooks";
import { BACKEND_URL } from "@main/constants";
import { useProgressedFetch } from "@main/request/utils";
import FileUpload from "@main/components/Specification/FileUpload.vue";
import SubmitingDialog from "@main/components/Dialogs/SubmitingDialog.vue";
import ConfirmDialog from "@main/components/Dialogs/ConfirmDialog.vue";

const store = useStore();
const router = useRouter();

const { t } = useI18n();

const showUploadDialog = ref(false);

const remoteFolder = useField<string>({
  defaultValue: "",
  defaultValid: false,
  validate: (value) => {
    if (!value || value.length === 0) {
      return t("Datasets.RemoteFolder.Error.Empty");
    }
    return "";
  },
});
const datasetFiles = useField<File[]>({
  defaultValue: [],
  defaultValid: false,
  validate: (files) => {
    if (!files || files.length === 0) {
      return t("Datasets.DatasetFiles.Error.Empty");
    }
    return "";
  },
});

const valid = computed(() => {
  return remoteFolder.valid && datasetFiles.valid;
});

const showDeleteDialog = ref(false);
const deleteItem = ref("");

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

function handleClickDelete(item: string): void {
  showDeleteDialog.value = true;
  deleteItem.value = item;
}

onActivated(() => {
  fetchItems();
});
</script>

<template>
  <div class="main-container mt-1">
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

    <submiting-dialog
      v-if="submiting"
      :progress="uploadProgress"
    >
      <template #title>
        <span>{{ t("Datasets.Uploading") }}</span>
      </template>
    </submiting-dialog>

    <confirm-dialog
      v-model="showDeleteDialog"
      @confirm="() => deleteDataset(deleteItem)"
    >
      <template #title>
        Confirm to delete&nbsp;
        <b> {{ deleteItem }} </b>?
      </template>
      <template #text>
        Dataset <b>{{ deleteItem }}</b> will be deleted in the server <i>permanently</i>. Do you
        really want to delete?
      </template>
    </confirm-dialog>

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
                {{ t("Datasets.DatasetFiles.Label") }}
              </div>
            </div>
            <div class="flex items-center justify-end">
              <v-btn
                class="opacity-0"
                icon="mdi-lock-reset"
              />
              <v-dialog
                v-model="showUploadDialog"
                max-width="600"
              >
                <template #activator="{ props: dialogProps }">
                  <v-btn
                    variant="flat"
                    v-bind="dialogProps"
                    icon="mdi-upload"
                  >
                  </v-btn>
                </template>
                <v-card>
                  <div class="p-2">
                    <v-card-title>
                      {{ t("Datasets.UploadDataset") }}
                    </v-card-title>
                    <v-card-text>
                      <div class="flat">
                        <v-text-field
                          v-model="remoteFolder.value"
                          :label="t('Datasets.RemoteFolder.Label')"
                          :hint="t('Datasets.RemoteFolder.Hint')"
                        />
                      </div>
                    </v-card-text>

                    <v-card-text>
                      <file-upload
                        v-model="datasetFiles.value"
                        class="text-3xl"
                        :tips="t('Datasets.DatasetFiles.Tips')"
                        :error-messages="datasetFiles.errorMessages"
                      />
                    </v-card-text>
                    <div class="flex justify-end space-x-2 px-4 py-2">
                      <v-spacer />
                      <v-btn
                        :disabled="!valid"
                        color="primary"
                        @click="uploadDataset"
                      >
                        {{ t("Datasets.Upload") }}
                      </v-btn>
                      <v-btn
                        variant="outlined"
                        @click="showUploadDialog = false"
                      >
                        {{ t("Datasets.Cancel") }}
                      </v-btn>
                    </div>
                  </div>
                </v-card>
              </v-dialog>
            </div>
          </div>
        </div>
        <div
          v-for="(item, i) in datasetItems"
          :key="i"
          class="item"
        >
          <div class="row">
            <div class="columns">
              <div>
                {{ item }}
              </div>
            </div>
            <div class="flex items-center justify-end">
              <v-btn
                variant="flat"
                icon="mdi-download"
                @click.stop="() => downloadDataset(item)"
              />
              <v-btn
                variant="flat"
                icon="mdi-delete"
                @click.stop="() => handleClickDelete(item)"
              />
            </div>
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
      {{ t("Dataset.OopsNoDatasetsFound") }}
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
    @apply border-t;
    .columns {
      @apply font-bold;
    }
  }

  .item {
    @apply border border-t-0 px-3;

    .row {
      @apply flex items-center;

      .columns {
        @apply grid w-full sm:grid-cols-[3fr,3fr,1fr,1fr,1fr];

        .my-title {
          @apply text-sm sm:flex sm:flex-col sm:items-start sm:justify-center lg:text-lg;
          .small-title {
            @apply font-bold sm:hidden;
          }
        }
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
