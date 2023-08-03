<script setup>
import { ref, onActivated } from "vue";
import { createToken, listToken, deleteToken } from "../request/user";

const tokens = ref([]);

const showError = ref(false);
const errorMsg = ref("");

function fetchList() {
  showError.value = false;
  listToken()
    .then((res) => {
      switch (res.code) {
        case 0: {
          tokens.value = res.data.token_list;
          return;
        }
        default: {
          throw new Error(res.msg);
        }
      }
    })
    .catch((err) => {
      console.error(err);
      showError.value = true;
      errorMsg.value = err.message;
    });
}

function onGenerateClick() {
  createToken()
    .then((res) => {
      switch (res.code) {
        case 0: {
          fetchList();
          return;
        }
        default: {
          throw new Error(res.msg);
        }
      }
    })
    .catch((err) => {
      console.error(err);
      showError.value = true;
      errorMsg.value = err.message;
    });
}

function onDeleteClick(token) {
  deleteToken({ token })
    .then((res) => {
      switch (res.code) {
        case 0: {
          fetchList();
          return;
        }
        default: {
          throw new Error(res.msg);
        }
      }
    })
    .catch((err) => {
      console.error(err);
      showError.value = true;
      errorMsg.value = err.message;
    });
}

onActivated(() => {
  fetchList();
});
</script>

<template>
  <v-container class="h-1/1 <sm:p-0">
    <v-card class="relative max-w-600px w-1/1 m-auto" flat>
      <v-card-title>
        <div class="text-h4">Client Token</div>
      </v-card-title>
      <v-card-subtitle></v-card-subtitle>
      <v-divider class="border-black"></v-divider>
      <v-card-text>
        <div>Tokens you have generated that can be used to access the learnware api.</div>
      </v-card-text>
      <v-card-text
        v-for="(token, index) in tokens"
        :key="index"
        class="flex items-center"
        style="border: 1px solid black; border-radius: 5px; margin: 5px 0;"
      >
        <div>
          {{ token }}
        </div>
        <v-spacer></v-spacer>
        <v-btn flat icon="mdi-delete" @click="() => onDeleteClick(token)"></v-btn>
      </v-card-text>
      <v-card-actions>
        <v-btn variant="outlined" @click="onGenerateClick">Generate</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<style scoped lang="scss">
.fixed {
  height: calc(100% - var(--v-layout-top));
}
</style>
