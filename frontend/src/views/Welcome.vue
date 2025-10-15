<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4">
    <div class="max-w-2xl w-full">
      <!-- DisplayText1 Component -->
      <DisplayText1 />

      <!-- Welcome Header -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center h-16 w-16 rounded-full bg-blue-600 text-white mb-4">
          <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <h1 class="text-4xl font-bold text-gray-900 mb-2">
          Welcome to InquiryCircle
        </h1>
        <p class="text-lg text-gray-600">
          Hello, {{ authStore.userRole }}!
        </p>
      </div>

      <!-- Participant View -->
      <div v-if="authStore.isParticipant" class="bg-white rounded-lg shadow-lg p-8">
        <div class="text-center">
          <h2 class="text-2xl font-semibold text-gray-900 mb-6">
            Ready to join your meeting?
          </h2>

          <div v-if="authStore.userCircle" class="mb-8">
            <p class="text-gray-600 mb-2">Your circle:</p>
            <p class="text-xl font-medium text-blue-600">{{ authStore.userCircle.name }}</p>
          </div>

          <router-link
            to="/meeting"
            class="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            Go to Your Meeting
            <svg class="ml-2 -mr-1 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Facilitator View -->
      <div v-if="authStore.isFacilitator" class="bg-white rounded-lg shadow-lg p-8">
        <div class="text-center">
          <h2 class="text-2xl font-semibold text-gray-900 mb-6">
            Facilitator Dashboard
          </h2>

          <div v-if="authStore.userCircle" class="mb-8">
            <p class="text-gray-600 mb-2">Your circle:</p>
            <p class="text-xl font-medium text-blue-600">{{ authStore.userCircle.name }}</p>
          </div>

          <div class="space-y-4">
            <!-- Facilitator Home Page Link -->
            <router-link
              to="/facpanel"
              class="block w-full px-8 py-4 border border-transparent text-lg font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
            >
              <span class="text-xl font-semibold">Facilitator's Home Page</span>
              <svg class="inline-block ml-2 w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </router-link>

            <!-- Additional Quick Links -->
            <div class="pt-4 border-t border-gray-200">
              <p class="text-sm text-gray-600 mb-3">Quick Links:</p>
              <div class="grid grid-cols-2 gap-3">
                <router-link
                  to="/facmeet"
                  class="px-4 py-3 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                >
                  Join Meeting
                </router-link>
                <router-link
                  to="/administration"
                  class="px-4 py-3 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                >
                  Administration
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Logout Link -->
      <div class="text-center mt-6">
        <button
          @click="handleLogout"
          class="text-sm text-gray-600 hover:text-gray-900"
        >
          Logout
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import DisplayText1 from '@/components/layout/DisplayText1.vue'

const router = useRouter()
const authStore = useAuthStore()

// Redirect to login if not authenticated
onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/')
  }
})

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>
