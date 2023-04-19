<script setup>
import { ref } from 'vue'

const dialog = ref(true)
</script>

<template>
  <v-dialog v-model="dialog" persistent class="max-w-600px w-1/1">
    <v-card class="p-2">
      <v-card-title class="my-4 text-center">
        <svg class="m-auto w-1/3" version="1.1" id="L1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 100 100"
          enable-background="new 0 0 100 100" xml:space="preserve">
          <circle fill="none" stroke-width="6" stroke-miterlimit="15" stroke-dasharray="14.2472,14.2472" cx="50" cy="50"
            r="47" style="stroke: rgb(var(--v-theme-primary))">
            <animateTransform attributeName="transform" attributeType="XML" type="rotate" dur="5s" from="0 50 50"
              to="360 50 50" repeatCount="indefinite" />
          </circle>
          <circle fill="none" stroke-width="1" stroke-miterlimit="10" stroke-dasharray="10,10" cx="50" cy="50" r="39"
            style="stroke: rgb(var(--v-theme-primary))">
            <animateTransform attributeName="transform" attributeType="XML" type="rotate" dur="5s" from="0 50 50"
              to="-360 50 50" repeatCount="indefinite" />
          </circle>
          <g style="fill: rgb(var(--v-theme-primary))">
            <rect x="30" y="35" width="5" height="30">
              <animateTransform attributeName="transform" dur="1s" type="translate" values="0 5 ; 0 -5; 0 5"
                repeatCount="indefinite" begin="0.1" />
            </rect>
            <rect x="40" y="35" width="5" height="30">
              <animateTransform attributeName="transform" dur="1s" type="translate" values="0 5 ; 0 -5; 0 5"
                repeatCount="indefinite" begin="0.2" />
            </rect>
            <rect x="50" y="35" width="5" height="30">
              <animateTransform attributeName="transform" dur="1s" type="translate" values="0 5 ; 0 -5; 0 5"
                repeatCount="indefinite" begin="0.3" />
            </rect>
            <rect x="60" y="35" width="5" height="30">
              <animateTransform attributeName="transform" dur="1s" type="translate" values="0 5 ; 0 -5; 0 5"
                repeatCount="indefinite" begin="0.4" />
            </rect>
            <rect x="70" y="35" width="5" height="30">
              <animateTransform attributeName="transform" dur="1s" type="translate" values="0 5 ; 0 -5; 0 5"
                repeatCount="indefinite" begin="0.5" />
            </rect>
          </g>
        </svg>
      </v-card-title>
    </v-card>
  </v-dialog>
</template>