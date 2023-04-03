<script setup>
import { ref, defineExpose } from 'vue'

const emits = defineEmits(['confirm'])

const dialog = ref(false)
const deleteName = ref('')
const deleteId = ref('')

function confirmDelete(args) {
  const { id, name } = args
  deleteName.value = name
  deleteId.value = id
  dialog.value = true
}

function emitDelete() {
  emits('confirm', deleteId.value)
  dialog.value = false
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
        Confirm to delete &nbsp; <b>{{ deleteName }}</b>?
      </v-card-title>
      <v-card-text>Your learnware <b>{{ deleteName }}</b> will be deleted in the learnware market <i>permanently</i>. Do you really want to delete?</v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="bg-red" @click="() => emitDelete()">
          Delete
        </v-btn>
        <v-btn variant="outlined" @click="dialog = false">
          Cancel
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