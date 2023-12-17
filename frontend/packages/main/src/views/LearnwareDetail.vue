<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { html2Markdown } from "../utils";
import { getLearnwareDetailById } from "../request/engine";
import { getProfile } from "../request/user";
import { deleteLearnware } from "../request/user";
import { downloadLearnwareSync } from "../utils";
import ConfirmDialog from "../components/Dialogs/ConfirmDialog.vue";
import { verifyLog } from "../request/user";
import dayjs from "dayjs";
import type { LearnwareDetailInfoWithDescription } from "@beiming-system/types/learnware";

const route = useRoute();

const router = useRouter();

const { t } = useI18n();

const learnware = ref<LearnwareDetailInfoWithDescription>({
  id: "",
  verifyStatus: "",
  lastModify: "",
  name: "",
  input: {
    Description: {},
    Dimension: 0,
  },
  output: {
    Description: {},
    Dimension: 0,
  },
  description: "",
  dataType: "",
  taskType: "",
  libraryType: "",
  scenarioList: [],
  licenseList: [],
});
const learnwareId = ref("");
const loading = ref(false);
const success = ref(false);

const editable = ref(false);

const showDescription = ref(false);
const descriptionTab = ref<string>("");

const showDeleteDialog = ref(false);
const deleteId = ref("");
const deleteName = ref("");

const showError = ref(false);
const errorMsg = ref("");

function getLearnwareDetail(id: string): Promise<void> {
  loading.value = true;
  success.value = false;
  return getLearnwareDetailById({ id })
    .then((res) => {
      switch (res.code) {
        case 0: {
          if (res.data && res.data.learnware_info) {
            const learnwareInfo = res.data.learnware_info;
            learnware.value = {
              id: learnwareInfo.learnware_id,
              verifyStatus: learnwareInfo.verify_status,
              lastModify: learnwareInfo.last_modify,
              name: learnwareInfo.semantic_specification.Name.Values,
              input: learnwareInfo.semantic_specification.Input,
              output: learnwareInfo.semantic_specification.Output,
              description: learnwareInfo.semantic_specification.Description.Values,
              dataType: learnwareInfo.semantic_specification.Data.Values[0],
              taskType: learnwareInfo.semantic_specification.Task.Values[0],
              libraryType: learnwareInfo.semantic_specification.Library.Values[0],
              scenarioList: learnwareInfo.semantic_specification.Scenario.Values,
              licenseList: learnwareInfo.semantic_specification.License.Values,
            };
            descriptionTab.value =
              learnwareInfo.semantic_specification.Data.Values[0] === "Table" ? "data" : "task";
            success.value = true;
            return learnwareInfo.user_id;
          }
          return;
        }
        default: {
          throw new Error(res.msg);
        }
      }
    })
    .then(async (learnwareUserId: string | undefined): Promise<void> => {
      if (!learnwareUserId) {
        editable.value = false;
        return;
      }
      try {
        const { data } = await getProfile();

        if ([1, 2].includes(data.role) || learnwareUserId === data.user_id) {
          editable.value = true;
          return;
        }
      } catch (err) {
        return;
      }
    })
    .catch((err) => {
      loading.value = false;
      showError.value = true;
      errorMsg.value = err.message;
    })
    .finally(() => {
      loading.value = false;
    });
}

onMounted(() => {
  const _id = route.query.id;
  learnwareId.value = String(_id);
  getLearnwareDetail(learnwareId.value);
});

function handleClickDelete(id: string): void {
  showDeleteDialog.value = true;
  deleteId.value = id;
  deleteName.value = learnware.value.name;
}

