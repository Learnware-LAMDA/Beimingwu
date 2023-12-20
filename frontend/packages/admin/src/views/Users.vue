<script setup lang="ts">
import { ref, computed, onMounted, onActivated } from "vue";
import { watchDebounced } from "@vueuse/core";
import { useDisplay } from "vuetify";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { fetchex, saveContentToFile } from "../utils";
import { BACKEND_URL } from "@main/constants";
import SuccessDialog from "@main/components/Dialogs/SuccessDialog.vue";
import ConfirmDialog from "@main/components/Dialogs/ConfirmDialog.vue";
import PageUserList from "@admin/components/User/PageUserList.vue";
import type { User, Filter } from "@beiming-system/types/user";

const display = useDisplay();

const store = useStore();
const route = useRoute();
const router = useRouter();

const { t } = useI18n();

const showDeleteDialog = ref(false);
const deleteId = ref("");
const deleteName = ref("");

const showResetDialog = ref(false);
const resetId = ref<string>("");
const resetName = ref<string>("");

const newPasswordDialog = ref<boolean>(false);
const newPassword = ref("");

const showSetRoleDialog = ref<boolean>(false);
const setRoleId = ref<number>(-1);
const setRoleRole = ref<number>(0);
const setRoleName = ref<string>("");

const showError = ref(false);
const errorMsg = ref("");
const errorTimer = ref<number>();

const userName = ref("");
const email = ref("");
const verifyStatus = ref<string[]>([]);
const allVerifyStatus = ref<string[]>(["verified", "unverified"]);
const isVerified = computed(() => {
  if (verifyStatus.value.includes("verified") && verifyStatus.value.includes("unverified")) {
    return undefined;
  }
  if (verifyStatus.value.includes("verified")) {
    return true;
  }
  if (verifyStatus.value.includes("unverified")) {
    return false;
  }
  return undefined;
});

const page = ref(1);
const pageSize = ref(Math.ceil(display.height.value / 900) * 10);
const pageNum = ref(1);
const userItems = ref<User[]>([]);

const loading = ref(false);

const filters = computed<Filter>(() => ({
  userName: userName.value,
  email: email.value,
  verifyStatus: isVerified.value,
}));

