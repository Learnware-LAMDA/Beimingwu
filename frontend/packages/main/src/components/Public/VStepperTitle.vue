<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";

export interface Props {
  currentStep: number;
  stepTitle: string;
  steps: {
    icon: string;
    title: string;
    subtitle: string;
  }[];
}

const display = useDisplay();

const greaterThanMd = computed(() => ["lg", "xl"].includes(display.name.value));

const emit = defineEmits(["active-step"]);

const props = defineProps<Props>();

const isStepActive = (index: number): boolean => props.currentStep === index;

const activeStep = (index: number): void => {
  emit("active-step", index);
};
</script>

<template>
  <div class="mx-auto w-full p-2">
    <div class="stepper-box">
      <div class="steps-wrapper">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="step"
          @click="() => activeStep(index)"
        >
          <div class="icon">
            <div
              class="circle"
              :class="isStepActive(index) ? 'bg-primary' : 'bg-grey-lighten-1'"
            >
              <v-icon
                :icon="step.icon"
                color="white"
                :size="greaterThanMd ? '1.5rem' : '1rem'"
              >
              </v-icon>
              <div class="divider-line"></div>
            </div>
          </div>
          <div class="step-title">
            <h4 class="text-sm md:text-lg">{{ `${stepTitle} ${index + 1}` }}</h4>
            <h5 class="md:texg-sm text-xs">{{ step.subtitle }}</h5>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.stepper-box {
  @apply relative;

  .steps-wrapper {
    @apply flex items-center justify-between md:mx-5;

    .step {
      @apply mx-2 flex cursor-pointer flex-col items-center;

      .icon {
        @apply bg-white p-1 md:p-3;

        .circle {
          @apply flex items-center justify-center rounded-full p-3;
        }
      }

      .step-title {
        @apply text-center;
      }
    }
  }

  .divider-line {
    @apply absolute left-[10%] -z-10 w-4/5 border md:border-2;
  }
}
</style>
