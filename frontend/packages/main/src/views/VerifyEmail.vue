<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import { verifyEmail } from "../request/auth";

const router = useRouter();
const route = useRoute();
const msg = ref("");
const icon = ref("");
const color = ref("");

onMounted(() => {
  const urlParams = new URLSearchParams(String(route.query));
  verifyEmail(urlParams.toString())
    .then((res) => {
      switch (res.code) {
        case 0: {
          icon.value = "mdi-check-circle";
          msg.value = res.msg;
          color.value = "success";
          return;
        }
        default: {
          icon.value = "mdi-alert-circle";
          msg.value = res.msg;
          color.value = "error";
          return;
        }
      }
    })
    .catch((err) => {
      console.error(err);
    });
});
</script>

<template>
  <v-card flat class="mx-auto w-1/1 sm:p-7 p-2" max-width="500">
    <v-card-item>
      <div class="items-center justify-center flex-1 d-flex">
        <v-icon :color="color">{{ icon }}</v-icon>
        <span class="ml-2"> {{ msg }} </span>
      </div>
    </v-card-item>
    <v-card-actions>
      <div class="items-center justify-center flex-1 d-flex">
        <v-btn variant="outlined" @click="router.push({ name: 'Login' })"> Continue </v-btn>
      </div>
    </v-card-actions>
  </v-card>
</template>
