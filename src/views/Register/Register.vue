<script setup>
import { ref, computed } from 'vue'
import { useDisplay } from 'vuetify'
import { useField, useForm } from 'vee-validate'
import RegSucDialog from '@/components/User/RegSucDialog.vue'

const display = useDisplay()

const elevationClass = computed(() => {
  if (display.name.value === 'xs') {
    return null
  } else {
    return 'elevation-8'
  }
})

const { handleSubmit, meta } = useForm({
  validationSchema: {
    userName(value) {
      if (value?.length >= 2) return true

      return 'Username needs to be at least 2 characters.'
    },
    email(value) {
      if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true

      return 'Must be a valid e-mail.'
    },
    password(value) {
      if (value?.length >= 8) return true

      return 'Password needs to be at least 8 characters.'
    },
    password2(value) {
      if (value && value === password.value.value) return true
      if (!value) return 'Password cannot be empty.'
      return 'Password does not match.'
    },
  },
})

const userName = useField('userName')
const email = useField('email')
const password = useField('password')
const password2 = useField('password2')

const showPassword = ref(false)
const showPassword2 = ref(false)
const showError = ref(false)
const errorMsg = ref('')
const success = ref(false)

const errorTimer = ref(null)

const valid = computed(() => {
  return meta.value.valid
})

const submit = handleSubmit(values => {
  const data = {
    username: values.userName,
    email: values.email,
    password: values.password,
  }

  fetch('/api/auth/register', {
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
        case 0: return success.value = true
        case 21: {
          throw new Error('System error')
        }
        case 51: return userName.setErrors(res.msg)
        case 52: return email.setErrors(res.msg)
      }
    })
    .catch((err) => {
      showError.value = true
      errorMsg.value = err.message
      clearTimeout(errorTimer.value)
      errorTimer.value = setTimeout(() => { showError.value = false }, 3000)
    })
})
</script>

<template>
  <div class="flex flex-row justify-center items-center fill-height p-2 md:text-md sm:text-sm text-xs bg-gray-100">
    <reg-suc-dialog v-if="success" />

    <v-card flat class="mx-auto w-1/1 p-4" :class="elevationClass" max-width="500">
      <v-card-title>
        <h1 class="text-lg-h4 text-h5 my-2">Register</h1>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field v-model="userName.value.value" label="Username" :counter="20"
            :error-messages="userName.errorMessage.value"></v-text-field>
          <v-text-field v-model="email.value.value" label="E-mail"
            :error-messages="email.errorMessage.value"></v-text-field>
          <v-text-field v-model="password.value.value" :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showPassword ? 'text' : 'password'" label="Password" :error-messages="password.errorMessage.value"
            @click:append="showPassword = !showPassword"></v-text-field>
          <v-text-field v-model="password2.value.value" :append-icon="showPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showPassword2 ? 'text' : 'password'" label="Confirm Password"
            :error-messages="password2.errorMessage.value" @click:append="showPassword2 = !showPassword2"></v-text-field>
        </v-form>
      </v-card-text>
      <v-scale-transition>
        <v-card-actions v-if="showError">
          <v-alert v-model="showError" closable :text="errorMsg" type="error" @click:close="() => closeErrorAlert" />
        </v-card-actions>
      </v-scale-transition>
      <v-card-actions>
        <v-btn block class="bg-primary py-5" color="white" @click="submit" :disabled="!valid">Register</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>