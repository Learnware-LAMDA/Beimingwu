<script setup>
import { ref, onMounted } from "vue";
import { useDisplay } from "vuetify";
import { useRoute, useRouter } from "vue-router";
import { getLearnwareDetailById } from "../request/engine";
import { downloadLearnwareSync } from "../utils";
import { verifyLog } from "../request/user";
import dayjs from "dayjs";

const route = useRoute();
const router = useRouter();

const display = useDisplay();

const learnware = ref(null);
const learnwareId = ref("");
const downloading = ref(false);
const loading = ref(false);

const showError = ref(false);
const errorMsg = ref("");

function getLearnwareDetail(id) {
  getLearnwareDetailById({ id })
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

function onLearnwareVerifyLog(learnware_id) {
  verifyLog({ learnware_id }).then((res) => {
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

      <v-card-text>
        <div>Data type: {{ learnware.dataType }}</div>
        <div>
          Input:
          <pre class="overflow-x-scroll">{{ JSON.stringify(learnware.input, null, 2) }}</pre>
        </div>
        <div>Task type: {{ learnware.taskType }}</div>
        <div>
          Output:
          <pre class="overflow-x-scroll">{{ JSON.stringify(learnware.output, null, 2) }}</pre>
        </div>
        <div>Library type: {{ learnware.libraryType }}</div>
        <div>Tags: {{ learnware.tagList.join(", ") }}</div>
        <div>
          Verify status: {{ learnware.verifyStatus }},
          <button class="text-blue-500 underline" @click="onLearnwareVerifyLog(learnware.id)">
            Logs
          </button>
        </div>
        <div>Last modify: {{ dayjs(learnware.lastModify).format("YYYY-MM-DD HH:mm:ss") }}</div>
      </v-card-text>

      <v-card-text class="md:(text-xl !leading-7) text-sm">
        Description: {{ learnware.description }}
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
</style>
