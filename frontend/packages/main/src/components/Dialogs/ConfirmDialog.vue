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
    <v-card>
      <div class="flex p-5 text-lg font-medium sm:text-xl">
        <v-icon
          class="mr-1"
          icon="mdi-alert"
          color="warning"
        />
        <slot name="title" />
      </div>
      <div class="p-4">
        <slot name="text" />
      </div>
      <div class="flex justify-end space-x-2 p-4">
        <v-btn
          variant="flat"
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
      </div>
    </v-card>
  </v-dialog>
</template>
