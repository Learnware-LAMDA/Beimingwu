<script setup>
import { computed } from 'vue';
import { useDisplay } from 'vuetify';

const emit = defineEmits(['update:value']);

const display = useDisplay();

const props = defineProps({
  value: {
    type: Array,
    required: true,
  },
  cols: {
    type: Number,
    default: 4,
  },
  md: {
    type: Number,
    default: 4,
  },
  sm: {
    type: Number,
    default: 2,
  },
  xs: {
    type: Number,
    default: 1,
  },
});

const realCols = computed(() => {
  let { cols } = props;
  if (props.md && display.md.value) {
    cols = props.md;
  } else if (props.sm && display.sm.value) {
    cols = props.sm;
  } else if (props.xs && display.xs.value) {
    cols = props.xs;
  }
  return cols;
});

const items = [
  {
    text: 'Business',
    icon: 'mdi-briefcase',
  },
  {
    text: 'Financial',
    icon: 'mdi-currency-usd',
  },
  {
    text: 'Health',
    icon: 'mdi-heart',
  },
  {
    text: 'Politics',
    icon: 'mdi-account-group',
  },
  {
    text: 'Computer',
    icon: 'mdi-desktop-classic',
  },
  {
    text: 'Internet',
    icon: 'mdi-earth',
  },
  {
    text: 'Traffic',
    icon: 'mdi-car',
  },
  {
    text: 'Nature',
    icon: 'mdi-tree',
  },
  {
    text: 'Fashion',
    icon: 'mdi-tshirt-crew',
  },
  {
    text: 'Industry',
    icon: 'mdi-factory',
  },
  {
    text: 'Agriculture',
    icon: 'mdi-tractor',
  },
  {
    text: 'Education',
    icon: 'mdi-school',
  },
  {
    text: 'Entertainment',
    icon: 'mdi-movie',
  },
  {
    text: 'Architecture',
    icon: 'mdi-home-city',
  },
];

const allSelected = computed(() => props.value && props.value.length === items.length);

const selections = computed(() => {
  if (props.value) {
    return props.value.map((s) => items.find((item) => item.text === s));
  }
  return [];
});

function click(text) {
  if (props.value && props.value.includes(text)) {
    deleteSelect(text);
  } else {
    addSelect(text);
  }
}

function addSelect(text) {
  if (props.value) {
    emit('update:value', [...props.value, text]);
  } else {
    emit('update:value', [text]);
  }
}

function deleteSelect(text) {
  if (props.value) {
    emit('update:value', props.value.filter((s) => s !== text));
  } else {
    emit('update:value', []);
  }
}
</script>

<template>
  <div class="tag-container" flat>
    <div class="title text-h6 !text-1rem">Scenario</div>

    <v-divider v-if="!allSelected"></v-divider>

    <div class="list" :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }">
      <template v-for="item in items" :key="item.text">
        <div :class="selections.includes(item) ? ['active'] : []" @click="() => click(item.text)" class="item text">
          <v-icon class="mr-4" :icon="item.icon"></v-icon>
          <div class="text" v-text="item.text"></div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped lang="scss">
.tag-container {
  .title {
    @apply mt-7 mb-5;
  }

  .list {
    @apply grid sm: gap-2 gap-1 bg-transparent;

    .item {
      @apply flex items-center p-3 pl-4 bg-gray-400 text-white rounded-2em cursor-pointer;
    }

    .active {
      @apply bg-orange-600;
    }

    .v-list-item {
      @apply '!overflow-visible';

      * {
        @apply '!overflow-visible';
      }
    }
  }

  .text {
    @apply lg: text-1rem sm:text-sm text-xs;
  }
}
</style>
