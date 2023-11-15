<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";
import { useI18n } from "vue-i18n";
import oopsImg from "/oops.svg?url";
import type { User } from "@beiming-system/types/user";

const emits = defineEmits(["click:reset", "click:delete", "click:export", "click:setRole"]);

const display = useDisplay();

const { t } = useI18n();

export interface Props {
  items: User[];
  cols?: number;
  md?: number;
  sm?: number;
  xs?: number;
  enableSetRole?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  cols: 2,
  md: 1,
  sm: 1,
  xs: 1,
});

const realCols = computed(() => {
  if (display.name.value === "xs") {
    return props.xs;
  }
  if (display.name.value === "sm") {
    return props.sm;
  }
  if (display.name.value === "md") {
    return props.md;
  }
  return props.cols;
});

function handleClickReset(id: number): void {
  emits("click:reset", id);
}

function handleClickDelete(id: number): void {
  emits("click:delete", id);
}

function handleClickExport(): void {
  emits("click:export");
}

function handleClickSetRole(id: number, role: number): void {
  emits("click:setRole", id, role);
}
</script>

<template>
  <div
    class="user-list-container"
    :class="items.length === 0 ? ['grid-cols-1', 'h-full'] : null"
    :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
  >
    <TransitionGroup name="fade">
      <div v-if="items && items.length > 0" flat class="item">
        <div class="row">
          <div class="columns">
            <div class="my-title">
              {{ t("AllUser.Username") }}
            </div>
            <div class="my-title">
              {{ t("AllUser.Email") }}
            </div>
            <div class="my-title">
              {{ t("AllUser.Verified") }}
            </div>
            <div class="my-title">
              {{ t("AllUser.Unverified") }}
            </div>
            <div class="my-title">
              {{ t("AllUser.IsAdmin") }}
            </div>
          </div>
          <v-card-actions class="actions">
            <v-btn class="opacity-0" icon="mdi-lock-reset" disabled=""></v-btn>
            <v-btn icon="mdi-file-export" @click="handleClickExport"></v-btn>
          </v-card-actions>
        </div>
      </div>
      <div v-for="(item, i) in items" :key="i" class="item">
        <div class="row">
          <div class="columns">
            <div class="my-title">
              <span class="small-title">Username: </span>
              <span class="link">
                <router-link :to="{ name: 'UserLearnware', query: { user_id: item.id } }">
                  {{ item.username }}
                </router-link>
              </span>
            </div>
            <div class="my-title"><span class="small-title">Email: </span>{{ item.email }}</div>
            <div class="my-title">
              <span class="small-title">Verified: </span>{{ item.verified_learnware_count }}
            </div>
            <div class="my-title">
              <span class="small-title">Unverified: </span>{{ item.unverified_learnware_count }}
            </div>
            <div class="my-title flex">
              <span class="small-title mr-2">IsAdmin: </span>
              <v-checkbox
                class="my-title"
                :model-value="item.role >= 1"
                :disabled="!enableSetRole || item.email === 'admin@localhost'"
                @click.prevent="handleClickSetRole(item.id, item.role == 1 ? 0 : 1)"
                density="dense"
                hide-details
              ></v-checkbox>
            </div>
          </div>
          <v-card-actions class="actions">
            <v-btn icon="mdi-lock-reset" @click.stop="() => handleClickReset(item.id)"></v-btn>
            <v-btn icon="mdi-delete" @click.stop="() => handleClickDelete(item.id)"></v-btn>
          </v-card-actions>
        </div>
      </div>
    </TransitionGroup>
    <div v-if="items.length === 0" flat class="no-user">
      {{ t("AllUser.OopsNoUser") }}
      <v-img class="oops-img" width="100" :src="oopsImg"></v-img>
    </div>
  </div>
</template>

<style scoped lang="scss">
.user-list-container {
  @apply relative p-1;

  .item:nth-child(1) {
    @apply hidden border-t sm:block;

    .columns {
      @apply font-bold;
    }
  }

  .item:nth-child(2) {
    @apply border-t sm:border-t-0;
  }

  .item {
    @apply border border-t-0 px-3 py-3 sm:py-0;

    .row {
      @apply flex items-center;

      .columns {
        @apply grid w-full sm:grid-cols-[3fr,3fr,1fr,1fr,1fr];

        .my-title {
          @apply text-sm sm:flex sm:flex-col sm:items-start sm:justify-center lg:text-lg xl:text-base;
          .link {
            @apply underline;
          }
          .small-title {
            @apply font-bold sm:hidden;
          }
        }
      }

      .actions {
        @apply justify-end p-0;
      }
    }
  }

  .no-user {
    @apply bottom-0 flex w-full flex-col items-center justify-center text-2xl;

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
