<script setup lang="ts">
import { ref, computed, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useField } from "@beiming-system/hooks";
import { useI18n } from "vue-i18n";
import SuccessDialog from "../components/Dialogs/SuccessDialog.vue";
import ErrorDialog from "../components/Dialogs/ErrorDialog.vue";
import { register } from "../request/auth";
import { hex_md5 } from "../utils";
import { resendEmail } from "../request/auth";
import { useTimeout } from "@beiming-system/hooks";
import AuthPage from "@main/components/AuthPage.vue";

const { t } = useI18n();
const router = useRouter();

const userName = useField<string>({
  defaultValue: "",
  validate: (value) => {
    if (value?.length < 2) return t("Register.Error.UsernameAtLeast2Chars");
    if (value?.length > 20) return t("Register.Error.UsernameAtMost20Chars");
    return "";
  },
});
const email = useField<string>({
  defaultValue: "",
  validate: (value) => {
    if (!/^[a-z.-_]+@[a-z.-]+\.[a-z]+$/i.test(value)) return t("Register.Error.InvalidEmail");
    if (value?.length > 50) return t("Register.Error.EmailAtMost50Chars");
    return "";
  },
});
const password = useField({
  defaultValue: "",
  validate: (value) => {
    if (value?.length < 8) return t("Register.Error.PasswordAtLeast8Chars");
    if (value?.length > 20) return t("Register.Error.PasswordAtMost20Chars");
    return "";
  },
});
const password2 = useField({
  defaultValue: "",
  validate: (value) => {
    if (value && value === password.value) return "";
    if (!value) return t("Register.Error.PasswordNotEmpty");
    return t("Register.Error.PasswordNotMatch");
  },
});
const agreeTerms = ref(false);

const showPassword = ref(false);
const showPassword2 = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const success = ref(false);
const showErrorDialog = ref(false);

const errorTimer = ref<number>();
const { ok, remain, start: startTimer, stop: stopTimer } = useTimeout(60 * 1000);

const valid = computed(
  () => userName.valid && email.valid && password.valid && password2.valid && agreeTerms.value,
);

function submit(): Promise<void> {
  if (!valid.value) return Promise.resolve();

  return register({
    username: userName.value,
    email: email.value,
    passwordMd5: hex_md5(password.value),
  })
    .then((res) => {
      switch (res.code) {
        case 0:
          success.value = true;
          return;
        case 53: {
          success.value = true;
          return;
        }
        case 21: {
          throw new Error(t("Error.UnknownError") + ": " + res.msg);
        }
        case 41: {
          showErrorDialog.value = true;
          errorMsg.value = t("Register.Error.EmailNotAllowed");
          return;
        }
        case 51: {
          userName.errorMessages = res.msg;
          return;
        }
        case 52: {
          email.errorMessages = res.msg;
          return;
        }
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

function onResend(): Promise<void> {
  return resendEmail(email.value)
    .then((res) => {
      if (res.code === 0) {
        startTimer();
      }
    })
    .catch((err) => {
      console.log(err);
    });
}

function handeClickShowUserAgreement(): void {
  window.open(t("Url.Docs.UserAgreement"));
}

function handeClickShowPrivacyPolicy(): void {
  window.open(t("Url.Docs.PrivacyPolicy"));
}

onUnmounted(() => {
  stopTimer();
});
</script>

<template>
  <auth-page>
    <success-dialog v-model="success">
      <template #msg>
        <div class="mb-8 mt-6 text-lg">
          {{ t("Register.SentEmail") }}
        </div>
      </template>
      <template #buttons>
        <v-btn
          class="mr-3"
          color="primary"
          rounded
          variant="flat"
          :disabled="!ok"
          @click="onResend()"
        >
          {{ t("Register.Resend") }} <span v-if="!ok">({{ Number(remain) / 1000 }})</span>
        </v-btn>
        <v-btn
          class="text-none"
          color="primary"
          rounded
          variant="outlined"
          width="90"
          @click="() => router.push('/login')"
        >
          {{ t("Register.Close") }}
        </v-btn>
      </template>
    </success-dialog>

    <error-dialog v-model="showErrorDialog">
      <template #msg>
        <div class="mb-8 mt-6 break-all text-lg">
          {{ errorMsg }}
        </div>
      </template>
      <template #buttons>
        <v-btn
          color="primary"
          rounded
          variant="outlined"
          width="90"
          @click="() => (showErrorDialog = false)"
        >
          {{ t("Register.Close") }}
        </v-btn>
      </template>
    </error-dialog>
    <v-scroll-y-transition>
      <v-alert
        v-if="showError"
        type="error"
      >
        {{ errorMsg }}
      </v-alert>
    </v-scroll-y-transition>

    <v-card-title>
      <div class="text-h5 sm:text-1.3em m-2 my-6 sm:my-2">
        {{ t("Register.Register") }}
      </div>
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field
          v-model="userName.value"
          :label="t('Register.Username')"
          :counter="20"
          :error-messages="userName.errorMessages"
        />
        <v-text-field
          v-model="email.value"
          :counter="50"
          :label="t('Register.Email')"
          :error-messages="email.errorMessages"
          type="text"
          name="login"
          autocomplete="username"
        />
        <v-text-field
          v-model="password.value"
          :counter="20"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword ? 'text' : 'password'"
          :label="t('Register.Password')"
          :error-messages="password.errorMessages"
          @click:append="showPassword = !showPassword"
        />
        <v-text-field
          v-model="password2.value"
          :append-icon="showPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword2 ? 'text' : 'password'"
          :label="t('Register.ConfirmPassword')"
          :error-messages="password2.errorMessages"
          @click:append="showPassword2 = !showPassword2"
          @keyup.enter="submit"
        />
      </v-form>
      <div class="flex">
        <v-checkbox
          v-model="agreeTerms"
          :label="t('Register.ReadAndAgree')"
          density="compact"
          hide-details
        ></v-checkbox>
        <v-btn
          target="_blank"
          color="primary"
          variant="text"
          @click="handeClickShowUserAgreement"
        >
          {{ t("Register.UserAgreement") }}
        </v-btn>
        <v-btn
          target="_blank"
          color="primary"
          variant="text"
          @click="handeClickShowPrivacyPolicy"
        >
          {{ t("Register.PrivacyPolicy") }}
        </v-btn>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-btn
        block
        class="bg-primary py-5"
        color="white"
        :disabled="!valid"
        @click="submit"
      >
        {{ t("Register.Register") }}
      </v-btn>
    </v-card-actions>
  </auth-page>
</template>