function fetchByFilterAndPage(filters: Filter, page: number): Promise<void> {
  loading.value = true;
  showError.value = false;

  return fetchex(BACKEND_URL + "/admin/list_user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: filters.userName,
      email: filters.email,
      is_verified: filters.verifyStatus,
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
  return fetchex(BACKEND_URL + "/admin/reset_password", {
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
      newPasswordDialog.value = true;
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
  return fetchex(BACKEND_URL + "/admin/delete_user", {
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
  showResetDialog.value = true;
  resetId.value = String(id);
  const userName = userItems.value.find((item) => item.id === id)?.username;
  userName && (resetName.value = userName);
}

function handleClickDelete(id: number): void {
  showDeleteDialog.value = true;
  deleteId.value = String(id);
  const userName = userItems.value.find((item) => item.id === id)?.username;
  userName && (deleteName.value = userName);
}

function handleClickSetRole(id: number, role: number): void {
  showSetRoleDialog.value = true;
  setRoleId.value = Number(id);
  setRoleRole.value = Number(role);
  const userName = userItems.value.find((item) => item.id === id)?.username;
  userName && (setRoleName.value = userName);
}

function setRole(id: number, role: number): Promise<void> {
  return fetchex(BACKEND_URL + "/admin/set_user_role", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: id,
      role: role,
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
      store.commit("setGlobalErrorMsg", "set successfully.");
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

async function handleClickExport(): Promise<void> {
  const table = [["Username", "Email", "Verified", "Unverified"]];
  for (let _page = 1; _page <= pageNum.value; _page++) {
    await fetchex(BACKEND_URL + "/admin/list_user", {
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
  saveContentToFile(csvContent, "text/csv;charset=utf-8", "user_list.csv");
}

watchDebounced(
  () => filters.value,
  () => (page.value = 1),
  { deep: true, debounce: 500 },
);

watchDebounced(
  () => [filters.value, page.value],
  (newVal) => {
    const [newFilters, newPage] = newVal as [Filter, number];

    fetchByFilterAndPage(newFilters, newPage);

    window.scrollTo(0, 0);
  },
  { deep: true, debounce: 300 },
);

onMounted(() => {
  fetchByFilterAndPage(filters.value, page.value);
});

onActivated(() => {
  if (route.query.is_verified) {
    if (route.query.is_verified === "true") {
      verifyStatus.value = ["verified"];
    } else if (route.query.is_verified === "false") {
      verifyStatus.value = ["unverified"];
    }
  }
});
</script>

<template>
  <div class="main-container">
    <confirm-dialog
      v-model="showResetDialog"
      @confirm="() => resetPassword(Number(resetId))"
    >
      <template #title>
        Confirm to reset password of&nbsp;
        <b> {{ resetName }} </b>?
      </template>
      <template #text>
        Password of user <b>{{ resetName }}</b> will be reset <i>permanently</i>. Do you really want
        to reset?
      </template>
    </confirm-dialog>

    <success-dialog v-model="newPasswordDialog">
      <template #msg>
        <v-card-text class="text-lg">
          Password of user <b>{{ resetName }}</b> has been reset to {{ newPassword }}. Please save
          the new password.
        </v-card-text>
      </template>
      <template #buttons>
        <v-btn
          class="text-none mr-3"
          color="primary"
          rounded
          variant="outlined"
          @click="newPasswordDialog = false"
        >
          OK
        </v-btn>
      </template>
    </success-dialog>

    <confirm-dialog
      v-model="showDeleteDialog"
      @confirm="() => deleteUser(Number(deleteId))"
    >
      <template #title>
        Confirm to delete&nbsp;
        <b> {{ deleteName }} </b>?
      </template>
      <template #text>
        User <b>{{ deleteName }}</b> will be deleted in the user list <i>permanently</i>. Do you
        really want to delete?
      </template>
    </confirm-dialog>

    <confirm-dialog
      v-model="showSetRoleDialog"
      @confirm="() => setRole(Number(setRoleId), Number(setRoleRole))"
    >
      <template #title>
        Confirm to set role of &nbsp; <b>{{ setRoleName }}</b
        >?
      </template>
      <template #text>
        User <b>{{ setRoleName }}</b> will be set as
        <i>{{ setRoleRole === 1 ? "admin" : "normal" }} user</i>. Do you really want to do this?
      </template>
    </confirm-dialog>

    <v-scroll-y-transition class="fixed left-0 right-0 z-50">
      <v-card-actions v-if="showError">
        <v-alert
          class="mx-auto w-full max-w-[900px]"
          closable
          :text="errorMsg"
          type="error"
          @click:close="showError = false"
        />
      </v-card-actions>
    </v-scroll-y-transition>
    <v-card
      flat
      class="search"
    >
      <v-card-title>
        {{ t("AllUser.Search") }}
      </v-card-title>
      <div class="grid grid-cols-1 lg:grid-cols-[3fr_3fr_2fr]">
        <div class="p-2">
          <v-text-field
            v-model="userName"
            :label="t('AllUser.SearchByUsername')"
            hide-details
            append-inner-icon="mdi-close"
            @click:append-inner="userName = ''"
          />
        </div>
        <div class="p-2">
          <v-spacer class="flex-1" />
          <v-text-field
            v-model="email"
            :label="t('AllUser.SearchByEmail')"
            hide-details
            append-inner-icon="mdi-close"
            @click:append-inner="email = ''"
          />
        </div>

        <div class="p-2">
          <v-combobox
            v-model="verifyStatus"
            :items="allVerifyStatus"
            :label="t('AllUser.VerifyStatus')"
            multiple
            hide-details
          >
            <template #selection="data">
              <v-chip :key="data.item.value">
                {{ t(`AllUser.${data.item.value[0].toUpperCase()}${data.item.value.slice(1)}`) }}
              </v-chip>
            </template>
            <template #item="{ item, props }">
              <v-list-item
                density="compact"
                v-bind="{
                  ...props,
                  title: t(
                    `AllUser.${(props.value as string)[0].toUpperCase()}${(
                      props.value as string
                    ).slice(1)}`,
                  ),
                }"
              >
                <template #prepend>
                  <v-checkbox
                    :model-value="verifyStatus.includes(item.value)"
                    density="comfortable"
                    hide-details
                  />
                </template>
              </v-list-item>
            </template>
          </v-combobox>
        </div>
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
      :enable-set-role="store.getters.getRole === 2"
      @click:delete="(id: number) => handleClickDelete(id)"
      @click:reset="(id: number) => handleClickReset(id)"
      @click:set-role="(id: number, role: number) => handleClickSetRole(id, role)"
      @click:export="handleClickExport"
      @page-change="pageChange"
    />
  </div>
</template>

<style scoped lang="scss">
.main-container {
  @apply mx-auto h-full w-full max-w-[1500px] overflow-hidden;

  .search {
    @apply z-50 mt-3 w-full max-w-[1500px] border;
  }
}
</style>
