<script setup lang="ts">
import { ref, onActivated } from "vue";
import { useI18n } from "vue-i18n";
import { createToken, listToken, deleteToken } from "../request/user";

const { t } = useI18n();

const tokens = ref<string[]>([]);

const loading = ref(false);
const showError = ref(false);
const errorMsg = ref("");

function fetchList(): Promise<void> {
  loading.value = true;
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
    })
    .finally(() => {
      loading.value = false;
    });
}

function handleClickGenerate(): Promise<void> {
  loading.value = true;
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
    })
    .finally(() => {
      loading.value = false;
    });
}

function handleClickDelete(token: string): Promise<void> {
  loading.value = true;
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
    })
    .finally(() => {
      loading.value = false;
    });
}

onActivated(() => {
  fetchList();
});
</script>

<template>
  <v-card
    class="m-auto mt-2 w-full max-w-[600px]"
    flat
    :loading="loading"
  >
    <v-card-title>
      <div class="text-h4">
        {{ t("ClientToken.Title") }}
      </div>
    </v-card-title>

    <v-divider />

    <v-card-text>
      {{ t("ClientToken.Description") }}
    </v-card-text>

    <v-card-text v-if="tokens.length > 0">
      <div class="rounded-md border border-black">
        <div
          v-for="(token, index) in tokens"
          :key="index"
          class="border-black"
          :class="{
            'border-b': index !== tokens.length - 1,
          }"
        >
          <div class="flex items-center px-2">
            {{ token }}
            <v-spacer class="flex-1" />
            <v-btn
              variant="flat"
              icon="mdi-delete"
              @click="() => handleClickDelete(token)"
            />
          </div>
        </div>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-btn
        block
        rounded
        @click="handleClickGenerate"
      >
        {{ t("ClientToken.Generate") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
