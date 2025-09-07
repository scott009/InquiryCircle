<template>
  <header class="bg-white shadow-sm border-b">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <router-link to="/" class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <svg class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-3">
              <h1 class="text-xl font-semibold text-gray-900">InquiryCircle</h1>
            </div>
          </router-link>
        </div>

        <div class="flex items-center space-x-4">
          <!-- Auth Status -->
          <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
            <!-- User Info -->
            <div class="text-sm text-gray-600">
              <span class="font-medium">{{ authStore.userRole === 'facilitator' ? 'Facilitator' : 'Participant' }}</span>
              <span v-if="authStore.accessKey" class="ml-2 text-xs text-gray-400">
                Key: {{ authStore.accessKey.substring(0, 8) }}...
              </span>
            </div>

            <!-- Navigation Links -->
            <nav class="flex space-x-2">
              <router-link 
                v-if="authStore.isFacilitator"
                to="/dashboard"
                class="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                active-class="text-blue-600 bg-blue-50"
              >
                Dashboard
              </router-link>
              <router-link 
                to="/circles"
                class="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                active-class="text-blue-600 bg-blue-50"
              >
                Circles
              </router-link>
            </nav>

            <!-- Logout Button -->
            <button
              @click="handleLogout"
              class="px-3 py-2 rounded-md text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 border border-red-200"
            >
              Logout
            </button>
          </div>

          <!-- Login Link -->
          <div v-else>
            <router-link 
              to="/login"
              class="px-4 py-2 rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              Login
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>