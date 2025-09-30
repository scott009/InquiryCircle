<template>
  <div class="dashboard p-6">
    <h2 class="text-2xl font-bold text-gray-900 mb-4">Welcome to InquiryCircle</h2>
    <p class="text-gray-600 mb-6">Vue 3 + TypeScript + Tailwind CSS application is working!</p>

    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <div class="lg:col-span-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-4 text-white mb-4">
        <h3 class="text-lg font-semibold mb-2">🎉 Complete Circle Management System!</h3>
        <p class="text-blue-100 mb-3">Create circles, manage participant keys, delete circles, and test video conferencing</p>
        <div class="flex flex-col sm:flex-row gap-3">
          <router-link
            to="/circle-manager-demo"
            class="inline-block bg-white text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors"
          >
            Full Circle Management Demo
          </router-link>
          <router-link
            to="/meeting"
            class="inline-block bg-blue-100 text-blue-700 px-4 py-2 rounded-lg font-medium hover:bg-blue-200 transition-colors"
          >
            Meeting
          </router-link>
          <router-link
            to="/tests"
            class="inline-block bg-blue-100 text-blue-700 px-4 py-2 rounded-lg font-medium hover:bg-blue-200 transition-colors"
          >
            System Health Checks
          </router-link>
        </div>
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