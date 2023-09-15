<script setup>
import { ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useDisplay } from "vuetify";
import { debounce } from "../../utils";

const { t, locale } = useI18n();

const display = useDisplay();

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
      if (
        Object.keys(json.Description)
          .map(Number)
          .reduce((a, b) => Math.max(a, b)) >= Number(json.Dimension)
      ) {
        return debouncedSetErrorMessages(
          "key 'Description' should not have index greater than 'Dimension'",
        );
      }
      descriptionJSON.value = json;
      debouncedSetErrorMessages("");
    } catch (e) {
      debouncedSetErrorMessages(e.message);
    }
  },
);
</script>

<template>
  <div class="mt-3">
    <v-alert type="info" color="primary" closable>
      <slot v-if="['sm', 'xs'].includes(display.name.value)" name="msg-small" />
      <slot v-else name="msg" />
    </v-alert>
    <v-container class="mt-3">
      <v-row>
        <v-col cols="12" md="6" class="flex flex-col max-h-[600px]">
          <v-virtual-scroll :items="descriptionArray">
            <template #default="{ index: idx }">
              <v-hover>
                <template #default="{ isHovering, props: hoverProps }">
                  <div v-bind="hoverProps">
                    <v-text-field
                      v-model="descriptionArray[idx]"
                      :label="`${t('Public.Description')}: ${name} ${idx}`"
                      class="mb-1"
                      hide-details
                    >
                      <template v-if="isHovering" #append-inner>
                        <v-icon
                          class="mr-1"
                          icon="mdi-plus"
                          @click="() => descriptionArray.splice(idx, 0, null)"
                        />
                        <v-icon
                          icon="mdi-delete"
                          @click="
                            () => (descriptionArray = descriptionArray.filter((_, i) => i !== idx))
                          "
                        />
                      </template>
                    </v-text-field>
                  </div>
                </template>
              </v-hover>
            </template>
          </v-virtual-scroll>
          <div>
            <v-btn block flat class="mt-1" @click="descriptionArray = [...descriptionArray, null]">
              <v-icon size="large" color="#555">mdi-plus</v-icon>
            </v-btn>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="max-h-[600px]">
          <div class="h-full overflow-y-scroll">
            <v-textarea
              v-model="descriptionString"
              auto-grow
              :label="`${name}${locale != 'zh' ? ' ' : ''}${t('Public.Description')}`"
              :error-messages="errorMessages"
            />
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