function handleDelete(): Promise<void> {
  loading.value = true;
  return deleteLearnware({ id: deleteId.value })
    .then((res) => {
      switch (res.code) {
        case 0: {
          router.go(-1);
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
    })
    .finally(() => {
      loading.value = false;
    });
}

function onLearnwareVerifyLog(learnware_id: string): Promise<void> {
  return verifyLog({ learnware_id }).then((res) => {
    var blob = new Blob([res.data], { type: "text/plain" });
    var _url = window.URL.createObjectURL(blob);
    window.open(_url, "_blank")?.focus(); // window.open + focus
  });
}

function handleDownload(id: string): void {
  downloadLearnwareSync(id).catch((err) => {
    console.error(err);
    showError.value = true;
    errorMsg.value = err.message;
  });
}
</script>

<template>
  <v-sheet class="relative mx-auto min-h-full max-w-[1200px] border p-4 sm:min-h-0 sm:p-6">
    <v-scroll-y-transition
      class="fixed left-0 right-0 z-10"
      style="top: var(--v-layout-top)"
    >
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

    <v-skeleton-loader
      v-if="loading"
      class=""
      :loading="loading"
      :show="true"
      :items="1"
      type="actions, article, article"
    />

    <template v-else-if="success">
      <confirm-dialog
        v-model="showDeleteDialog"
        @confirm="handleDelete"
      >
        <template #title>
          <div class="ml-1 flex-1 overflow-hidden text-ellipsis">
            {{ t("MyLearnware.ConfirmToDelete") }}
          </div>
        </template>
        <template #text>
          {{ t("MyLearnware.YourLearnware") }} <b>{{ deleteName }}</b>
          {{ t("MyLearnware.DeleteContinue") }}
        </template>
      </confirm-dialog>

      <!-- name and download button -->
      <div class="justify-between sm:flex">
        <div class="flex-1 break-all text-3xl lg:text-5xl">
          {{ learnware.name }}
        </div>
        <div class="flex justify-end">
          <v-btn
            variant="flat"
            icon="mdi-download"
            @click="() => handleDownload(learnware.id)"
          />
          <template v-if="editable">
            <v-btn
              variant="flat"
              icon="mdi-pencil"
              :to="{
                path: '/submit',
                query: {
                  edit: 'true',
                  id: learnware.id,
                },
              }"
            />
            <v-btn
              variant="flat"
              icon="mdi-delete"
              @click="() => handleClickDelete(learnware.id)"
            />
          </template>
        </div>
      </div>

      <!-- id and last modify -->
      <div class="justify-between sm:mt-4 sm:flex">
        <div class="text-lg">
          {{ learnware.id }}
        </div>
        <div class="text-base">
          {{ t("LearnwareDetail.LastModified") }}:
          {{
            dayjs.utc(learnware.lastModify.replace(" UTC", "")).tz().format("YYYY-MM-DD HH:mm:ss")
          }}
          <template v-if="editable">
            <span
              class="cursor-pointer underline"
              @click="onLearnwareVerifyLog(learnware.id)"
            >
              {{ t("LearnwareDetail.ViewLogs") }}
            </span>
          </template>
        </div>
      </div>

      <!-- verify status -->
      <v-chip
        v-if="learnware.verifyStatus"
        :prepend-icon="
          learnware.verifyStatus === 'FAIL'
            ? 'mdi-close'
            : learnware.verifyStatus === 'SUCCESS'
              ? 'mdi-check'
              : 'mdi-alert'
        "
        size="large"
        :color="
          learnware.verifyStatus === 'FAIL'
            ? 'error'
            : learnware.verifyStatus === 'SUCCESS'
              ? 'success'
              : 'warning'
        "
        class="mt-4"
      >
        {{ t(`Learnware.VerifyStatus.${learnware.verifyStatus}`) }}
      </v-chip>

      <!-- semantic specification -->
      <div class="mt-2 flex flex-wrap items-center space-x-2 pb-2 pt-0 text-sm">
        <v-chip
          label
          class="my-1"
        >
          {{ t(`Submit.SemanticSpecification.DataType.Type.${learnware.dataType}`) }}
        </v-chip>
        <v-chip
          label
          class="my-1"
        >
          {{
            t(
              `Submit.SemanticSpecification.TaskType.Type.${learnware.taskType.replace(
                "Others",
                "OtherTask",
              )}`,
            )
          }}
        </v-chip>
        <v-chip class="my-1">
          {{
            t(
              `Submit.SemanticSpecification.LibraryType.Type.${learnware.libraryType.replace(
                "Others",
                "OtherLibrary",
              )}`,
            )
          }}
        </v-chip>
        <v-chip
          v-for="(scenario, i) in learnware.scenarioList"
          :key="i"
          class="my-1"
        >
          {{
            t(
              `Submit.SemanticSpecification.Scenario.Type.${scenario.replace(
                "Others",
                "OtherScenario",
              )}`,
            )
          }}
        </v-chip>
        <v-chip
          v-for="(license, i) in learnware.licenseList"
          :key="i"
          class="my-1"
        >
          {{
            license === "Others"
              ? t("Submit.SemanticSpecification.License.Type.OtherLicense")
              : license
          }}
        </v-chip>
      </div>

      <!-- feature/label description -->
      <div
        v-if="
          learnware.dataType === 'Table' ||
          ['Classification', 'Regression'].includes(learnware.taskType)
        "
        class="rounded border p-2"
      >
        <div
          class="cursor-pointer text-base"
          @click="showDescription = !showDescription"
        >
          <v-icon
            class="transition"
            :class="{ 'rotate-90': showDescription }"
          >
            mdi-chevron-right
          </v-icon>
          {{ t("LearnwareDetail.FeatureLabelDescription") }}
        </div>
        <v-expand-transition>
          <div
            v-if="showDescription"
            class="text-base"
          >
            <v-tabs v-model="descriptionTab">
              <v-tab
                v-if="learnware.dataType === 'Table'"
                value="data"
              >
                {{ t("Submit.SemanticSpecification.DataType.DescriptionInput.Name") }}
              </v-tab>
              <v-tab
                v-if="
                  ['Classification', 'Regression', 'Feature Extraction'].includes(
                    learnware.taskType,
                  )
                "
                value="task"
              >
                {{ t("Submit.SemanticSpecification.TaskType.DescriptionOutput.Name") }}
              </v-tab>
            </v-tabs>

            <v-window v-model="descriptionTab">
              <v-window-item value="data">
                <div
                  v-if="learnware.dataType === 'Table'"
                  class="mt-2"
                >
                  <div class="flex border-y py-3 font-bold">
                    <div class="w-20">
                      {{ t("Submit.SemanticSpecification.DataType.DescriptionInput.Name") }}
                    </div>
                    <div class="w-full">
                      {{ t("Submit.SemanticSpecification.DataType.DescriptionInput.Description") }}
                    </div>
                  </div>
                  <div v-if="learnware.input.Dimension < 8">
                    <div
                      v-for="[key, val] in Object.entries(learnware.input.Description)"
                      :key="key"
                    >
                      <div class="flex border-b px-1 py-2">
                        <div class="w-20">
                          {{ key }}
                        </div>
                        <div class="w-full">
                          {{ val }}
                        </div>
                      </div>
                    </div>
                  </div>
                  <v-virtual-scroll
                    v-else
                    :items="Object.entries(learnware.input.Description)"
                    :height="300"
                  >
                    <template #default="{ item }">
                      <div class="flex border-b px-1 py-2">
                        <div class="w-20">
                          {{ Number(item[0]) }}
                        </div>
                        <div class="w-full">
                          {{ item[1] }}
                        </div>
                      </div>
                    </template>
                  </v-virtual-scroll>
                </div>
              </v-window-item>
              <v-window-item value="task">
                <div
                  v-if="
                    ['Classification', 'Regression', 'Feature Extraction'].includes(
                      learnware.taskType,
                    )
                  "
                  class="mt-2"
                >
                  <div class="flex border-y py-3 font-bold">
                    <div class="w-20">
                      {{ t("Submit.SemanticSpecification.TaskType.DescriptionOutput.Name") }}
                    </div>
                    <div class="w-full">
                      {{ t("Submit.SemanticSpecification.TaskType.DescriptionOutput.Description") }}
                    </div>
                  </div>
                  <div v-if="learnware.output.Dimension < 8">
                    <div
                      v-for="[key, val] in Object.entries(learnware.output.Description)"
                      :key="key"
                    >
                      <div class="flex border-b px-1 py-2">
                        <div class="w-20">
                          {{ key }}
                        </div>
                        <div class="w-full">
                          {{ val }}
                        </div>
                      </div>
                    </div>
                  </div>
                  <v-virtual-scroll
                    v-else
                    :items="Object.entries(learnware.output.Description)"
                    :height="300"
                  >
                    <template #default="{ item }">
                      <div class="flex border-b px-1 py-2">
                        <div class="w-20">
                          {{ Number(item[0]) }}
                        </div>
                        <div class="w-full">
                          {{ item[1] }}
                        </div>
                      </div>
                    </template>
                  </v-virtual-scroll>
                </div>
              </v-window-item>
            </v-window>
          </div>
        </v-expand-transition>
      </div>

      <!-- description -->
      <div
        class="markdown-content mt-2 overflow-x-auto break-words text-lg"
        v-html="html2Markdown(learnware.description)"
      />
    </template>
  </v-sheet>
</template>

<style scoped lang="scss">
.markdown-content {
  :deep(ol),
  :deep(ul) {
    @apply list-inside;
  }

  :deep(h1),
  :deep(h2),
  :deep(h3),
  :deep(h4),
  :deep(h5),
  :deep(h6) {
    @apply mb-2 mt-4;
  }
}
</style>
