<script setup lang="ts">
import { ref } from "vue";

const emits = defineEmits(["confirm"]);

const dialog = ref(false);

function confirm(): void {
  dialog.value = true;
}

function emitConfirm(): void {
  emits("confirm");
  dialog.value = false;
}

defineExpose({
  confirm,
});
</script>

<template>
  <v-dialog v-model="dialog" class="dialog-container">
    <v-card class="dialog">
      <v-card-title class="title">
        <v-icon class="icon" icon="mdi-alert" color="red"></v-icon>
        <slot name="title" />
      </v-card-title>
      <v-card-text>
        <slot name="text" />
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn class="bg-red" @click="() => emitConfirm()"> Confirm </v-btn>
        <v-btn variant="outlined" @click="dialog = false"> Cancel </v-btn>
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
