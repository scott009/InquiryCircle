<template>
  <div class="dashboard p-6">
    <h2 class="text-2xl font-bold text-gray-900 mb-4">Welcome to InquiryCircle</h2>
    <p class="text-gray-600 mb-6">Vue 3 + TypeScript + Tailwind CSS application is working!</p>
    
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
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
      
      <div class="bg-green-50 border border-green-200 rounded-lg p-4">
        <h3 class="text-lg font-semibold text-green-900 mb-2">Test API Client</h3>
        <p class="text-green-700 mb-3">Test the API client connection to Django backend</p>
        <router-link 
          to="/test-api" 
          class="inline-block bg-green-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors"
        >
          Launch API Test
        </router-link>
      </div>

      <div class="bg-purple-50 border border-purple-200 rounded-lg p-4">
        <h3 class="text-lg font-semibold text-purple-900 mb-2">Authentication</h3>
        <p class="text-purple-700 mb-3">Test the key-based authentication system</p>
        <router-link 
          to="/login" 
          class="inline-block bg-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-700 transition-colors"
        >
          Test Login Form
        </router-link>
      </div>

      <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
        <h3 class="text-lg font-semibold text-indigo-900 mb-2">Circle Management</h3>
        <p class="text-indigo-700 mb-3">Test circle creation and management UI</p>
        <router-link 
          to="/circles" 
          class="inline-block bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
        >
          View Circles Interface
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