<template>
  <div id="app">
    <TopBar1 />
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import TopBar1 from './components/layout/TopBar1.vue'
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
