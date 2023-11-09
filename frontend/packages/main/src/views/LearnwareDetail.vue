<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { getLearnwareDetailById } from "../request/engine";
import { getProfile } from "../request/user";
import { deleteLearnware } from "../request/user";
import { downloadLearnwareSync } from "../utils";
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader";
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
});
const learnwareId = ref("");
const downloading = ref(false);
const loading = ref(false);

const editable = ref(false);

const deleteDialog = ref<InstanceType<typeof ConfirmDialog>>();
const deleteId = ref("");
const deleteName = ref("");

const showError = ref(false);
const errorMsg = ref("");

function getLearnwareDetail(id: string): Promise<void> {
  loading.value = true;
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
            };
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
      const { data } = await getProfile();
      if ([1, 2].includes(data.role) || learnwareUserId === data.user_id) {
        editable.value = true;
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
  deleteDialog.value?.confirm();
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
</script>

<template>
  <div class="relative max-w-[1200px] mx-auto p-4 sm:p-6 min-h-full sm:min-h-0 bg-white">
    <v-skeleton-loader
      v-if="loading"
      class=""
      :loading="loading"
      :show="true"
      :items="1"
      type="actions, article, article"
    />

    <div v-else>
      <confirm-dialog ref="deleteDialog" @confirm="handleDelete">
        <template #title>
          {{ t("MyLearnware.ConfirmToDelete") }} &nbsp; <b>{{ deleteName }}</b
          >{{ t("MyLearnware.?") }}
        </template>
        <template #text>
          {{ t("MyLearnware.YourLearnware") }} <b>{{ deleteName }}</b>
          {{ t("MyLearnware.DeleteContinue") }}
        </template>
      </confirm-dialog>

      <v-scroll-y-transition class="fixed left-0 right-0 z-10" style="top: var(--v-layout-top)">
        <v-card-actions v-if="showError">
          <v-alert
            class="w-full max-w-[900px] mx-auto"
            closable
            :text="errorMsg"
            type="error"
            @click:close="showError = false"
          />
        </v-card-actions>
      </v-scroll-y-transition>

      <div class="sm:flex justify-between">
        <div>
          <div class="text-h3 text-3xl lg:text-5xl">
            {{ learnware.name }}
          </div>
          <div class="my-4">
            {{ learnware.id }}
          </div>
        </div>
        <div class="flex justify-end">
          <v-btn
            variant="flat"
            icon="mdi-download"
            @click="() => downloadLearnwareSync(learnware.id)"
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

      <div v-if="learnware" class="min-h-full w-full" flat>
        <div class="learnware-container text-lg">
          <v-expansion-panels v-if="learnware.dataType === 'Table'" class="mt-2 border rounded-lg">
            <v-expansion-panel elevation="0" class="rounded-lg">
              <v-expansion-panel-title class="text-lg">
                <div>
                  <b>{{ t("Submit.SemanticSpecification.DataType.DataType") }}:</b>
                  {{
                    learnware.dataType &&
                    t(`Submit.SemanticSpecification.DataType.Type.${learnware.dataType}`)
                  }}
                </div>
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <div class="flex font-bold py-3 border-y">
                  <div class="w-20">
                    {{ t("Submit.SemanticSpecification.DataType.DescriptionInput.Name") }}
                  </div>
                  <div class="w-full">
                    {{ t("Submit.SemanticSpecification.DataType.DescriptionInput.Description") }}
                  </div>
                </div>
                <div v-if="learnware.input.Dimension < 8">
                  <div v-for="[key, val] in Object.entries(learnware.input.Description)" :key="key">
                    <div class="flex py-2 px-1 border-b">
                      <div class="w-20">{{ key }}</div>
                      <div class="w-full">{{ val }}</div>
                    </div>
                  </div>
                </div>
                <v-virtual-scroll
                  v-else
                  :items="Object.entries(learnware.input.Description)"
                  :height="300"
                >
                  <template #default="{ item }">
                    <div class="flex py-2 px-1 border-b">
                      <div class="w-20">{{ Number(item[0]) }}</div>
                      <div class="w-full">{{ item[1] }}</div>
                    </div>
                  </template>
                </v-virtual-scroll>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
          <div v-else>
            <b>{{ t("Submit.SemanticSpecification.DataType.DataType") }}:</b>
            {{
              learnware.dataType &&
              t(`Submit.SemanticSpecification.DataType.Type.${learnware.dataType}`)
            }}
          </div>

          <v-expansion-panels
            v-if="['Classification', 'Regression'].includes(learnware.taskType)"
            class="mr-2 border rounded-lg"
          >
            <v-expansion-panel elevation="0" class="rounded-lg">
              <v-expansion-panel-title class="text-lg">
                <div>
                  <b>{{ t("Submit.SemanticSpecification.TaskType.TaskType") }}:</b>
                  {{
                    learnware.taskType &&
                    t(`Submit.SemanticSpecification.TaskType.Type.${learnware.taskType}`)
                  }}
                </div>
              </v-expansion-panel-title>
              <v-expansion-panel-text>
                <div
                  v-if="
                    ['Classification', 'Regression', 'Feature Extraction'].includes(
                      learnware.taskType,
                    )
                  "
                  class="mt-2"
                >
                  <div class="flex font-bold py-3 border-y">
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
                      <div class="flex py-2 px-1 border-b">
                        <div class="w-20">{{ key }}</div>
                        <div class="w-full">{{ val }}</div>
                      </div>
                    </div>
                  </div>
                  <v-virtual-scroll
                    v-else
                    :items="Object.entries(learnware.output.Description)"
                    :height="300"
                  >
                    <template #default="{ item }">
                      <div class="flex py-2 px-1 border-b">
                        <div class="w-20">{{ Number(item[0]) }}</div>
                        <div class="w-full">{{ item[1] }}</div>
                      </div>
                    </template>
                  </v-virtual-scroll>
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>

          <div v-else>
            <b>{{ t("Submit.SemanticSpecification.TaskType.TaskType") }}:</b>
            {{
              learnware.taskType &&
              t(`Submit.SemanticSpecification.TaskType.Type.${learnware.taskType}`)
            }}
          </div>

          <div>
            <b>{{ t("Submit.SemanticSpecification.LibraryType.LibraryType") }}:</b>
            {{
              learnware.libraryType &&
              t(`Submit.SemanticSpecification.LibraryType.Type.${learnware.libraryType}`)
            }}
          </div>
          <div>
            <b>{{ t("Submit.SemanticSpecification.Scenario.Scenario") }}:</b>
            <span v-for="(scenario, i) in learnware.scenarioList" :key="i" class="ml-1 active">
              {{ t(`Submit.SemanticSpecification.Scenario.Type.${scenario}`) }}
            </span>
          </div>
          <div>
            <b>{{ t("LearnwareDetail.VerifyStatus.VerifyStatus") }}: </b>
            {{
              learnware.verifyStatus && t(`LearnwareDetail.VerifyStatus.${learnware.verifyStatus}`)
            }},
            <button class="text-blue-500 underline" @click="onLearnwareVerifyLog(learnware.id)">
              {{ t("LearnwareDetail.Logs") }}
            </button>
          </div>
          <div>
            <b> {{ t("LearnwareDetail.LastModified") }}: </b>
            {{ dayjs(learnware.lastModify).format("YYYY-MM-DD HH:mm:ss") }}
          </div>
          <div>
            <b>{{ t("Submit.Description.Description") }}:</b>
            {{ learnware.description }}
          </div>
        </div>
      </div>
      <v-overlay v-model="downloading" class="flex justify-center items-center">
        <v-progress-circular size="80" width="8" indeterminate />
      </v-overlay>
    </div>
  </div>
</template>

<style scoped lang="scss">
.learnware-container > div {
  @apply my-3;
}
</style>
