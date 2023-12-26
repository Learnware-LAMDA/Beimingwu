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
import TreeView from "@main/components/Public/TreeView.vue";
import OopsImg from "@main/assets/images/public/oops.svg?component";

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

const datasetItems = ref<Record<string, string[]>>({});

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
          datasets: Record<string, string[]>;
        };
      }) => {
        if (res.code === 0) {
          if (res.data && res.data.datasets) {
            remoteFolder.value = "";
            datasetFiles.value = [];
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
    })
    .catch((err) => {
      showError.value = true;
      errorMsg.value = err.message;
    })
    .finally(() => {
      loading.value = false;
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

function downloadDataset(path: string, name: string): void {
  window.open(`${BACKEND_URL}/datasets/download_datasets?dataset=${path}/${name}`);
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
      console.error(err);
      showError.value = true;
      errorMsg.value = err.message;
      clearTimeout(errorTimer.value);
      errorTimer.value = Number(
        setTimeout(() => {
          showError.value = false;
        }, 3000),
      );
    })
    .finally(() => {
      submiting.value = false;
    });
}

function handleClickDelete(path: string, name: string): void {
  showDeleteDialog.value = true;
  deleteItem.value = `${path}/${name}`;
}

onActivated(() => {
  fetchItems();
});
</script>

<template>
  <div
    class="bg-surface-light dark:bg-surface-dark mx-auto mt-1 w-full max-w-[1500px] overflow-hidden"
  >
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
        <span class="truncate">
          Confirm to delete
          <b> {{ deleteItem }} </b>
        </span>
        ?
      </template>
      <template #text>
        Dataset <b class="break-all">{{ deleteItem }}</b> will be deleted in the server
        <i>permanently</i>. Do you really want to delete?
      </template>
    </confirm-dialog>

    <div
      class="relative p-1"
      :class="Object.values(datasetItems).length === 0 ? ['grid-cols-1', 'h-full'] : null"
      :style="{ gridTemplateColumns: `repeat(2, minmax(0, 1fr))` }"
    >
      <div>
        <div class="flex items-center justify-between">
          <div class="p-3 text-xl font-medium sm:flex sm:flex-col lg:text-2xl">
            {{ t("Datasets.DatasetFiles.Label") }}
          </div>

          <div class="flex items-center justify-end">
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

      <template v-if="Object.values(datasetItems).length > 0">
        <TreeView
          v-for="(items, folder) in datasetItems"
          :key="folder"
          :title="folder"
          :items="items"
          title-icon="mdi-folder"
        >
          <template #title="{ showDetails, toggleDetails }">
            <h3
              class="hover:bg-active-light dark:bg-active-dark flex cursor-pointer items-center p-1"
              @click="() => toggleDetails()"
            >
              <v-icon
                class="transition"
                :class="{ 'rotate-90': showDetails }"
                >mdi-chevron-right</v-icon
              >
              <v-icon>mdi-folder</v-icon>
              <span class="ms-2 overflow-hidden truncate">{{ folder }}</span>

              <div class="flex-1" />

              <v-btn
                variant="flat"
                icon="mdi-upload"
                color="transparent"
                @click.stop="
                  () => {
                    remoteFolder.value = folder;
                    showUploadDialog = true;
                  }
                "
              />
            </h3>
          </template>

          <template #items="{ item }">
            <div
              class="hover:bg-active-light dark:hover:bg-active-dark ms-4 flex items-center justify-between border-s"
            >
              <div class="flex h-4 w-4 flex-col justify-center">
                <div class="border-t" />
              </div>
              <div class="flex-1 overflow-hidden truncate py-3 pl-1">
                <v-icon>mdi-file</v-icon>
                {{ item }}
              </div>
              <div class="flex items-center justify-end">
                <v-btn
                  variant="flat"
                  icon="mdi-download"
                  color="transparent"
                  @click.stop="() => downloadDataset(folder, item)"
                />
                <v-btn
                  variant="flat"
                  icon="mdi-delete"
                  color="transparent"
                  @click.stop="() => handleClickDelete(folder, item)"
                />
              </div>
            </div>
          </template>
        </TreeView>
      </template>

      <div
        v-else
        flat
        class="bottom-0 flex w-full flex-col items-center justify-center text-2xl"
      >
        <oops-img
          class="mx-auto block fill-gray-800 dark:fill-gray-300"
          width="100"
          height="100"
        />
        {{ t("Datasets.OopsNoDatasetsFound") }}
      </div>
    </div>
  </div>
</template>
