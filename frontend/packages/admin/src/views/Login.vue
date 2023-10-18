<script setup lang="ts">
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useField } from "hooks";
import { fetchex } from "../utils";
import collaborationImg from "@/assets/images/collaboration.svg?url";

const store = useStore();

const router = useRouter();

const email = useField<string>({
  defaultValue: "",
  validate: (value) => {
    if (!value) {
      return "Email is required";
    }
    if (!value.includes("@")) {
      return "Email is invalid";
    }
    return "";
  },
});
const password = useField<string>({
  defaultValue: "",
  validate: (value) => {
    if (!value) {
      return "Password is required";
    }
    return "";
  },
});

const showPassword = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const success = ref(false);

const errorTimer = ref<number>();

const valid = computed(() => {
  return email.valid && password.valid;
});

function login(): Promise<void> {
  if (!valid.value) {
    showError.value = true;
    errorMsg.value = "Please fill in all fields";
    clearTimeout(errorTimer.value);
    errorTimer.value = Number(
      setTimeout(() => {
        showError.value = false;
      }, 3000),
    );
    return Promise.reject();
  }
  showError.value = false;

  const data = {
    email: email.value,
    password: password.value,
  };

  return fetchex("/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((res) => {
      if (res && res.status === 200) {
        return res;
      }
      throw new Error("Network error");
    })
    .then((res) => res.json())
    .then((res) => {
      switch (res.code) {
        case 0: {
          localStorage.setItem("token", res.data.token);
          return;
        }
        default: {
          throw new Error(res.msg);
        }
      }
    })
    .then(() =>
      fetchex("/api/auth/get_role", {
        method: "POST",
      }),
    )
    .then((res) => {
      if (res && res.status === 200) {
        return res;
      }
      throw new Error("Network error");
    })
    .then((res) => res.json())
    .then((res) => {
      switch (res.code) {
        case 0: {
          return res;
        }
        default: {
          throw new Error(res.msg);
        }
      }
    })
    .then((res) => {
      if (res.data && res.data.role === 1) {
        success.value = true;
        setTimeout(() => {
          store.dispatch("login");
          router.push("/");
        }, 1000);
        return;
      }
      throw new Error("Permission denied");
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
  showError.value = false;
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
              @click:close="() => closeErrorAlert"
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
              v-model="email.value"
              label="E-mail"
              :error-messages="email.errorMessages"
            ></v-text-field>
            <v-text-field
              v-model="password.value"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showPassword ? 'text' : 'password'"
              label="Password"
              :error-messages="password.errorMessages"
              @click:append="showPassword = !showPassword"
              @keyup.enter="login"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn block class="bg-primary py-5" color="white" :disabled="!valid" @click="login"
            >Login</v-btn
          >
        </v-card-actions>
      </v-card>
    </div>
  </div>
</template>
