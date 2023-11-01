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
    :class="items.length === 0 ? ['!grid-cols-1', 'h-1/1'] : null"
    :style="{ gridTemplateColumns: `repeat(${realCols}, minmax(0, 1fr))` }"
  >
    <TransitionGroup name="fade">
      <div v-if="items && items.length > 0" flat class="item">
        <div class="row">
          <div class="columns">
            <div class="title">
              {{ t("AllUser.Username") }}
            </div>
            <div class="title">
              {{ t("AllUser.Email") }}
            </div>
            <div class="title">
              {{ t("AllUser.Verified") }}
            </div>
            <div class="title">
              {{ t("AllUser.Unverified") }}
            </div>
            <div class="title">
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
            <div class="title">
              <span class="small-title">Username: </span>
              <span class="link">
                <router-link :to="{ name: 'UserLearnware', query: { user_id: item.id } }">
                  {{ item.username }}
                </router-link>
              </span>
            </div>
            <div class="title"><span class="small-title">Email: </span>{{ item.email }}</div>
            <div class="title">
              <span class="small-title">Verified: </span>{{ item.verified_learnware_count }}
            </div>
            <div class="title">
              <span class="small-title">Unverified: </span>{{ item.unverified_learnware_count }}
            </div>
            <div class="title flex">
              <span class="small-title mr-2">IsAdmin: </span>
              <v-checkbox
                class="title"
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
        @apply grid sm: "grid-cols-[3fr,3fr,1fr,1fr,1fr]" w-1/1;

        .title {
          @apply xl: text-1rem lg:text-lg text-sm sm: (flex flex-col items-start justify-center);
          .link {
            @apply underline;
          }
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
