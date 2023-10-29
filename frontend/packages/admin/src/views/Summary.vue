<script setup lang="ts">
import { ref, computed, onMounted, type ComputedRef } from "vue";
import { useI18n } from "vue-i18n";
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { fetchex } from "../utils";
import Router from "../router";
import type { DataType, TaskType, LibraryType, Tag } from "@beiming-system/types/learnware";

export interface CountDetail {
  Data: Record<DataType, number>;
  Task: Record<TaskType, number>;
  Library: Record<LibraryType, number>;
  Scenario: Record<Tag, number>;
}

const { t } = useI18n();

ChartJS.register(ArcElement, Tooltip, Legend);

const countUser = ref(0);
const countVerifiedLearnware = ref(0);
const countUnverifiedLearnware = ref(0);
const countDownload = ref(0);
const countDetail = ref<CountDetail>();

const options = ref({
  responsive: true,
  maintainAspectRatio: true,
});

const showError = ref(false);
const errorMsg = ref("");
const errorTimer = ref<number>();

const numberItems = computed(() => {
  return [
    {
      title: t("Summary.UserCount"),
      icon: "mdi-account",
      value: countUser.value,
      to: "/alluser",
    },
    {
      title: t("Summary.VerifiedLearnwareCount"),
      icon: "mdi-check",
      value: countVerifiedLearnware.value,
      to: "/alllearnware?is_verify=true",
    },
    {
      title: t("Summary.UnverifiedLearnwareCount"),
      icon: "mdi-close",
      value: countUnverifiedLearnware.value,
      to: "/alllearnware?is_verify=false",
    },
    {
      title: t("Summary.DownloadCount"),
      icon: "mdi-download",
      value: countDownload.value,
    },
  ];
});

function fetchSummary(): void {
  fetchex("/api/admin/summary", { method: "POST" })
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
          count_user: number;
          count_download: number;
          count_verified_learnware: number;
          count_unverified_learnware: number;
          count_detail: CountDetail;
        };
      }) => {
        if (res.code === 0) {
          countUser.value = res.data.count_user;
          countVerifiedLearnware.value = res.data.count_verified_learnware;
          countUnverifiedLearnware.value = res.data.count_unverified_learnware;
          countDownload.value = res.data.count_download;
          countDetail.value = res.data.count_detail;
        } else if (res.code === 11) {
          Router.push("/login");
        } else {
          errorMsg.value = res.msg;
          showError.value = true;
        }
      },
    )
    .catch((err) => {
      console.error(err);
      showError.value = true;
      clearTimeout(errorTimer.value);
      setTimeout(() => (showError.value = false), 2000);
      errorMsg.value = err.message;
    });
}

function getPieData(
  counts: {
    [key: string]: number;
  },
  key: string,
): {
  labels: string[];
  datasets: {
    label: string;
    backgroundColor: string[];
    data: number[];
  }[];
} {
  return {
    labels: Object.keys(counts),
    datasets: [
      {
        label: key,
        backgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#4BC0C0",
          "#FF8A80",
          "#FFD180",
          "#A1887F",
          "#90CAF9",
          "#80CBC4",
          "#B39DDB",
          "#F48FB1",
          "#CE93D8",
          "#FFAB91",
          "#BCAAA4",
          "#EEEEEE",
          "#B0BEC5",
          "#9E9E9E",
          "#E0E0E0",
          "#FFEB3B",
          "#FFC107",
          "#FF9800",
          "#FF5722",
          "#795548",
          "#607D8B",
        ],
        data: Object.values(counts),
      },
    ],
  };
}

function translateKey<T>(obj: Record<string, T>, prefix: string): ComputedRef<Record<string, T>> {
  return computed(() =>
    Object.fromEntries(Object.entries(obj).map(([key, val]) => [t(prefix + key), val])),
  );
}

onMounted(() => {
  fetchSummary();
});
</script>

<template>
  <div class="m-auto md:max-w-6xl">
    <v-snackbar v-model="showError" :timeout="2000" color="error">
      {{ errorMsg }}
    </v-snackbar>

    <div class="grid md:(grid-cols-2) md:gap-2 md:m-2">
      <v-card
        v-for="item in numberItems"
        flat
        class="md:border-1 border-b-1"
        :to="item.to"
        :key="item.title"
      >
        <v-card-title>
          <v-icon>{{ item.icon }}</v-icon>
          {{ item.title }}
        </v-card-title>
        <v-card-text class="my-8 text-h3 text-center font-bold">
          {{ item.value }}
        </v-card-text>
      </v-card>
    </div>

    <div class="md:m-2">
      <v-card flat class="md:border-1">
        <v-card-title>
          <v-icon>mdi-chart-pie</v-icon>
          {{ t("Summary.Chart") }}
        </v-card-title>
        <v-card-item>
          <div class="grid lg:grid-cols-4 sm:grid-cols-2 gap-4">
            <div>
              <Pie
                v-if="countDetail"
                :data="
                  getPieData(
                    translateKey(countDetail.Data, 'Submit.Tag.DataType.Type.').value,
                    'Data',
                  )
                "
                :options="options"
              />
            </div>
            <div>
              <Pie
                v-if="countDetail"
                :data="
                  getPieData(
                    translateKey(countDetail.Task, 'Submit.Tag.TaskType.Type.').value,
                    'Task',
                  )
                "
                :options="options"
              />
            </div>
            <div>
              <Pie
                v-if="countDetail"
                :data="
                  getPieData(
                    translateKey(countDetail.Library, 'Submit.Tag.LibraryType.Type.').value,
                    'Library',
                  )
                "
                :options="options"
              />
            </div>
            <div>
              <Pie
                v-if="countDetail"
                :data="
                  getPieData(
                    translateKey(countDetail.Scenario, 'Submit.Tag.Scenario.Type.').value,
                    'Scenario',
                  )
                "
                :options="options"
              />
            </div>
          </div>
        </v-card-item>
      </v-card>
    </div>
  </div>
</template>
