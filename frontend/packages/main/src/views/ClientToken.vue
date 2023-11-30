<script setup lang="ts">
import { ref, onActivated, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import ConfirmDialog from "../components/Dialogs/ConfirmDialog.vue";
import { createToken, listToken, deleteToken } from "../request/user";

const { t } = useI18n();

const tokens = ref<string[]>([]);

const loading = ref(false);
const showError = ref(false);
const errorMsg = ref("");

const showSuccess = ref(false);

const showDeleteDialog = ref(false);
const tokenToDelete = ref("");

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

function handleClickCopy(token: string): void {
  navigator.clipboard.writeText(token);
  showSuccess.value = true;
}

function handleClickDelete(token: string): void {
  tokenToDelete.value = token;
  showDeleteDialog.value = true;
}

function handleDelete(token: string): Promise<void> {
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

onMounted(() => {
  fetchList();
});

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
    <v-card-title class="flex items-center py-4">
      <v-icon> mdi-key </v-icon>
      <div class="text-h4 ml-3">
        {{ t("ClientToken.Title") }}
      </div>
    </v-card-title>

    <v-card-text>
      {{ t("ClientToken.Description") }}
    </v-card-text>

    <v-card-text v-if="tokens.length > 0">
      <div class="border">
        <div
          v-for="(token, index) in tokens"
          :key="index"
          :class="{
            'border-b': index !== tokens.length - 1,
          }"
        >
          <div class="flex items-center px-2">
            {{ token }}
            <v-spacer class="flex-1" />
            <v-btn
              variant="flat"
              icon="mdi-content-copy"
              @click="() => handleClickCopy(token)"
            />
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

    <v-snackbar
      v-model="showSuccess"
      :timeout="3000"
      color="success"
    >
      {{ t("ClientToken.CopySuccess") }}
    </v-snackbar>

    <confirm-dialog
      v-model="showDeleteDialog"
      @confirm="() => handleDelete(tokenToDelete)"
    >
      <template #title>
        <span class="ml-2">{{ t("ClientToken.DeleteToken") }}</span>
      </template>
      <template #text>
        {{ t("ClientToken.YourTokenWillBeDeleted", { token: tokenToDelete }) }}
      </template>
    </confirm-dialog>
  </v-card>
</template>
