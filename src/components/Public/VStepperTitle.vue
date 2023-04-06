<script setup>
import { computed } from 'vue';
import { useDisplay } from 'vuetify';

const display = useDisplay();

const greaterThanMd = computed(() => ['lg', 'xl'].includes(display.name.value))

const emit = defineEmits('active-step')

const props = defineProps({
  currentStep: {
    type: Number,
    required: true,
  },
  steps: {
    type: Array,
    default: () => [
      {
        icon: 'mdi-mail',
        name: 'first',
        title: 'Sample title 1',
        subtitle: 'Subtitle sample'
      },
      {
        icon: 'mdi-alert',
        name: 'second',
        title: 'Sample title 2',
        subtitle: 'Subtitle sample'
      }
    ]
  },
})

const isStepActive = (index) => {
  return props.currentStep === index
}

const activeStep = (index) => {
  emit('active-step', index)
}
</script>

<template>
  <div class="w-1/1 mx-auto p-2">
    <div class="stepper-box">
      <div class="steps-wrapper">
        <div v-for="(step, index) in steps" class="step" @click="() => activeStep(index)" :key="index">
          <div class="icon">
            <div class="circle" :class="isStepActive(index) ? 'bg-primary' : 'bg-gray-300'">
              <v-icon :icon="step.icon" color="white" :size="greaterThanMd ? '1.5rem' : '1rem'"></v-icon>
              <div class="divider-line"></div>
            </div>
          </div>
          <div class="step-title">
            <h4 class="md:text-lg text-sm">{{ `Step ${index + 1}` }}</h4>
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
    @apply flex justify-between items-center md: mx-5;

    .step {
      @apply flex flex-col items-center mx-2 cursor-pointer;

      .icon {
        @apply md: p-3 p-1 bg-white;

        .circle {
          @apply p-3 flex justify-center items-center rounded-100rem;
        }
      }

      .step-title {
        @apply text-center;
      }
    }
  }

  .divider-line {
    @apply absolute w-4/5 left-1/10 border-b-#CCC md:border-2 border-1 -z-1;
  }
}
</style>