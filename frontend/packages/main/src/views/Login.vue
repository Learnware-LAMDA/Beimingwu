<script setup lang="ts">
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useField } from "@beiming-system/hooks";
import { login, sendResetPasswordEmail } from "../request/auth";
import SuccessDialog from "../components/Dialogs/SuccessDialog.vue";
import { hex_md5 } from "../utils";
import collaborationImg from "../assets/images/public/collaboration.svg?url";

const store = useStore();

const { t } = useI18n();

const router = useRouter();

const email = useField<string>({
  defaultValue: "",
  validate: (value) => {
    if (!/^[a-z.-_]+@([a-z.-]+\.[a-z]+|localhost)$/i.test(value)) {
      return t("Login.Error.InvalidEmail");
    }
    return "";
  },
});
const password = useField<string>({
  defaultValue: "",
  validate: (value) => {
    if (value?.length >= 8) return "";

    return t("Login.Error.PasswordAtLeast8Chars");
  },
});

const showPassword = ref(false);
const showError = ref(false);
const showResetPassword = ref(false);
const showResetPasswordDialog = ref(false);
const errorMsg = ref("");
const success = ref(false);

const errorTimer = ref<number>();

const valid = computed(() => email.valid && password.valid);

function submit(): Promise<void> {
  return login({
    email: email.value,
    passwordMd5: hex_md5(password.value),
  })
    .then((res) => {
      switch (res.code) {
        case 0: {
          success.value = true;
          setTimeout(() => {
            store.dispatch("login");
            router.push("/");
          }, 1000);

          localStorage.setItem("token", res.data.token);

          return;
        }
        default: {
          if (res.code == 52) {
            showResetPassword.value = true;
          }
          showError.value = true;
          errorMsg.value = res.msg;
          clearTimeout(errorTimer.value);
          errorTimer.value = Number(setTimeout(() => (showError.value = false), 3000));
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

function showErrorMessage(msg: string): void {
  showError.value = true;
  errorMsg.value = msg;
  clearTimeout(errorTimer.value);
  errorTimer.value = Number(
    setTimeout(() => {
      showError.value = false;
    }, 3000),
  );
}

function onResetPassword(): void {
  sendResetPasswordEmail(email.value)
    .then((res) => {
      if (res.code === 0) {
        showResetPasswordDialog.value = true;
      } else {
        showErrorMessage(res.msg);
      }
    })
    .catch((err) => {
      showErrorMessage(err.message);
    });
}
</script>

<template>
  <div class="flex h-full bg-gray-100">
    <div
      class="hidden h-full w-full md:block"
      :style="{
        background: `url(${collaborationImg})`,
        backgroundSize: 'contain',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center center',
      }"
    />
    <div
      class="fill-height md:text-md flex w-full flex-row items-center justify-center p-2 text-xs sm:text-sm"
    >
      <v-card
        flat
        class="mx-auto w-full"
        max-width="500"
      >
        <div class="p-2 sm:p-7">
          <v-scroll-y-transition>
            <v-card-actions v-if="showError">
              <v-alert
                v-model="showError"
                closable
                :text="errorMsg"
                type="error"
                @click:close="closeErrorAlert"
              />
            </v-card-actions>
          </v-scroll-y-transition>
          <v-scroll-y-transition>
            <v-card-actions v-if="success">
              <v-alert
                closable
                :text="t('Login.Success')"
                type="success"
              />
            </v-card-actions>
          </v-scroll-y-transition>
          <v-card-title>
            <h1 class="text-h5 sm:text-1.3em m-2 my-6 sm:my-2">
              {{ t("Login.Login") }}
            </h1>
          </v-card-title>
          <v-card-text>
            <v-form ref="form">
              <v-text-field
                v-model="email.value"
                :label="t('Login.Email')"
                :error-messages="email.errorMessages"
                type="text"
                name="login"
                autocomplete="username"
              />
              <v-text-field
                v-model="password.value"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPassword ? 'text' : 'password'"
                :label="t('Login.Password')"
                :error-messages="password.errorMessages"
                @click:append="showPassword = !showPassword"
                @keyup.enter="submit"
              />
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn
              block
              class="bg-primary py-5"
              color="white"
              :disabled="!valid"
              @click="submit"
            >
              {{ t("Login.Login") }}
            </v-btn>
          </v-card-actions>
          <v-card-actions>
            {{ t("Login.NoAccount") }}
            <v-spacer class="flex-1" />
            <v-btn
              variant="text"
              color="primary"
              @click="router.push('/register')"
            >
              {{ t("Login.RegisterFirst") }}
            </v-btn>
            <v-btn
              v-if="showResetPassword"
              variant="text"
              color="primary"
              @click="onResetPassword"
            >
              {{ t("Login.ResetPassword") }}
            </v-btn>
          </v-card-actions>
        </div>
      </v-card>
      <success-dialog v-model="showResetPasswordDialog">
        <template #msg>
          <h2 class="mb-8 mt-6 text-lg">
            {{ t("Login.ResetPasswordSent") }}
          </h2>
        </template>

        <template #buttons>
          <v-btn
            class="text-none"
            color="primary"
            rounded
            variant="outlined"
            width="90"
            @click="() => (showResetPasswordDialog = false)"
          >
            Close
          </v-btn>
        </template>
      </success-dialog>
    </div>
  </div>
</template>
