<script setup>
import { ref, computed, watch } from 'vue'
import { useDisplay } from 'vuetify'

const emit = defineEmits(['update:value'])

const display = useDisplay()

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
})

const realCols = computed(() => {
  console.log(display.xs.value)
  let cols = props.cols
  if (props.md && display.md.value) {
    cols = props.md
  } else if (props.sm && display.sm.value) {
    cols = props.sm
  } else if (props.xs && display.xs.value) {
    cols = props.xs
  }
  return cols
})

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
]
const search = ref('')
const selected = ref(props.value)

const allSelected = computed(() => selected.value.length === items.length)
const categories = computed(() => {
  const _search = search.value.toLowerCase()

  if (!_search) return items

  return items.filter(item => {
    const text = item.text.toLowerCase()

    return text.indexOf(_search) > -1
  })
})
const selections = computed(() => [...selected.value])

watch(
  () => selected.value,
  () => search.value = ''
)

watch(
  () => selections.value,
  (newVal) => emit('update:value', newVal.map(item => item.text))
)
</script>

<template>
<v-card class="container" flat>
  <div class="title">Tag</div>
  <div class="items">
    <div class="item" v-for="(selection, i) in selections" :key="selection.text">
      <v-chip class="chip bg-orange-500 text-white" closable @click:close="selected.splice(i, 1)">
        <v-icon :icon="selection.icon" start></v-icon>

        {{ selection.text }}
      </v-chip>
    </div>
  </div>

  <div class="search" v-if="!allSelected" cols="12">
    <v-text-field v-model="search" hide-details label="Search" single-line append-inner-icon="mdi-close" @click:append-inner="search = ''"></v-text-field>
  </div>

  <v-divider v-if="!allSelected"></v-divider>

  <v-list class="list" :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }">
    <template v-for="item in categories">
      <v-list-item v-if="!selected.includes(item)" :key="item.text" @click="selected.push(item)">
        <template v-slot:prepend>
          <v-icon :icon="item.icon"></v-icon>
        </template>

        <v-list-item-title v-text="item.text"></v-list-item-title>
      </v-list-item>
    </template>
  </v-list>
</v-card>
</template>

<style scoped lang="scss">
.container {
  .title {
    @apply my-2;
  }

  .items {
    @apply flex flex-wrap my-2;

    .item {
      @apply py-1 pe-0;

      .chip {
        @apply "!p-5" mr-2;
      }
    }
  }
  
  .list {
    @apply grid gap-2;
  }
}
</style>