<script setup lang="ts">
interface Props {
  user?: string;
  host?: string;
}

withDefaults(defineProps<Props>(), {
  user: "beimingwu",
  host: "localhost",
});

const date = new Date().toString();
const time = new Date().toLocaleTimeString();
</script>

<template>
  <div class="p-1 font-mono text-xs text-white md:text-base">
    <slot name="header">
      <div>Last login: {{ date }}</div>
      <br />
      <div>
        <b class="text-purple-800">#&nbsp;</b>
        <b class="text-indigo-500">{{ user }}&nbsp;</b>
        <span>@&nbsp;</span>
        <span class="text-green-500">{{ host }}&nbsp;</span>
        <span>in&nbsp;</span>
        <b class="text-yellow-500">~&nbsp;</b>
        <span>[{{ time }}]</span>
      </div>
    </slot>
    <slot />
  </div>
</template>
