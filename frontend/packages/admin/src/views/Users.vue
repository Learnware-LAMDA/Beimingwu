<script setup lang="ts">
import { ref, computed, onActivated, watch } from "vue";
import { useDisplay } from "vuetify";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { fetchex, saveContentToFile } from "../utils";
import SuccessDialog from "@/components/Dialogs/SuccessDialog.vue";
import ConfirmDialog from "@/components/Dialogs/ConfirmDialog.vue";
import PageUserList from "@/components/User/PageUserList.vue";
import type { User, Filter } from "@beiming-system/types/user";

const display = useDisplay();

const store = useStore();
const router = useRouter();

const { t } = useI18n();

const deleteDialog = ref<InstanceType<typeof ConfirmDialog>>(null);
const deleteId = ref("");
const deleteName = ref("");

const resetDialog = ref<InstanceType<typeof ConfirmDialog>>(null);
const resetId = ref<string>("");
const resetName = ref<string>("");

const newPasswordDialog = ref<InstanceType<typeof SuccessDialog>>(null);
const newPassword = ref("");

const showError = ref(false);
const errorMsg = ref("");
const errorTimer = ref<number>();

const userName = ref("");
const email = ref("");

const page = ref(1);
const pageSize = ref(Math.ceil(display.height.value / 900) * 10);
const pageNum = ref(1);
const userItems = ref<User[]>([]);

const loading = ref(false);

const filters = computed(() => ({
  userName: userName.value,
  email: email.value,
}));

function fetchByFilterAndPage(filters: Filter, page: number): Promise<void> {
  loading.value = true;
  showError.value = false;

  return fetchex("/api/admin/list_user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: filters.userName,
      email: filters.email,
      limit: pageSize.value,
      page: page - 1,
    }),
  })
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
          user_list: User[];
          total_pages: number;
        };
      }) => {
        if (res.code === 0) {
          if (res.data && res.data.user_list) {
            return res;
          }
        }
        if (res.code === 11 || res.code === 12) {
          store.dispatch("logout");
          router.go(0);
        }
        throw new Error(res.msg);
      },
    )
    .then((res) => {
      userItems.value = res.data.user_list;
      pageNum.value = res.data.total_pages;
      loading.value = false;
    })
    .catch((err) => {
      loading.value = false;
      showError.value = true;
      errorMsg.value = err.message;
    });
}

function resetPassword(id: number): Promise<void> {
  return fetchex("/api/admin/reset_password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
    }),
  })
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
          password: string;
        };
      }) => {
        if (res.code === 0) {
          return res;
        }
        throw new Error(res.msg);
      },
    )
    .then((res) => {
      newPasswordDialog.value && newPasswordDialog.value.show();
      newPassword.value = res.data.password;
    })
    .catch((err) => {
      console.error(err);
      showError.value = true;
      errorMsg.value = err.message;
      clearTimeout(errorTimer.value);
      errorTimer.value = Number(
        setTimeout(() => {
          showError.value = false;
        }, 3000),
      );
    });
}

function deleteUser(id: number): Promise<void> {
  return fetchex("/api/admin/delete_user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: id,
    }),
  })
    .then((res) => {
      if (res && res.status === 200) {
        return res;
      }
      throw new Error("Network error");
    })
    .then((res) => res.json())
    .then((res: { code: number; msg: string }) => {
      if (res.code === 0) {
        return res;
      }
      throw new Error(res.msg);
    })
    .then(() => {
      store.commit("setShowGlobalError", true);
      store.commit("setGlobalErrorMsg", "Delete successfully.");

      userItems.value.splice(
        userItems.value.findIndex((item) => item.id === id),
        1,
      );

      fetchByFilterAndPage(filters.value, page.value);
    })
    .catch((err) => {
      console.error(err);
      showError.value = true;
      errorMsg.value = err.message;
      clearTimeout(errorTimer.value);
      errorTimer.value = Number(
        setTimeout(() => {
          showError.value = false;
        }, 3000),
      );
    });
}

function pageChange(newPage: number): void {
  page.value = newPage;
}

function handleClickReset(id: number): void {
  resetDialog.value && resetDialog.value.confirm();
  resetId.value = String(id);
  const userName = userItems.value.find((item) => item.id === id)?.username;
  userName && (resetName.value = userName);
}

function handleClickDelete(id: number): void {
  deleteDialog.value.confirm();
  deleteId.value = String(id);
  const userName = userItems.value.find((item) => item.id === id)?.username;
  userName && (deleteName.value = userName);
}

