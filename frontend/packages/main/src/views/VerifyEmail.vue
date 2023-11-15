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
  const urlParams = new URLSearchParams();
  const code = route.query.code;
  if (!code) {
    icon.value = "mdi-alert-circle";
    msg.value = "Invalid URL";
    color.value = "error";
    return;
  }
  urlParams.append("code", code.toString());
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
  <v-card flat class="mx-auto w-full p-2 sm:p-7" max-width="500">
    <v-card-item>
      <div class="d-flex flex-1 items-center justify-center">
        <v-icon :color="color">{{ icon }}</v-icon>
        <span class="ml-2"> {{ msg }} </span>
      </div>
    </v-card-item>
    <v-card-actions>
      <div class="d-flex flex-1 items-center justify-center">
        <v-btn variant="outlined" @click="router.push({ name: 'Login' })"> Continue </v-btn>
      </div>
    </v-card-actions>
  </v-card>
</template>
