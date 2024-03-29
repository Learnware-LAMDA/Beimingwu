<script setup lang="ts">
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useField } from "@beiming-system/hooks";
import { useI18n } from "vue-i18n";
import { changePassword } from "../request/user";
import { hex_md5 } from "../utils";
import AuthPage from "@main/components/AuthPage.vue";

const store = useStore();

const router = useRouter();

const { t } = useI18n();

const oldPassword = useField<string>({ defaultValue: "" });
const newPassword = useField<string>({
  defaultValue: "",
  validate: (value) => {
    if (value?.length >= 8) return "";

    return t("ChangePassword.Error.NewPasswordAtLeast8Chars");
  },
});
const newPassword2 = useField<string>({
  defaultValue: "",
  validate: (value) => {
    if (value?.length >= 8) {
      if (value && value === newPassword.value) return "";
      return t("ChangePassword.Error.NewPasswordNotMatch");
    }
    return t("ChangePassword.Error.NewPasswordAtLeast8Chars");
  },
});

const showOldPassword = ref(false);
const showNewPassword = ref(false);
const showNewPassword2 = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const success = ref(false);

const errorTimer = ref<number>();

const valid = computed(() => oldPassword.valid && newPassword.valid && newPassword2.valid);

function change(): Promise<void> {
  return changePassword({
    oldPasswordMd5: hex_md5(oldPassword.value),
    newPasswordMd5: hex_md5(newPassword.value),
  })
    .then((res) => {
      switch (res.code) {
        case 0: {
          success.value = true;
          setTimeout(() => {
            store.dispatch("logout");
            router.push("/login");
          }, 1000);
          return;
        }
        case 11: {
          success.value = false;
          store.dispatch("logout");
          setTimeout(() => {
            router.push("/login");
          }, 1000);
          throw new Error("You are not logged in.");
        }
        default: {
          showError.value = true;
          errorMsg.value = res.msg;
          clearTimeout(errorTimer.value);
          errorTimer.value = Number(
            setTimeout(() => {
              showError.value = false;
            }, 3000),
          );
        }
      }
    })
    .catch((err) => {
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

function closeErrorAlert(): void {
  clearTimeout(errorTimer.value);
}
</script>

<template>
  <auth-page>
    <v-scroll-y-transition>
      <v-card-actions v-if="showError">
        <v-alert
          v-model="showError"
          closable
          :text="errorMsg"
          type="error"
          @click:close="() => closeErrorAlert"
        />
      </v-card-actions>
    </v-scroll-y-transition>
    <v-scroll-y-transition>
      <v-card-actions v-if="success">
        <v-alert
          closable
          :text="t('ChangePassword.Success')"
          type="success"
        />
      </v-card-actions>
    </v-scroll-y-transition>
    <v-card-title>
      <div class="m-2 my-6 text-[1.6em] font-normal sm:my-2 sm:text-[1.3em]">
        {{ t("ChangePassword.ChangePassword") }}
      </div>
    </v-card-title>
    <v-card-text>
      <v-form ref="form">
        <v-text-field
          v-model="oldPassword.value"
          :append-icon="showOldPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showOldPassword ? 'text' : 'password'"
          :label="t('ChangePassword.OldPassword')"
          :error-messages="oldPassword.errorMessages"
          @click:append="showOldPassword = !showOldPassword"
        />
        <v-text-field
          v-model="newPassword.value"
          :append-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showNewPassword ? 'text' : 'password'"
          :label="t('ChangePassword.NewPassword')"
          :error-messages="newPassword.errorMessages"
          @click:append="showNewPassword = !showNewPassword"
        />
        <v-text-field
          v-model="newPassword2.value"
          :append-icon="showNewPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showNewPassword2 ? 'text' : 'password'"
          :label="t('ChangePassword.ConfirmNewPassword')"
          :error-messages="newPassword2.errorMessages"
          @click:append="showNewPassword2 = !showNewPassword2"
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn
        block
        class="bg-primary py-5"
        color="white"
        :disabled="!valid"
        @click="change"
      >
        {{ t("ChangePassword.Change") }}
      </v-btn>
    </v-card-actions>
  </auth-page>
</template>