async function handleClickExport(): Promise<void> {
  const table = [["Username", "Email", "Verified", "Unverified"]];
  for (let _page = 1; _page <= pageNum.value; _page++) {
    await fetchex("/api/admin/list_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: filters.value.userName,
        email: filters.value.email,
        limit: pageSize.value,
        page: _page - 1,
      }),
    })
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
            user_list: User[];
            total_pages: number;
          };
        }) => {
          if (res.code === 0) {
            if (res.data && res.data.user_list) {
              return res;
            }
          }
          if (res.code === 11 || res.code === 12) {
            store.dispatch("logout");
            router.go(0);
          }
          throw new Error(res.msg);
        },
      )
      .then((res) => {
        for (const user of res.data.user_list) {
          table.push([
            user.username,
            user.email,
            String(user.verified_learnware_count),
            String(user.unverified_learnware_count),
          ]);
        }
      })
      .catch((err) => {
        console.error(err);
        showError.value = true;
        errorMsg.value = err.message;
        clearTimeout(errorTimer.value);
        errorTimer.value = Number(
          setTimeout(() => {
            showError.value = false;
          }, 3000),
        );
      });
  }
  const csvContent = "\ufeff" + table.map((e) => e.join(",")).join("\n");
  saveContentToFile(csvContent, "user_list.csv");
}

watch(
  () => filters.value,
  () => (page.value = 1),
  { deep: true },
);

watch(
  () => [filters.value, page.value],
  (newVal) => {
    const [newFilters, newPage] = newVal as [Filter, number];

    fetchByFilterAndPage(newFilters, newPage);
  },
  { deep: true },
);

onActivated(() => {
  fetchByFilterAndPage(filters.value, page.value);
});
</script>

<template>
  <div class="main-container">
    <confirm-dialog ref="resetDialog" @confirm="() => resetPassword(Number(resetId))">
      <template #title>
        Confirm to reset password of &nbsp; <b>{{ resetName }}</b
        >?
      </template>
      <template #text>
        Password of user <b>{{ resetName }}</b> will be reset <i>permanently</i>. Do you really want
        to reset?
      </template>
    </confirm-dialog>

    <success-dialog ref="newPasswordDialog" @close="() => {}">
      <template #title>
        Password of &nbsp; <b>{{ resetName }}</b> &nbsp; has been reset.
      </template>
      <template #text>
        Password of user <b>{{ resetName }}</b> has been reset to {{ newPassword }}. Please save the
        new password.
      </template>
    </success-dialog>

    <confirm-dialog ref="deleteDialog" @confirm="() => deleteUser(Number(deleteId))">
      <template #title>
        Confirm to delete &nbsp; <b>{{ deleteName }}</b
        >?
      </template>
      <template #text>
        User <b>{{ deleteName }}</b> will be deleted in the user list <i>permanently</i>. Do you
        really want to delete?
      </template>
    </confirm-dialog>

    <v-scroll-y-transition class="fixed left-0 right-0 z-index-10000">
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
    <v-card flat class="search">
      <div class="search-row">
        <v-card-title>
          {{ t("AllUser.SearchByUsername") }}
          <v-spacer></v-spacer>
          <v-text-field
            v-model="userName"
            :label="t('AllUser.Username')"
            single-line
            hide-details
            append-inner-icon="mdi-close"
            @click:append-inner="userName = ''"
          ></v-text-field>
        </v-card-title>
        <v-card-title>
          {{ t("AllUser.SearchByEmail") }}
          <v-spacer></v-spacer>
          <v-text-field
            v-model="email"
            :label="t('AllUser.Email')"
            single-line
            hide-details
            append-inner-icon="mdi-close"
            @click:append-inner="email = ''"
          ></v-text-field>
        </v-card-title>
      </div>
    </v-card>
    <page-user-list
      class="users"
      :items="userItems"
      :cols="1"
      :show-actions="true"
      :page="page"
      :page-size="pageSize"
      :page-num="pageNum"
      :loading="loading"
      :show-pagination="pageNum > 1"
      @click:delete="(id: number) => handleClickDelete(id)"
      @click:reset="(id: number) => handleClickReset(id)"
      @click:export="handleClickExport"
      @page-change="pageChange"
    />
  </div>
</template>

<style scoped lang="scss">
.main-container {
  @apply mx-auto w-1/1 h-1/1 max-w-1500px overflow-hidden;

  .search {
    @apply mt-3 w-1/1 max-w-1500px border-1 z-1000;

    .search-row {
      @apply grid md: grid-cols-2;
    }
  }
}
</style>
