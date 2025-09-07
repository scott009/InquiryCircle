<template>
  <div class="dashboard p-6">
    <h2 class="text-2xl font-bold text-gray-900 mb-4">Welcome to InquiryCircle</h2>
    <p class="text-gray-600 mb-6">Vue 3 + TypeScript + Tailwind CSS application is working!</p>
    
    <div class="space-y-4">
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 class="text-lg font-semibold text-blue-900 mb-2">Test Jitsi Integration</h3>
        <p class="text-blue-700 mb-3">Test the video conferencing functionality</p>
        <router-link 
          to="/test-jitsi" 
          class="inline-block bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Launch Video Conference Test
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Dashboard component - main landing page
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}
</style>