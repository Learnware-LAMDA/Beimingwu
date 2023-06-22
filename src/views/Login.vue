<script setup>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useField, useForm } from "vee-validate";
import { login } from "../request/auth";
import { hex_md5 } from "../utils";
import collaborationImg from "../assets/images/public/collaboration.svg?url";

const store = useStore();

const router = useRouter();

const { handleSubmit, meta } = useForm({
  validationSchema: {
    email(value) {
      if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true;

      return "Must be a valid e-mail.";
    },
    password(value) {
      if (value?.length >= 8) return true;

      return "Password needs to be at least 8 characters.";
    },
  },
});

const email = useField("email");
const password = useField("password");

const showPassword = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const success = ref(false);

const errorTimer = ref(null);

const valid = computed(() => meta.value.valid);

const submit = handleSubmit((values) => {
  login({
    email: values.email,
    passwordMd5: hex_md5(values.password),
  })
    .then((res) => {
      switch (res.code) {
        case 0: {
          success.value = true;
          setTimeout(() => {
            store.commit("setLoggedIn", true);
            router.push("/");
          }, 1000);
          return;
        }
        default: {
          showError.value = true;
          errorMsg.value = res.msg;
          clearTimeout(errorTimer.value);
          errorTimer.value = setTimeout(() => (showError.value = false), 3000);
        }
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

function closeErrorAlert() {
  clearTimeout(errorTimer.value);
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
    ></div>
    <div
      class="flex flex-row justify-center items-center w-1/1 fill-height p-2 md:text-md sm:text-sm text-xs"
    >
      <v-card flat class="mx-auto w-1/1 sm:p-7 p-2" max-width="500">
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
            <v-alert closable text="Login successfully" type="success" />
          </v-card-actions>
        </v-scroll-y-transition>
        <v-card-title>
          <h1 class="text-h5 !text-1.3em !<sm:(text-1.6em my-6) m-2">Login</h1>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
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
              @keyup.enter="submit"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn block class="bg-primary py-5" color="white" :disabled="!valid" @click="submit"
            >Login</v-btn
          >
        </v-card-actions>
        <v-card-actions>
          Don't have an account?
          <v-spacer></v-spacer>
          <v-btn variant="text" color="primary" @click="router.push('/register')"
            >Register first</v-btn
          >
        </v-card-actions>
      </v-card>
    </div>
  </div>
</template>
