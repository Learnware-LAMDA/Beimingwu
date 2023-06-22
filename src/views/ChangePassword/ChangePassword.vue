<script setup>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useField, useForm } from "vee-validate";
import { changePassword } from "../../request/user";
import { hex_md5 } from "../../utils";
import collaborationImg from "../../assets/images/public/collaboration.svg?url";

const store = useStore();

const router = useRouter();

const { handleSubmit, meta } = useForm({
  validationSchema: {
    oldPassword() {
      return true;
    },
    newPassword(value) {
      if (value?.length >= 8) return true;

      return "New password needs to be at least 8 characters.";
    },
    newPassword2(value) {
      if (value?.length >= 8) {
        if (value && value === newPassword.value.value) return true;
        return "New passwords do not match.";
      }
      return "New password needs to be at least 8 characters.";
    },
  },
});

const oldPassword = useField("oldPassword");
const newPassword = useField("newPassword");
const newPassword2 = useField("newPassword2");

const showOldPassword = ref(false);
const showNewPassword = ref(false);
const showNewPassword2 = ref(false);
const showError = ref(false);
const errorMsg = ref("");
const success = ref(false);

const errorTimer = ref(null);

const valid = computed(() => meta.value.valid);

const change = handleSubmit((values) => {
  changePassword({
    oldPasswordMd5: hex_md5(values.oldPassword),
    newPasswordMd5: hex_md5(values.newPassword),
  })
    .then((res) => {
      switch (res.code) {
        case 0: {
          success.value = true;
          setTimeout(() => {
            store.commit("setLoggedIn", false);
            router.push("/login");
          }, 1000);
          return;
        }
        case 11: {
          success.value = false;
          store.commit("setLoggedIn", false);
          setTimeout(() => {
            router.push("/login");
          }, 1000);
          throw new Error("You are not logged in.");
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
              @click:close="() => closeErrorAlert"
            />
          </v-card-actions>
        </v-scroll-y-transition>
        <v-scroll-y-transition>
          <v-card-actions v-if="success">
            <v-alert closable text="Change successfully" type="success" />
          </v-card-actions>
        </v-scroll-y-transition>
        <v-card-title>
          <h1 class="text-h5 !text-1.3em !<sm:(text-1.6em my-6) m-2">Change password</h1>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="oldPassword.value.value"
              :append-icon="showOldPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showOldPassword ? 'text' : 'password'"
              label="Old password"
              :error-messages="oldPassword.errorMessage.value"
              @click:append="showOldPassword = !showOldPassword"
            >
            </v-text-field>
            <v-text-field
              v-model="newPassword.value.value"
              :append-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showNewPassword ? 'text' : 'password'"
              label="New password"
              :error-messages="newPassword.errorMessage.value"
              @click:append="showNewPassword = !showNewPassword"
            >
            </v-text-field>
            <v-text-field
              v-model="newPassword2.value.value"
              :append-icon="showNewPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showNewPassword2 ? 'text' : 'password'"
              label="Confirm password"
              :error-messages="newPassword2.errorMessage.value"
              @click:append="showNewPassword2 = !showNewPassword2"
            >
            </v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn block class="bg-primary py-5" color="white" :disabled="!valid" @click="change">
            Change
          </v-btn>
        </v-card-actions>
      </v-card>
    </div>
  </div>
</template>
