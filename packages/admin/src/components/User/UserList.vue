<script setup>
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import oopsImg from '/oops.svg?url'

const emits = defineEmits(['click:reset', 'click:delete', 'click:export'])

const display = useDisplay()

const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
  cols: {
    type: Number,
    default: 2,
  },
  md: {
    type: Number,
    default: 1,
  },
  sm: {
    type: Number,
    default: 1,
  },
  xs: {
    type: Number,
    default: 1,
  }
})

const realCols = computed(() => {
  switch (display.name.value) {
    case 'md': if (props.md) return props.md
    case 'sm': if (props.sm) return props.sm
    case 'xs': if (props.xs) return props.xs
    default: return props.cols
  }
})

function handleClickReset(id) {
  emits('click:reset', id)
}

function handleClickDelete(id) {
  emits('click:delete', id)
}

function handleClickExport() {
  emits('click:export')
}
</script>

<template>
  <div class="user-list-container" :class="items.length === 0 ? ['!grid-cols-1', 'h-1/1'] : null"
    :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }">
    <TransitionGroup name="fade">
      <div flat class="item" v-if="items && items.length > 0">
        <div class="row">
          <div class="columns">
            <div class="title">Username</div>
            <div class="title">Email</div>
            <div class="title">Verified</div>
            <div class="title">Unverified</div>
          </div>
          <v-card-actions class="actions">
            <v-btn class="opacity-0" icon="mdi-lock-reset" disabled=""></v-btn>
            <v-btn @click="handleClickExport" icon="mdi-file-export"></v-btn>
          </v-card-actions>
        </div>
      </div>
      <div class="item" v-for="(item, i) in items" :key="i">
        <div class="row">
          <div class="columns">
            <div class="title"><span class="small-title">Username: </span>{{ item.username }}</div>
            <div class="title"><span class="small-title">Email: </span>{{ item.email }}</div>
            <div class="title"><span class="small-title">Verified: </span>{{ item.verified_learnware_count }}</div>
            <div class="title"><span class="small-title">Unverified: </span>{{ item.unverified_learnware_count }}</div>
          </div>
          <v-card-actions class="actions">
            <v-btn icon="mdi-lock-reset" @click.stop="() => handleClickReset(item.id)"></v-btn>
            <v-btn icon="mdi-delete" @click.stop="() => handleClickDelete(item.id)"></v-btn>
          </v-card-actions>
        </div>
      </div>
    </TransitionGroup>
    <div flat v-if="items.length === 0" class="no-user">
      Oops! There are no users.
      <v-img class="oops-img" width="100" :src="oopsImg"></v-img>
    </div>
  </div>
</template>

<style scoped lang="scss">
.user-list-container {
  @apply relative p-1;

  .item:nth-child(1) {
    @apply border-t-1 sm: visible <sm:hidden;

    .columns {
      @apply font-weight-bold;
    }
  }

  .item:nth-child(2) {
    @apply <sm: border-t-1;
  }

  .item {
    @apply px-3 <sm:py-3 border-1 border-t-0;

    .row {
      @apply flex items-center;

      .columns {
        @apply grid sm: "grid-cols-[3fr,3fr,1fr,1fr]" w-1/1;

        .title {
          @apply xl: text-1rem lg:text-lg text-xs;

          .small-title {
            @apply sm: hidden font-weight-bold;
          }
        }
      }

      .actions {
        @apply '!p-0' justify-end;
      }
    }
  }

  .no-user {
    @apply flex flex-col justify-center items-center w-1/1 bottom-0 text-2xl;

    .oops-img {
      @apply mx-auto;
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  @apply transition duration-500;
}

.fade-enter,
.fade-leave-to {
  @apply opacity-0;
}
</style>