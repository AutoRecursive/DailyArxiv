<template>
  <TheHeader />
  <router-view />
</template>

<script setup>
import TheHeader from './components/TheHeader.vue';
</script>

<style lang="scss">
@use './assets/styles/main';
</style>
