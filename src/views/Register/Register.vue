<script setup>
import { ref, computed } from "vue";
import { useField, useForm } from "vee-validate";
import RegSucDialog from "../../components/User/RegSucDialog.vue";
import { register } from "../../request/auth";
import { hex_md5 } from "../../utils";
import collaborationImg from "../../assets/images/public/collaboration.svg?url";

const { handleSubmit, meta } = useForm({
  validationSchema: {
    userName(value) {
      if (value?.length >= 2) return true;

      return "Username needs to be at least 2 characters.";
    },
    email(value) {
      if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true;

      return "Must be a valid e-mail.";
    },
    password(value) {
      if (value?.length >= 8) return true;

      return "Password needs to be at least 8 characters.";
    },
    password2(value) {
      if (value && value === password.value.value) return true;
      if (!value) return "Password cannot be empty.";
      return "Password does not match.";
    },
  },
});

const userName = useField("userName");
const email = useField("email");
const password = useField("password");
const password2 = useField("password2");

const showPassword = ref(false);
const showPassword2 = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const success = ref(false);

const errorTimer = ref(null);

const valid = computed(() => meta.value.valid);

const submit = handleSubmit((values) => {
  register({
    username: values.userName,
    email: values.email,
    passwordMd5: hex_md5(values.password),
  })
    .then((res) => {
      switch (res.code) {
        case 0:
          return (success.value = true);
        case 21: {
          throw new Error("System error");
        }
        case 51:
          return userName.setErrors(res.msg);
        case 52:
          return email.setErrors(res.msg);
      }
    })
    .catch((err) => {
      showError.value = true;
      errorMsg.value = err.message;
      clearTimeout(errorTimer.value);
      errorTimer.value = setTimeout(() => {
        showError.value = false;
      }, 3000);
    });
});
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
    ></div>
    <div
      class="flex flex-row justify-center items-center w-1/1 fill-height p-2 md:text-md sm:text-sm text-xs bg-gray-100"
    >
      <reg-suc-dialog v-if="success" />

      <v-card flat class="mx-auto w-1/1 sm:p-6 p-2" max-width="500">
        <v-card-title>
          <h1 class="text-h5 !text-1.3em !<sm:(text-1.6em my-6) m-2 mb-5">Register</h1>
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="userName.value.value"
              label="Username"
              :counter="20"
              :error-messages="userName.errorMessage.value"
            ></v-text-field>
            <v-text-field
              v-model="email.value.value"
              label="E-mail"
              :error-messages="email.errorMessage.value"
            ></v-text-field>
            <v-text-field
              v-model="password.value.value"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              label="Password"
              :error-messages="password.errorMessage.value"
              @click:append="showPassword = !showPassword"
            ></v-text-field>
            <v-text-field
              v-model="password2.value.value"
              :append-icon="showPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword2 ? 'text' : 'password'"
              label="Confirm Password"
              :error-messages="password2.errorMessage.value"
              @click:append="showPassword2 = !showPassword2"
              @keyup.enter="submit"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-scale-transition>
          <v-card-actions v-if="showError">
            <v-alert
              v-model="showError"
              closable
              :text="errorMsg"
              type="error"
              @click:close="() => closeErrorAlert"
            />
          </v-card-actions>
        </v-scale-transition>
        <v-card-actions>
          <v-btn block class="bg-primary py-5" color="white" :disabled="!valid" @click="submit"
            >Register</v-btn
          >
        </v-card-actions>
      </v-card>
    </div>
  </div>
</template>
