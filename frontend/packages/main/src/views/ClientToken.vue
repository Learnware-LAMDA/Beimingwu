<script setup lang="ts">
import { ref, onActivated } from "vue";
import { useI18n } from "vue-i18n";
import { createToken, listToken, deleteToken } from "../request/user";

const { t } = useI18n();

const tokens = ref<string[]>([]);

const showError = ref(false);
const errorMsg = ref("");

function fetchList(): Promise<void> {
  showError.value = false;
  return listToken()
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

function onGenerateClick(): Promise<void> {
  return createToken()
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

function onDeleteClick(token: string): Promise<void> {
  return deleteToken({ token })
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
  <v-container class="h-full p-0 sm:p-2">
    <v-card class="relative m-auto w-full max-w-[600px]" flat>
      <v-card-title>
        <div class="text-h4">
          {{ t("ClientToken.Title") }}
        </div>
      </v-card-title>
      <v-card-subtitle></v-card-subtitle>
      <v-divider class="border-black"></v-divider>
      <v-card-text>
        <div>
          {{ t("ClientToken.Description") }}
        </div>
      </v-card-text>
      <v-card-text
        v-for="(token, index) in tokens"
        :key="index"
        class="flex items-center"
        style="border: 1px solid black; border-radius: 5px; margin: 5px 0"
      >
        <div>
          {{ token }}
        </div>
        <v-spacer class="flex-1"></v-spacer>
        <v-btn variant="flat" icon="mdi-delete" @click="() => onDeleteClick(token)"></v-btn>
      </v-card-text>
      <v-card-actions>
        <v-btn variant="outlined" @click="onGenerateClick">
          {{ t("ClientToken.Generate") }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<style scoped lang="scss">
.fixed {
  height: calc(100% - var(--v-layout-top));
}
</style>
