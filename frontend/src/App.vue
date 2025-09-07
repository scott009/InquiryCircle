<template>
  <div id="app">
    <AppHeader />
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import AppHeader from './components/layout/AppHeader.vue'
// InquiryCircle Vue 3 Application
// Main application component with Vue Router and navigation
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
