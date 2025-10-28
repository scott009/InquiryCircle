<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4">
    <div class="max-w-2xl w-full">
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
        <p class="text-lg text-gray-600 mb-4">
          Hello, {{ authStore.userRole }}!
        </p>

        <!-- DisplayText1 Component - wider, no border, matches background -->
        <div class="max-w-6xl mx-auto mb-4">
          <DisplayText1 class="bg-gray-50" />
          <hr class="border-gray-300 mt-4" />
        </div>
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
        <div>
          <h2 class="text-2xl font-semibold text-gray-900 mb-6">
            Your Circles
          </h2>

          <!-- Loading State -->
          <div v-if="isLoadingCircles" class="text-center py-8">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p class="mt-2 text-gray-600">Loading circles...</p>
          </div>

          <!-- Error State -->
          <div v-if="circlesError" class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <p class="text-red-800">{{ circlesError }}</p>
          </div>

          <!-- Circles List - Two Column Grid -->
          <div v-if="!isLoadingCircles && circles.length > 0" class="grid grid-cols-2 gap-4 mb-6">
            <div
              v-for="circle in circles"
              :key="circle.id"
              class="border border-gray-200 rounded-lg p-5 hover:border-blue-300 hover:shadow-md transition-all flex flex-col"
            >
              <div class="flex items-start justify-between mb-3">
                <div class="flex-1">
                  <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ circle.name }}</h3>
                  <router-link
                    :to="`/facpanel?circle=${circle.id}`"
                    class="text-base text-blue-600 hover:text-blue-800 font-medium"
                  >
                    Configure Circle
                  </router-link>
                  <div class="h-12 mt-2">
                    <p v-if="circle.description" class="text-sm text-gray-600 line-clamp-2">
                      {{ circle.description }}
                    </p>
                  </div>
                </div>
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="{
                    'bg-green-100 text-green-800': circle.status === 'active',
                    'bg-gray-100 text-gray-800': circle.status === 'inactive',
                    'bg-red-100 text-red-800': circle.status === 'ended'
                  }"
                >
                  {{ circle.status }}
                </span>
              </div>

              <!-- Circle Action Button -->
              <router-link
                :to="`/facmeet?circle=${circle.id}`"
                class="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors mt-auto"
              >
                Join the Circle
                <svg class="ml-2 -mr-0.5 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </router-link>
            </div>
          </div>

          <!-- No Circles State -->
          <div v-if="!isLoadingCircles && circles.length === 0" class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <p class="mt-4 text-gray-600">You haven't created any circles yet.</p>
            <p class="text-sm text-gray-500 mt-1">Create your first circle to get started!</p>
          </div>

          <!-- Create New Circle Button -->
          <button
            @click="showCreateCircleModal = true"
            class="w-full flex items-center justify-center px-6 py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-blue-400 hover:text-blue-600 transition-colors"
          >
            <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Create New Circle
          </button>
        </div>
      </div>

      <!-- Create Circle Modal -->
      <div
        v-if="showCreateCircleModal"
        class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
        @click.self="showCreateCircleModal = false"
      >
        <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
          <div class="mt-3">
            <h3 class="text-lg font-medium leading-6 text-gray-900 mb-4">
              Create New Circle
            </h3>

            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Circle Name *
                </label>
                <input
                  v-model="newCircleName"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter circle name"
                  @keyup.enter="createCircle"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Description (optional)
                </label>
                <textarea
                  v-model="newCircleDescription"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter circle description"
                ></textarea>
              </div>

              <div v-if="createCircleError" class="bg-red-50 border border-red-200 rounded-md p-3">
                <p class="text-sm text-red-800">{{ createCircleError }}</p>
              </div>
            </div>

            <div class="flex gap-3 mt-6">
              <button
                @click="showCreateCircleModal = false"
                class="flex-1 px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-200 transition-colors"
              >
                Cancel
              </button>
              <button
                @click="createCircle"
                :disabled="!newCircleName.trim() || isCreatingCircle"
                class="flex-1 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {{ isCreatingCircle ? 'Creating...' : 'Create Circle' }}
              </button>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { apiService, type Circle } from '@/services/api'
import DisplayText1 from '@/components/layout/DisplayText1.vue'

const router = useRouter()
const authStore = useAuthStore()

// Circles state
const circles = ref<Circle[]>([])
const isLoadingCircles = ref(false)
const circlesError = ref<string | null>(null)

// Create circle modal state
const showCreateCircleModal = ref(false)
const newCircleName = ref('')
const newCircleDescription = ref('')
const isCreatingCircle = ref(false)
const createCircleError = ref<string | null>(null)

// Load facilitator's circles
const loadCircles = async () => {
  if (!authStore.isFacilitator) return

  isLoadingCircles.value = true
  circlesError.value = null

  try {
    const response = await apiService.getCircles()
    circles.value = response.circles
  } catch (error: any) {
    circlesError.value = apiService.getErrorMessage(error)
    console.error('Failed to load circles:', error)
  } finally {
    isLoadingCircles.value = false
  }
}

// Create new circle
const createCircle = async () => {
  if (!newCircleName.value.trim()) return

  isCreatingCircle.value = true
  createCircleError.value = null

  try {
    const newCircle = await apiService.createCircle({
      name: newCircleName.value.trim(),
      description: newCircleDescription.value.trim()
    })

    // Add to circles list
    circles.value.unshift(newCircle)

    // Close modal and reset form
    showCreateCircleModal.value = false
    newCircleName.value = ''
    newCircleDescription.value = ''
  } catch (error: any) {
    createCircleError.value = apiService.getErrorMessage(error)
    console.error('Failed to create circle:', error)
  } finally {
    isCreatingCircle.value = false
  }
}

// Redirect to login if not authenticated
onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/')
  } else if (authStore.isFacilitator) {
    loadCircles()
  }
})

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>
