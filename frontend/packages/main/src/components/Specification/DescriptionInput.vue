<script setup lang="ts">
import { ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { debounce } from "../../utils";

export interface Props {
  name: string;
  modelValue: {
    Dimension: number;
    Description: Record<number, string>;
  };
}

const { t, locale } = useI18n();

const emits = defineEmits(["update:modelValue"]);

const props = defineProps<Props>();

const errorMessages = ref<string>("");

const descriptionJSON = ref(props.modelValue);
const descriptionArray = ref<(string | null)[]>(
  [...new Array(props.modelValue.Dimension)].map(
    (_, idx) => props.modelValue?.Description[idx] || null,
  ),
);
const descriptionString = ref(JSON.stringify(props.modelValue, null, 2));

const dragging = ref(false);

const debouncedSetErrorMessages = debounce<string>((val) => {
  errorMessages.value = val;
}, 500);

const handleDrop = (event: DragEvent): void => {
  dragging.value = false;
  if (event.dataTransfer?.files) {
    event.dataTransfer.files[0].text().then((text) => {
      descriptionString.value = text;
    });
  }
};

watch(
  () => descriptionJSON.value,
  (newVal, oldVal) => {
    if (JSON.stringify(newVal) === JSON.stringify(oldVal)) return;
    descriptionArray.value = [...new Array(newVal.Dimension)].map(
      (_, idx) => newVal.Description[idx] || null,
    );
    descriptionString.value = JSON.stringify(newVal, null, 2);
    emits("update:modelValue", newVal);
  },
);
watch(
  () => JSON.stringify(descriptionArray.value),
  (newVal) => {
    const newValJSON = JSON.parse(newVal);
    descriptionJSON.value = {
      Dimension: newValJSON.length,
      Description: newValJSON.reduce(
        (acc: { [key: string]: string | null }, cur: string | null, idx: number) => {
          cur && (acc[String(idx)] = cur);
          return acc;
        },
        {},
      ),
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
      const error = e as Error;
      debouncedSetErrorMessages(error.message);
    }
  },
);
</script>

<template>
  <div class="grid grid-cols-1 gap-0 overflow-auto md:grid-cols-2 md:gap-3">
    <div class="flex max-h-[600px] flex-col">
      <v-virtual-scroll
        v-if="modelValue.Dimension > 7"
        :items="descriptionArray"
        class="flex-1"
      >
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
                  <template
                    v-if="isHovering"
                    #append-inner
                  >
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
      <template v-else>
        <v-hover
          v-for="(_description, idx) in descriptionArray"
          :key="idx"
        >
          <template #default="{ isHovering, props: hoverProps }">
            <div v-bind="hoverProps">
              <v-text-field
                v-model="descriptionArray[idx]"
                :label="`${t('Public.Description')}: ${name} ${idx}`"
                class="mb-1"
                hide-details
              >
                <template
                  v-if="isHovering"
                  #append-inner
                >
                  <v-icon
                    class="mr-1"
                    icon="mdi-plus"
                    @click="() => descriptionArray.splice(idx, 0, null)"
                  />
                  <v-icon
                    icon="mdi-delete"
                    @click="() => (descriptionArray = descriptionArray.filter((_, i) => i !== idx))"
                  />
                </template>
              </v-text-field>
            </div>
          </template>
        </v-hover>
      </template>
      <div>
        <v-btn
          block
          variant="flat"
          class="mt-1"
          @click="descriptionArray = [...descriptionArray, null]"
        >
          <v-icon
            size="large"
            color="#555"
          >
            mdi-plus
          </v-icon>
        </v-btn>
      </div>
    </div>

    <div class="max-h-[600px]">
      <div class="h-full overflow-y-auto">
        <v-textarea
          v-model="descriptionString"
          auto-grow
          class="relative rounded"
          :class="dragging ? 'drag-hover' : ''"
          :label="`${name}${locale != 'zh-cn' ? ' ' : ''}${t('Public.Description')}`"
          :error-messages="errorMessages"
          :messages="t('Public.TryDragYourJSONFileHere')"
          @drop.prevent="handleDrop"
          @dragover.prevent
          @dragenter.prevent="dragging = true"
          @dragleave.prevent="dragging = false"
        >
          <template #prepend>
            <div
              v-if="dragging"
              class="pointer-events-none absolute bottom-0 left-0 right-0 top-0 z-10 flex flex-col items-center justify-center rounded border-2 border-dashed border-gray-500 bg-gray-200 text-lg opacity-80"
            >
              {{ t("Public.DropYourJSONFileHere") }}
            </div>
          </template>
        </v-textarea>
      </div>
    </div>
  </div>
</template>
