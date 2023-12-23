<script setup lang="ts">
import { computed } from "vue";
import { useDisplay } from "vuetify";

export interface Props {
  modelValue: number;
  stepTitle: string;
  steps: {
    icon: string;
    title: string;
    subtitle: string;
    check: boolean;
  }[];
}

const display = useDisplay();

const emit = defineEmits(["active-step", "update:modelValue"]);

const props = defineProps<Props>();

const modelValue = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const isStepActive = (index: number): boolean => modelValue.value === index;

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
              class="circle box-border transition-all duration-300"
              :class="[
                { 'bg-primary dark:bg-primary-dark': isStepActive(index) && !step.check },
                { 'bg-inactive dark:bg-inactive-dark': !isStepActive(index) && !step.check },
                { 'bg-success dark:bg-success-dark': step.check },
              ]"
            >
              <v-icon
                :icon="step.check && !isStepActive(index) ? 'mdi-check' : step.icon"
                color="white"
                :size="display.mdAndUp.value ? '1.5rem' : '1rem'"
              >
              </v-icon>
              <div class="divider-line"></div>
            </div>
          </div>
          <div class="step-title">
            <div class="text-sm md:text-lg">{{ `${stepTitle} ${index + 1}` }}</div>
            <div class="md:texg-sm text-xs">{{ step.subtitle }}</div>
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
      @apply bg-surface-light dark:bg-surface-dark mx-2 flex cursor-pointer flex-col items-center;

      .icon {
        @apply p-1 md:p-3;

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
