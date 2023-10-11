<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useDisplay } from "vuetify";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { getLearnwareDetailById } from "../request/engine";
import { downloadLearnwareSync } from "../utils";
import { verifyLog } from "../request/user";
import dayjs from "dayjs";

const route = useRoute();
const router = useRouter();

const display = useDisplay();

const { t } = useI18n();

const learnware = ref(null);
const learnwareId = ref("");
const downloading = ref(false);
const loading = ref(false);

const showInputDescription = ref(false);
const showOutputDescription = ref(false);

const showError = ref(false);
const errorMsg = ref("");

function getLearnwareDetail(id): Promise<void> {
  return getLearnwareDetailById({ id })
    .then((res) => {
      switch (res.code) {
        case 0: {
          const learnwareInfo = res.data ? res.data.learnware_info : {};
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
            tagList: learnwareInfo.semantic_specification.Scenario.Values,
          };
          return;
        }
        default: {
          throw new Error(res.msg);
        }
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
  learnwareId.value = _id;
  getLearnwareDetail(learnwareId.value);
});

function onLearnwareVerifyLog(learnware_id): Promise<void> {
  return verifyLog({ learnware_id }).then((res) => {
    var blob = new Blob([res.data], { type: "text/plain" });
    //var blob = res.blob();
    // blob.type = "text/plain";
    var _url = window.URL.createObjectURL(blob);
    window.open(_url, "_blank").focus(); // window.open + focus
  });
}
</script>

<template>
  <v-container class="md:flex max-w-1500px <sm:p-1">
    <v-scroll-y-transition class="fixed left-0 right-0 z-index-10" style="top: var(--v-layout-top)">
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

    <v-btn
      v-if="display.name.value !== 'xs'"
      class="md:mx-3 <md:my-3"
      icon="mdi-arrow-left"
      size="50"
      @click="() => router.go(-1)"
    />
    <v-card v-if="learnware" class="p-2 w-1/1" :flat="display.name.value === 'xs'">
      <v-card-title class="text-h4 !md:text-3xl !text-xl">
        {{ learnware.name }}
      </v-card-title>

      <v-card-actions class="download-button">
        <v-btn icon="mdi-download" @click="() => downloadLearnwareSync(learnware.id)" />
      </v-card-actions>

      <v-card-subtitle>
        {{ learnware.id }}
      </v-card-subtitle>

      <v-card-text class="learnware-container">
        <div class="flex items-center">
          <div class="mr-2">
            <v-switch
              v-if="learnware.dataType === 'Table'"
              v-model="showInputDescription"
              color="primary"
              density="compact"
              inset
              hide-details
            />
          </div>
          <div>
            <b>{{ t("Submit.Tag.DataType.DataType") }}:</b>
            {{ t(`Submit.Tag.DataType.Type.${learnware.dataType}`) }}
          </div>
        </div>
        <v-expand-transition>
          <div v-if="learnware.dataType === 'Table' && showInputDescription" class="mt-2">
            <div class="flex font-bold py-3 border-y-1">
              <div class="w-20">
                {{ t("Submit.Tag.DataType.DescriptionInput.Name") }}
              </div>
              <div class="w-1/1">
                {{ t("Submit.Tag.DataType.DescriptionInput.Description") }}
              </div>
            </div>
            <v-virtual-scroll :items="Object.entries(learnware.input.Description)" :height="300">
              <template #default="{ item }">
                <div class="flex py-2 px-1 border-b-1">
                  <div class="w-20">{{ Number(item[0]) }}</div>
                  <div class="w-1/1">{{ item[1] }}</div>
                </div>
              </template>
            </v-virtual-scroll>
          </div>
        </v-expand-transition>

        <div class="flex items-center">
          <div class="mr-2">
            <v-switch
              v-if="
                ['Classification', 'Regression', 'Feature Extraction'].includes(learnware.taskType)
              "
              v-model="showOutputDescription"
              color="primary"
              density="compact"
              inset
              hide-details
            />
          </div>
          <div>
            <b>{{ t("Submit.Tag.TaskType.TaskType") }}:</b>
            {{ t(`Submit.Tag.TaskType.Type.${learnware.taskType}`) }}
          </div>
        </div>
        <v-expand-transition>
          <div
            v-if="
              ['Classification', 'Regression', 'Feature Extraction'].includes(learnware.taskType) &&
              showOutputDescription
            "
            class="mt-2"
          >
            <div class="flex font-bold py-3 border-y-1">
              <div class="w-20">
                {{ t("Submit.Tag.TaskType.DescriptionOutput.Name") }}
              </div>
              <div class="w-1/1">
                {{ t("Submit.Tag.TaskType.DescriptionOutput.Description") }}
              </div>
            </div>
            <v-virtual-scroll :items="Object.entries(learnware.output.Description)" :height="300">
              <template #default="{ item }">
                <div class="flex py-2 px-1 border-b-1">
                  <div class="w-20">{{ Number(item[0]) }}</div>
                  <div class="w-1/1">{{ item[1] }}</div>
                </div>
              </template>
            </v-virtual-scroll>
          </div>
        </v-expand-transition>
        <div>
          <b>{{ t("Submit.Tag.LibraryType.LibraryType") }}:</b>
          {{ t(`Submit.Tag.LibraryType.Type.${learnware.libraryType}`) }}
        </div>
        <div>
          <b>{{ t("Submit.Tag.Scenario.Scenario") }}:</b>
          <span
            v-for="(tag, i) in learnware.tagList"
            :key="i"
            class="ml-1"
            :class="
              filters && filters.tagList && filters.tagList.includes(tag) ? 'active' : undefined
            "
          >
            {{ t(`Submit.Tag.Scenario.Type.${tag}`) }}
          </span>
        </div>
        <div>
          <b>{{ t("LearnwareDetail.VerifyStatus.VerifyStatus") }}: </b>
          {{ t(`LearnwareDetail.VerifyStatus.${learnware.verifyStatus}`) }},
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
      </v-card-text>
    </v-card>
    <v-overlay v-model="downloading" class="flex justify-center items-center">
      <v-progress-circular size="80" width="8" indeterminate />
    </v-overlay>
  </v-container>
</template>

<style scoped lang="scss">
.download-button {
  @apply absolute right-2 top-2;
}

.learnware-container {
  @apply text-lg;
  > div {
    @apply my-3;
  }
}
</style>
