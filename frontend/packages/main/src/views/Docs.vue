<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();

router.go(-1);
location.href = "http://36.111.128.21:30006/";
</script>

<template>
  <div></div>
</template>
