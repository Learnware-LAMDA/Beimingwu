<script setup>
import { ref, computed } from "vue";
import { useDisplay } from "vuetify";
import colors from "vuetify/lib/util/colors";
import AudioBtn from "../../assets/images/specification/dataType/audio.svg?component";
import VideoBtn from "../../assets/images/specification/dataType/video.svg?component";
import TextBtn from "../../assets/images/specification/dataType/text.svg?component";
import ImageBtn from "../../assets/images/specification/dataType/image.svg?component";
import TableBtn from "../../assets/images/specification/dataType/table.svg?component";
import { downloadLearnwareSync } from "../../utils";

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  filters: {
    type: Object,
    default: () => ({}),
  },
  showDownload: {
    type: Boolean,
    default: true,
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["click:edit", "click:delete"]);

const display = useDisplay();

const greaterThanXs = computed(() => display.name.value !== "xs");

const greaterThanSm = computed(() => display.name.value !== "xs" && display.name.value !== "sm");

const showEditTips = ref(props.item.showEditTips);

const dataTypeBtns = {
  Table: TableBtn,
  Image: ImageBtn,
  Text: TextBtn,
  Video: VideoBtn,
  Audio: AudioBtn,
};

function getColorByScore(score) {
  if (score > 80) return colors.green.base;
  if (score > 50) return colors.orange.base;
  return colors.red.base;
}

function handleClickEdit(id) {
  emit("click:edit", id);
}

function handleClickDelete(id) {
  emit("click:delete", id);
}
</script>

<template>
  <v-card
    flat
    :density="greaterThanXs ? 'comfortable' : 'compact'"
    class="card"
    :class="typeof item.matchScore === 'number' ? ['pt-2'] : ['py-2']"
  >
    <div class="first-row">
      <v-card-title class="title">
        <v-avatar :size="greaterThanSm ? 'default' : 'small'">
          <component :is="dataTypeBtns[item.dataType]" class="w-4/5 opacity-70" />
        </v-avatar>
        {{ `${item.username ? item.username + "/" : ""}${item.name}` }}
      </v-card-title>
    </div>
    <v-card-subtitle>
      <div style="color: red">
        {{ item.verifyStatus != undefined && item.verifyStatus != "SUCCESS" ? "Unverified" : "" }}
      </div>
    </v-card-subtitle>
    <v-card-text class="card-text">
      <div
        class="label"
        :class="
          filters && filters.dataType && filters.dataType.includes(item.dataType)
            ? 'active'
            : undefined
        "
      >
        {{ item.dataType }}
      </div>
      <div
        class="label"
        :class="
          filters && filters.taskType && filters.taskType.includes(item.taskType)
            ? 'active'
            : undefined
        "
      >
        {{ item.taskType.replace("Others", "Other Task") }}
      </div>
      <div
        class="label"
        :class="
          filters && filters.libraryType && filters.libraryType.includes(item.libraryType)
            ? 'active'
            : undefined
        "
      >
        {{ item.libraryType.replace("Others", "Other Library") }}
      </div>
      <div
        v-for="(tag, i) in item.tagList"
        :key="i"
        class="tag"
        :class="filters && filters.tagList && filters.tagList.includes(tag) ? 'active' : undefined"
      >
        {{ tag }}
      </div>
    </v-card-text>
    <v-card-text class="card-text">
      <div class="description">{{ item.description }}</div>
    </v-card-text>
    <v-card-title
      class="last-row"
      :class="
        typeof item.matchScore === 'number'
          ? ['justify-between']
          : isAdmin
          ? ['justify-end']
          : ['absolute', 'right-0', 'bottom-0']
      "
    >
      <div v-if="typeof item.matchScore === 'number'" class="xl: text-xl lg:text-lg text-1rem">
        Specification score
        <span class="ml-2 text-xl" :style="`color: ${getColorByScore(item.matchScore)}`">{{
          item.matchScore
        }}</span>
      </div>
      <div class="actions">
        <v-tooltip v-model="showEditTips" location="top">
          <template #activator="{ toolTipProps }">
            <v-btn
              v-if="isAdmin"
              flat
              icon="mdi-pencil"
              v-bind="toolTipProps"
              :size="greaterThanXs ? undefined : 'small'"
              @click.stop="() => handleClickEdit(item.id)"
            ></v-btn>
          </template>
          <span>Not availble</span>
        </v-tooltip>
        <v-btn
          v-if="showDownload"
          flat
          icon="mdi-download"
          :size="greaterThanXs ? undefined : 'small'"
          @click.stop="() => downloadLearnwareSync(item.id)"
        ></v-btn>
        <v-btn
          v-if="isAdmin"
          flat
          icon="mdi-delete"
          :size="greaterThanXs ? undefined : 'small'"
          @click.stop="handleClickDelete(item.id)"
        ></v-btn>
      </div>
    </v-card-title>
  </v-card>
</template>

<style scoped lang="scss">
.card {
  @apply sm: (border-1 hover: (border-1 border-purple-500)) <sm: (border-b-1 rounded-0px);

  .first-row {
    @apply flex justify-between items-start;

    .title {
      @apply xl: text-xl lg:text-lg text-1rem;
    }
  }

  .last-row {
    @apply flex items-center;

    .actions {
      @apply flex flex-row justify-end;

      * {
        @apply <sm: mx-0;
      }
    }
  }

  .card-text {
    @apply flex flex-wrap items-center pt-0 pb-2 text-gray-700;

    * {
      @apply mr-2 mt-1;
    }

    .label {
      @apply px-2 border-gray-700 bg-gray-400 text-xs text-white rounded;
    }

    .tag {
      @apply px-2 border-gray-700 bg-gray-400 text-xs text-white rounded-1em;
    }

    .label.active {
      background: rgb(var(--v-theme-primary));
    }

    .tag.active {
      @apply bg-orange-600;
    }

    .description {
      @apply truncate;
    }
  }

  .placeholder {
    @apply opacity-0;
  }
}
</style>
