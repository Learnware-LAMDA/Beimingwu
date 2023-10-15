<script setup lang="ts">
import { ref, computed } from "vue";
import { useField } from "hooks";
import { useI18n } from "vue-i18n";
import RegSucDialog from "../components/User/RegSucDialog.vue";
import { register } from "../request/auth";
import { hex_md5 } from "../utils";
import collaborationImg from "../assets/images/public/collaboration.svg?url";

const { t } = useI18n();

const userName = useField<string>({
  defaultValue: "",
  validate: (value) => {
    if (value?.length >= 2) return "";

    return t("Register.Error.UsernameAtLeast2Chars");
  },
});
const email = useField<string>({
  defaultValue: "",
  validate: (value) => {
    if (/^[a-z.-_]+@[a-z.-]+\.[a-z]+$/i.test(value)) return "";

    return t("Register.Error.InvalidEmail");
  },
});
const password = useField({
  defaultValue: "",
  validate: (value) => {
    if (value?.length >= 8) return "";

    return t("Register.Error.PasswordAtLeast8Chars");
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

const showPassword = ref(false);
const showPassword2 = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const success = ref(false);

const errorTimer = ref<number>();

const valid = computed(() => userName.valid && email.valid && password.valid && password2.valid);

function submit(): Promise<void> {
  return register({
    username: userName.value,
    email: email.value,
    passwordMd5: hex_md5(password.value),
  })
    .then((res) => {
      switch (res.code) {
        case 0:
          return;
        case 53: {
          success.value = true;
          return;
        }
        case 21: {
          throw new Error("System error");
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
</script>

<template>
  <div class="flex h-1/1 bg-gray-100">
    <div
      class="d-md-block d-none w-1/1 h-1/1"
      :style="{
        background: `url(${collaborationImg})`,
        backgroundSize: 'contain',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center center',
      }"
    />
    <div
      class="flex flex-row justify-center items-center w-1/1 fill-height p-2 md:text-md sm:text-sm text-xs bg-gray-100"
    >
      <reg-suc-dialog v-if="success" :email="email.value" />

      <v-card flat class="mx-auto w-1/1 sm:p-6 p-2" max-width="500">
        <v-card-title>
          <h1 class="text-h5 !text-1.3em !<sm:(text-1.6em my-6) m-2 mb-5">
            {{ t("Register.Register") }}
          </h1>
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="userName.value"
              :label="t('Register.Username')"
              :counter="20"
              :error-messages="userName.errorMessages"
            ></v-text-field>
            <v-text-field
              v-model="email.value"
              :label="t('Register.Email')"
              :error-messages="email.errorMessages"
            ></v-text-field>
            <v-text-field
              v-model="password.value"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              :label="t('Register.Password')"
              :error-messages="password.errorMessages"
              @click:append="showPassword = !showPassword"
            ></v-text-field>
            <v-text-field
              v-model="password2.value"
              :append-icon="showPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword2 ? 'text' : 'password'"
              :label="t('Register.ConfirmPassword')"
              :error-messages="password2.errorMessages"
              @click:append="showPassword2 = !showPassword2"
              @keyup.enter="submit"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-scale-transition>
          <v-card-actions v-if="showError">
            <v-alert v-model="showError" closable :text="errorMsg" type="error" />
          </v-card-actions>
        </v-scale-transition>
        <v-card-actions>
          <v-btn block class="bg-primary py-5" color="white" :disabled="!valid" @click="submit">
            {{ t("Register.Register") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </div>
  </div>
</template>
