<script setup>
import { ref, onActivated } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { fetchex } from "@/utils";

ChartJS.register(ArcElement, Tooltip, Legend);

const route = useRoute();
const router = useRouter();

const countUser = ref(0);
const countVerifiedLearnware = ref(0);
const countUnverifiedLearnware = ref(0);
const countDownload = ref(0);
const countDetail = ref({});

const options = ref({
  responsive: true,
  maintainAspectRatio: false,
});

const showError = ref(false);
const errorMsg = ref("");

function fetchSummary() {
  countDetail.value = {};

  fetchex("/api/admin/summary", { method: "POST" })
    .then((res) => res.json())
    .then((res) => {
      if (res.code !== 0) {
        errorMsg.value = res.msg;
        showError.value = true;
      } else {
        countUser.value = res.data.count_user;
        countVerifiedLearnware.value = res.data.count_verified_learnware;
        countUnverifiedLearnware.value = res.data.count_unverified_learnware;
        countDownload.value = res.data.count_download;
        countDetail.value = res.data.count_detail;
      }
    })
    .catch((err) => {
      console.error(err);
      showError.value = true;
      clearTimeout(errorTimer.value);
      setTimeout(() => (showError.value = false), 2000);
      errorMsg.value = err.message;
    });
}

function getPieData(counts, key) {
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

onActivated(() => {
  fetchSummary();
});

</script>

<template>
  <div>
    <v-container class="md:flex max-w-1000px <sm:p-1">
      <v-card flat>
        <v-card-item>
          <div class="text-h6 mb-1">
            User Count:
            <router-link
              to="/alluser"
              class="text-blue-500 text-decoration: underline"
            >
              {{ countUser }}
            </router-link>
          </div>
          <div class="text-h6 mb-1">
            Verified Learnware Count:
            <router-link
              class="text-blue-500 text-decoration: underline"
              to="/alllearnware?is_verify=true"
              >{{ countVerifiedLearnware }}
            </router-link>
          </div>
          <div class="text-h6 mb-1">
            Unverified Learnware Count:
            <router-link
              class="text-blue-500 text-decoration: underline"
              to="/alllearnware?is_verify=false"
              >{{ countUnverifiedLearnware }}</router-link
            >
          </div>
          <div class="text-h6 mb-1">Download Count: {{ countDownload }}</div>
        </v-card-item>
      </v-card>
    </v-container>

    <v-container flat class="flex max-w-1000px <sm:p-1">
      <v-card>
        <v-card-item>
          <div class="text-h6 mb-1">Details</div>
        </v-card-item>
        <v-card-item>
          <div class="flex">
            <v-container v-for="key in Object.keys(countDetail)" :key="key">
              <Pie
                :data="getPieData(countDetail[key], key)"
                :options="options"
                :width="150"
              />
            </v-container>
          </div>
        </v-card-item>
      </v-card>
    </v-container>
  </div>
</template>
