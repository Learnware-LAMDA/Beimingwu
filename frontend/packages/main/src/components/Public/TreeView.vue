<script lang="ts" setup>
import { ref } from "vue";

export interface TreeViewProps {
  items: string[];
}

defineProps<TreeViewProps>();

const showDetails = ref<boolean>(false);

function toggleDetails() {
  showDetails.value = !showDetails.value;
}
</script>

<template>
  <div>
    <slot
      name="title"
      :showDetails="showDetails"
      :toggleDetails="toggleDetails"
      @click="showDetails = !showDetails"
    >
      <h3
        class="hover:bg-active-light dark:bg-active-dark cursor-pointer p-3"
        @click="() => (showDetails = !showDetails)"
      >
        <v-icon>mdi-folder</v-icon>
        folder
      </h3>
    </slot>

    <v-expand-transition>
      <div
        v-if="showDetails"
      >
        <div
          v-for="(item, i) in items"
          :key="i"
        >
          <slot
            name="items"
            :item="item"
          >
            <div class="flex items-center">
              <v-icon>mdi-file</v-icon>
              {{ item }}
            </div>
          </slot>
        </div>
      </div>
    </v-expand-transition>
  </div>
</template>
