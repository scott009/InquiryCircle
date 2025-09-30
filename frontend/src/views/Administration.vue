<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center">
                <span class="text-sm font-medium text-white">IC</span>
              </div>
            </div>
            <div class="ml-4">
              <h1 class="text-lg font-medium text-gray-900">Administration</h1>
              <p class="text-sm text-gray-500">Manage your inquiry circles</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-500">{{ authStore.accessKey }}</span>
            <button
              @click="logout"
              class="text-gray-400 hover:text-gray-500"
            >
              <span class="sr-only">Sign out</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Quick actions -->
      <div class="mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
              Quick Actions
            </h3>
            <div class="flex flex-col sm:flex-row gap-4">
              <button
                @click="showCreateCircleModal = true"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Create New Circle
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Circles list -->
      <div class="bg-white shadow overflow-hidden sm:rounded-md">
        <div class="px-4 py-5 sm:px-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Your Circles
          </h3>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">
            Manage and facilitate your inquiry circles
          </p>
        </div>

        <!-- Loading state -->
        <div v-if="isLoading" class="px-4 py-5 sm:p-6">
          <div class="flex justify-center">
            <svg class="animate-spin h-6 w-6 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        </div>

        <!-- Circles list -->
        <ul v-else-if="circles.length > 0" class="divide-y divide-gray-200">
          <li v-for="circle in circles" :key="circle.id" class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                    <svg class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">{{ circle.name }}</div>
                  <div class="text-sm text-gray-500">{{ circle.description || 'No description' }}</div>
                  <div class="text-xs text-gray-400 mt-1">
                    Created {{ formatDate(circle.created_at) }} •
                    <span :class="{
                      'text-green-600': circle.status === 'active',
                      'text-yellow-600': circle.status === 'inactive',
                      'text-gray-600': circle.status === 'ended'
                    }">
                      {{ circle.status.charAt(0).toUpperCase() + circle.status.slice(1) }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <button
                  @click="openCircle(circle)"
                  class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  Open
                </button>
                <button
                  @click="joinCircle(circle)"
                  :class="{
                    'bg-green-600 hover:bg-green-700 text-white': circle.status === 'active',
                    'bg-gray-300 text-gray-500 cursor-not-allowed': circle.status !== 'active'
                  }"
                  class="inline-flex items-center px-3 py-2 border border-transparent shadow-sm text-sm leading-4 font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  :disabled="circle.status !== 'active'"
                >
                  {{ circle.status === 'active' ? 'Join' : 'Inactive' }}
                </button>
              </div>
            </div>
          </li>
        </ul>

        <!-- Empty state -->
        <div v-else class="px-4 py-5 sm:p-6 text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No circles</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by creating a new inquiry circle.</p>
          <div class="mt-6">
            <button
              @click="showCreateCircleModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create Circle
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Circle Modal -->
    <CreateCircleModal
      v-if="showCreateCircleModal"
      @close="showCreateCircleModal = false"
      @created="handleCircleCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { apiService, type Circle } from '@/services/api'
import CreateCircleModal from '../components/dashboard/CreateCircleModal.vue'

const router = useRouter()
const authStore = useAuthStore()

const circles = ref<Circle[]>([])
const isLoading = ref(true)
const showCreateCircleModal = ref(false)

const loadCircles = async () => {
  isLoading.value = true
  try {
    const response = await apiService.getCircles()
    circles.value = response.circles
  } catch (error) {
    console.error('Failed to load circles:', error)
  } finally {
    isLoading.value = false
  }
}

const handleCircleCreated = (newCircle: Circle) => {
  circles.value.unshift(newCircle)
  showCreateCircleModal.value = false
}

const openCircle = (circle: Circle) => {
  router.push(`/circle/${circle.id}`)
}

const joinCircle = (circle: Circle) => {
  if (circle.status === 'active') {
    router.push(`/circle/${circle.id}`)
  }
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadCircles()
})
</script>
