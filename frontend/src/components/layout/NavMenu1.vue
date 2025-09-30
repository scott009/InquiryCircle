<template>
  <nav class="flex items-center space-x-1">
    <router-link
      to="/"
      class="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50"
      active-class="text-blue-600 bg-blue-50"
    >
      Home
    </router-link>

    <router-link
      to="/meeting"
      class="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50"
      active-class="text-blue-600 bg-blue-50"
    >
      Meeting
    </router-link>

    <router-link
      v-if="authStore.isFacilitator"
      to="/facmeet"
      class="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50"
      active-class="text-blue-600 bg-blue-50"
    >
      Fac Meeting
    </router-link>

    <router-link
      v-if="authStore.isFacilitator"
      to="/facpanel"
      class="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50"
      active-class="text-blue-600 bg-blue-50"
    >
      Fac Panel
    </router-link>

    <router-link
      to="/administration"
      class="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50"
      active-class="text-blue-600 bg-blue-50"
    >
      Administration
    </router-link>

    <router-link
      to="/tests"
      class="px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50"
      active-class="text-blue-600 bg-blue-50"
    >
      Tests
    </router-link>

    <!-- User Info & Logout -->
    <div v-if="authStore.isAuthenticated" class="flex items-center space-x-2 ml-4 pl-4 border-l border-gray-200">
      <div class="text-xs text-gray-500">
        <span class="font-medium">{{ authStore.userRole === 'facilitator' ? 'Facilitator' : 'Participant' }}</span>
        <span v-if="authStore.accessKey" class="ml-1">
          ({{ authStore.accessKey.substring(0, 8) }}...)
        </span>
      </div>

      <button
        @click="handleLogout"
        class="px-2 py-1 rounded-md text-xs font-medium text-red-600 hover:text-red-700 hover:bg-red-50 border border-red-200"
      >
        Logout
      </button>
    </div>

    <!-- Login Link -->
    <router-link
      v-else
      to="/login"
      class="ml-4 pl-4 border-l border-gray-200 px-3 py-2 rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
    >
      Login
    </router-link>
  </nav>
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
