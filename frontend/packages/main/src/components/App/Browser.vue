<script setup lang="ts">
import LogoNoText from "../../../public/logo-no-text.svg?component";
import Logo from "../../../public/logo.svg?component";
</script>

<template>
  <div class="flex flex-col overflow-hidden rounded-md">
    <div class="flex h-6 items-center justify-between bg-gray-900">
      <div class="flex">
        <div class="ml-2" />
        <div
          v-for="i in 3"
          :key="i"
          class="my-2 ml-1.5 h-2 w-2 rounded-full bg-gray-800"
        />
        <svg
          class="ml-2 mt-1 h-5"
          viewBox="-1 -1 72 11"
        >
          <defs>
            <g id="cross">
              <path
                d="M 0,0 2,2 M 2,0 0,2"
                stroke="white"
                stroke-width="0.3"
                stroke-linecap="round"
              />
            </g>
          </defs>
          <path
            d="M0 10 a2 2 0 0 0 2 -2 v-6 a2 2 0 0 1 2 -2 h60 a2 2 0 0 1 2 2 v6 a2 2 0 0 0 2 2"
            class="fill-gray-700"
          />
          <logo-no-text
            x="5"
            y="2"
            height="6"
            width="6"
          />
          <text
            x="14"
            y="5"
            text-anchor="start"
            dominant-baseline="middle"
            font-size="4"
            fill="white"
          >
            Beimingwu
          </text>
          <use
            href="#cross"
            x="60"
            y="4"
          />
        </svg>
        <svg
          class="mr-2 mt-1 w-1.5"
          viewBox="0 0 10 10"
        >
          <path
            d="M 0 5 10 5 M5 0 5 10"
            stroke="white"
            stroke-width="1"
          />
        </svg>
      </div>
      <svg
        class="m-1 mr-2 w-1"
        viewBox="0 0 10 10"
      >
        <path
          d="M 1,3 5,9 9,3"
          stroke="white"
          stroke-width="1"
          fill="none"
        />
      </svg>
    </div>

    <div class="flex h-6 items-center bg-gray-700">
      <div class="text-[0.4rem]">
        <v-icon class="ml-1 p-2"> mdi-arrow-left </v-icon>
        <v-icon class="p-2"> mdi-arrow-right </v-icon>
        <v-icon class="p-2"> mdi-reload </v-icon>
        <v-icon class="p-2"> mdi-home-outline </v-icon>
      </div>
      <div
        class="flex h-3.5 flex-1 flex-col justify-center rounded-full bg-gray-600 px-1.5 text-left text-[0.3rem]"
      >
        <div class="flex h-full items-center">
          <v-icon>mdi-lock</v-icon>
          <span class="mx-1 text-[0.4rem]"> bmwu.cloud </span>
        </div>
      </div>
      <div class="text-[0.4rem]">
        <v-icon class="p-2"> mdi-magnify </v-icon>
        <v-icon class="p-2"> mdi-dots-horizontal </v-icon>
      </div>
    </div>

    <div class="flex items-center justify-between border-b border-gray-300 bg-white">
      <div class="p-2">
        <logo class="w-20" />
      </div>
    </div>

    <slot />
  </div>
</template>
