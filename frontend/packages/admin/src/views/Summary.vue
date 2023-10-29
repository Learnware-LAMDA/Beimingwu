<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { fetchex } from "../utils";
import Router from "../router";

ChartJS.register(ArcElement, Tooltip, Legend);

const countUser = ref(0);
const countVerifiedLearnware = ref(0);
const countUnverifiedLearnware = ref(0);
const countDownload = ref(0);
const countDetail = ref<{
  Data: {
    [key: string]: number;
  };
  Task: {
    [key: string]: number;
  };
  Library: {
    [key: string]: number;
  };
  Scenario: {
    [key: string]: number;
  };
}>({
  Data: {},
  Task: {},
  Library: {},
  Scenario: {},
});

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
      title: "User Count",
      icon: "mdi-account",
      value: countUser.value,
      to: "/alluser",
    },
    {
      title: "Verified Learnware Count",
      icon: "mdi-check",
      value: countVerifiedLearnware.value,
      to: "/alllearnware?is_verify=true",
    },
    {
      title: "Unverified Learnware Count",
      icon: "mdi-close",
      value: countUnverifiedLearnware.value,
      to: "/alllearnware?is_verify=false",
    },
    {
      title: "Download Count",
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
          count_detail: {
            Data: {
              [key: string]: number;
            };
            Task: {
              [key: string]: number;
            };
            Library: {
              [key: string]: number;
            };
            Scenario: {
              [key: string]: number;
            };
          };
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
        backgroundColor: ["#41B883", "#E46651", "#00D8FF", "#DD1B16"],
        data: Object.values(counts),
      },
    ],
  };
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
      <v-card v-for="item in numberItems" flat class="md:border-1 border-b-1" :to="item.to" :key="item.title">
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
          Chart
        </v-card-title>
        <v-card-item>
          <div class="grid lg:grid-cols-4 sm:grid-cols-2 gap-4">
            <div v-for="(val, key) in countDetail" :key="key">
              <Pie :data="getPieData(val, key)" :options="options" />
            </div>
          </div>
        </v-card-item>
      </v-card>
    </div>
  </div>
</template>
