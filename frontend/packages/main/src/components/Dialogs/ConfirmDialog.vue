<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ modelValue: boolean }>();
const emits = defineEmits(["confirm", "update:modelValue"]);

const dialog = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emits("update:modelValue", value);
  },
});

function emitConfirm(): void {
  emits("confirm");
  dialog.value = false;
}
</script>

<template>
  <v-dialog
    v-model="dialog"
    class="mx-auto w-full max-w-[600px]"
  >
    <v-card class="mx-2">
      <v-card-title class="m-2 flex">
        <v-icon
          icon="mdi-alert"
          color="red"
        />
        <slot name="title" />
      </v-card-title>
      <v-card-text>
        <slot name="text" />
      </v-card-text>
      <v-card-actions>
        <v-spacer class="flex-1" />
        <v-btn
          class="bg-red"
          @click="() => emitConfirm()"
        >
          Confirm
        </v-btn>
        <v-btn
          variant="outlined"
          @click="dialog = false"
        >
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
