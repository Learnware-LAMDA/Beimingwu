<script setup>
import { ref, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'
import { useRouter } from 'vue-router'
import { useField, useForm } from 'vee-validate'

const display = useDisplay()

const store = useStore()

const router = useRouter()

const elevationClass = computed(() => {
  if (display.name.value === 'xs') {
    return null
  } else {
    return 'elevation-8'
  }
})

const { handleSubmit, meta } = useForm({
  initialValues: {
    email: 'a@a.a',
    password: 'aaaaaaaa',
  },
  validationSchema: {
    email(value) {
      if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true

      return 'Must be a valid e-mail.'
    },
    password(value) {
      if (value?.length >= 8) return true

      return 'Password needs to be at least 8 characters.'
    },
  },
})


const email = useField('email')
const password = useField('password')

const showPassword = ref(false)
const showError = ref(false)
const errorMsg = ref('')
const success = ref(false)

const errorTimer = ref(null)

const valid = computed(() => {
  return meta.value.valid
})

const login = handleSubmit(values => {
  const data = {
    email: values.email,
    password: values.password,
  }

  fetch('/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  })
    .then((res) => {
      if (res.status === 200) {
        return res
      }
      throw new Error('Network error')
    })
    .then((res) => res.json())
    .then((res) => {
      switch (res.code) {
        case 0: {
          success.value = true
          setTimeout(() => {
            store.commit('setLoggedIn', true)
            router.push('/')
          }, 1000)
          return
        }
        default: {
          showError.value = true
          errorMsg.value = res.msg
          clearTimeout(errorTimer.value)
          errorTimer.value = setTimeout(() => showError.value = false, 3000)
        }
      }
    })
    .catch((err) => {
      showError.value = true
      errorMsg.value = err.message
      clearTimeout(errorTimer.value)
      errorTimer.value = setTimeout(() => { showError.value = false }, 3000)
    })
})

function closeErrorAlert() {
  clearTimeout(errorTimer.value)
}
</script>

<template>
  <div class="flex flex-row justify-center items-center fill-height p-2 md:text-md sm:text-sm text-xs bg-gray-100">
    <v-card flat class="mx-auto w-1/1 p-4" :class="elevationClass" max-width="500">
      <v-card-title>
        <h1 class="text-lg-h4 text-h5 m-2">Login</h1>
      </v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field v-model="email.value.value" label="E-mail"
            :error-messages="email.errorMessage.value"></v-text-field>
          <v-text-field v-model="password.value.value" :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showPassword ? 'text' : 'password'" label="Password" :error-messages="password.errorMessage.value"
            @click:append="showPassword = !showPassword"></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions v-if="success">
        <v-alert closable text="Login successfully" type="success" />
      </v-card-actions>
      <v-scale-transition>
        <v-card-actions v-if="showError">
          <v-alert v-model="showError" closable :text="errorMsg" type="error" @click:close="() => closeErrorAlert" />
        </v-card-actions>
      </v-scale-transition>
      <v-card-actions>
        <v-btn block class="bg-primary py-5" color="white" @click="login" :disabled="!valid">Login</v-btn>
      </v-card-actions>
      <v-card-actions>
        Don't have an account?
        <v-spacer></v-spacer>
        <v-btn variant="text" color="primary" @click="router.push('/register')">Register first</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>