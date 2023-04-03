<script setup>
import { ref, defineExpose } from 'vue'

const dialog = ref(false)
const deleteName = ref('')

function confirmDelete(name) {
  deleteName.value = name
  dialog.value = true
}

defineExpose({
  confirmDelete
})
</script>

<template>
  <v-dialog v-model="dialog" class="dialog-container">
    <v-card class="dialog">
      <v-card-title class="title">
        <v-icon class="icon" icon="mdi-alert" color="red"></v-icon>
        Confirm to delete a learnware?
      </v-card-title>
      <v-card-text>Your learnware <b>{{ deleteName }}</b> will be deleted in the learnware market <i>permanently</i>. Do you really want to delete?</v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="green-darken-1" variant="text" @click="dialog = false">
          Keep
        </v-btn>
        <v-btn color="red" variant="text" @click="dialog = false">
          <v-icon icon="mdi-alert" color="red"></v-icon>Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">
.dialog-container {
  @apply mx-auto w-1/1 max-w-600px;

  .dialog {
    @apply mx-2;

    .title {
      @apply flex m-2;

      .icon {
        @apply mr-2;
      }
    }
  }
}
</style>