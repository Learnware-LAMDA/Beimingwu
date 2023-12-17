<script setup lang="ts">
import collaborationImg from "../assets/images/public/collaboration.svg?url";
</script>

<template>
  <div class="flex h-full">
    <div
      class="hidden h-full flex-1 md:block"
      :style="{
        background: `url(${collaborationImg})`,
        backgroundSize: 'contain',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center center',
      }"
    />
    <div
      class="fill-height md:text-md flex flex-1 flex-row items-center justify-center p-2 text-xs sm:text-sm"
    >
      <v-card
        flat
        class="mx-auto w-full max-w-[500px]"
      >
        <div class="rounded border p-2 sm:p-6">
          <slot />
        </div>
      </v-card>
    </div>
  </div>
</template>
