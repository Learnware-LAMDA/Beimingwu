<script setup>
import { ref, watch } from "vue";
import { debounce } from "../../utils";

const emits = defineEmits(["update:value"]);

const props = defineProps({
  name: {
    type: String,
    required: false,
    default: "feature",
  },
  value: {
    type: Object,
    required: true,
  },
});

const errorMessages = ref("");

const descriptionJSON = ref(props.value);
const descriptionArray = ref(
  [...new Array(props.value.Dimension)].map((_, idx) => props.value?.Description[idx] || null),
);
const descriptionString = ref(JSON.stringify(props.value, null, 2));

const debouncedSetErrorMessages = debounce((val) => {
  errorMessages.value = val;
}, 500);

watch(
  () => descriptionJSON.value,
  (newVal, oldVal) => {
    if (JSON.stringify(newVal) === JSON.stringify(oldVal)) return;
    descriptionArray.value = [...new Array(newVal.Dimension)].map(
      (_, idx) => newVal.Description[idx] || null,
    );
    descriptionString.value = JSON.stringify(newVal, null, 2);
    emits("update:value", newVal);
  },
);
watch(
  () => JSON.stringify(descriptionArray.value),
  (newVal) => {
    newVal = JSON.parse(newVal);
    descriptionJSON.value = {
      Dimension: newVal.length,
      Description: newVal.reduce((acc, cur, idx) => {
        cur && (acc[idx] = cur);
        return acc;
      }, {}),
    };
  },
);
watch(
  () => descriptionString.value,
  (val) => {
    try {
      const json = JSON.parse(val);
      if (json.Dimension === undefined)
        return debouncedSetErrorMessages("key 'Dimension' not found");
      if (!json.Dimension) return debouncedSetErrorMessages("key 'Dimension' should not be empty");
      if (json.Description === undefined)
        return debouncedSetErrorMessages("key 'Description' not found");
      if (!json.Description)
        return debouncedSetErrorMessages("key 'Description' should not be empty");
      descriptionJSON.value = json;
      debouncedSetErrorMessages("");
    } catch (e) {
      debouncedSetErrorMessages(e.message);
    }
  },
);
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          v-for="(_, idx) in descriptionArray"
          :key="idx"
          v-model="descriptionArray[idx]"
          :label="`${name} ${idx}`"
          class="mt-1"
          hide-details
          prepend-icon="mdi-plus"
          append-icon="mdi-delete"
          append-inner-icon="mdi-close"
          @click:prepend="() => descriptionArray.splice(idx, 0, null)"
          @click:append="() => (descriptionArray = descriptionArray.filter((_, i) => i !== idx))"
          @click:append-inner="
            () => (descriptionArray = descriptionArray.map((_, i) => (i === idx ? null : _)))
          "
        />
        <v-btn block flat class="mt-1" @click="descriptionArray = [...descriptionArray, null]">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-col>
      <v-col cols="12" md="6">
        <v-textarea
          v-model="descriptionString"
          auto-grow
          class="flex flex-col"
          :label="`${name.slice(0, 1).toUpperCase()}${name.slice(1)} Description`"
          :error-messages="errorMessages"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.v-input__control,
textarea {
  height: 100% !important;
}
</style>
