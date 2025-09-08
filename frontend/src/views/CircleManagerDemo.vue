<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <router-link 
                to="/"
                class="mr-4 p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
              >
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </router-link>
              <div>
                <h1 class="text-2xl font-bold text-gray-900">Circle Management Demo</h1>
                <p class="text-sm text-gray-500 mt-1">Complete circle lifecycle management with participant key controls</p>
              </div>
            </div>
            <button
              @click="showCreateModal = true"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
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

    <!-- Main content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="space-y-6">
        <!-- Circles List -->
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Your Circles</h3>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">
              Manage circles, participant keys, and access controls
            </p>
          </div>
          
          <div v-if="isLoadingCircles" class="p-6 text-center">
            <div class="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
            <span class="ml-2 text-sm text-gray-500">Loading circles...</span>
          </div>
          
          <div v-else-if="circles.length === 0" class="p-6 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No circles yet</h3>
            <p class="mt-1 text-sm text-gray-500">Get started by creating your first inquiry circle.</p>
            <div class="mt-6">
              <button
                @click="showCreateModal = true"
                class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Create Circle
              </button>
            </div>
          </div>
          
          <div v-else class="divide-y divide-gray-200">
            <div
              v-for="circle in circles"
              :key="circle.id"
              class="p-6 hover:bg-gray-50 cursor-pointer"
              @click="selectCircle(circle.id)"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center space-x-3">
                    <h4 class="text-lg font-medium text-gray-900">{{ circle.name }}</h4>
                    <span :class="{
                      'bg-green-100 text-green-800': circle.status === 'active',
                      'bg-yellow-100 text-yellow-800': circle.status === 'inactive',
                      'bg-gray-100 text-gray-800': circle.status === 'ended'
                    }" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ circle.status }}
                    </span>
                  </div>
                  <p class="mt-1 text-sm text-gray-500">{{ circle.description }}</p>
                  <div class="mt-2 flex items-center text-sm text-gray-500 space-x-6">
                    <div class="flex items-center">
                      <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                      </svg>
                      ID: {{ circle.id }}
                    </div>
                    <div class="flex items-center">
                      <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {{ formatDate(circle.created_at) }}
                    </div>
                    <div class="flex items-center">
                      <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v-2H7v-2H4a1 1 0 01-1-1v-4a1 1 0 011-1h3V7a6 6 0 016-6z" />
                      </svg>
                      Room: {{ circle.jitsi_room_id }}
                    </div>
                  </div>
                </div>
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Debug Info -->
        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
          <h4 class="text-sm font-medium text-yellow-800">Debug Info</h4>
          <p class="text-xs text-yellow-700 mt-1">
            Selected Circle ID: {{ selectedCircleId || 'None' }} | 
            Circles Count: {{ circles.length }} |
            Auth Key: {{ apiService.getAccessKey() || 'Not authenticated' }}
          </p>
        </div>

        <!-- Selected Circle Management -->
        <div v-if="selectedCircleId">
          <CircleManagement 
            :circleId="selectedCircleId" 
            @deleted="onCircleDeleted"
            @updated="onCircleUpdated"
          />
        </div>
      </div>
    </div>

    <!-- Create Circle Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75" @click="showCreateModal = false"></div>
        </div>
        
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Create New Circle</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Circle Name *</label>
                <input
                  v-model="createForm.name"
                  type="text"
                  placeholder="e.g., Morning Inquiry Circle"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                  v-model="createForm.description"
                  rows="3"
                  placeholder="Describe the purpose or focus of this circle..."
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                ></textarea>
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
            <button
              @click="createCircle"
              :disabled="isCreating || !createForm.name.trim()"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 disabled:opacity-50 sm:col-start-2 sm:text-sm"
            >
              {{ isCreating ? 'Creating...' : 'Create Circle' }}
            </button>
            <button
              @click="showCreateModal = false"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:col-start-1 sm:text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService, type Circle, type CircleDetail } from '@/services/api'
import CircleManagement from '@/components/circles/CircleManagement.vue'

// Reactive state
const circles = ref<Circle[]>([])
const selectedCircleId = ref<number | null>(null)
const isLoadingCircles = ref(false)
const showCreateModal = ref(false)
const isCreating = ref(false)

const createForm = ref({
  name: '',
  description: ''
})

// Methods
const loadCircles = async () => {
  try {
    isLoadingCircles.value = true
    const response = await apiService.getCircles()
    circles.value = response.circles
  } catch (error: any) {
    console.error('Failed to load circles:', error)
  } finally {
    isLoadingCircles.value = false
  }
}

const selectCircle = (circleId: number) => {
  console.log('Selecting circle:', circleId, 'Current selected:', selectedCircleId.value)
  selectedCircleId.value = selectedCircleId.value === circleId ? null : circleId
  console.log('New selected circle ID:', selectedCircleId.value)
}

const createCircle = async () => {
  if (!createForm.value.name.trim()) return
  
  try {
    isCreating.value = true
    const newCircle = await apiService.createCircle(createForm.value)
    circles.value.push(newCircle)
    
    // Clear form and close modal
    createForm.value = { name: '', description: '' }
    showCreateModal.value = false
    
    // Auto-select the new circle
    selectedCircleId.value = newCircle.id
  } catch (error: any) {
    console.error('Failed to create circle:', error)
    alert('Failed to create circle')
  } finally {
    isCreating.value = false
  }
}

const onCircleDeleted = () => {
  selectedCircleId.value = null
  loadCircles() // Refresh the list
}

const onCircleUpdated = (updatedCircle: CircleDetail) => {
  // Update the circle in the list
  const index = circles.value.findIndex(c => c.id === updatedCircle.id)
  if (index !== -1) {
    circles.value[index] = { ...circles.value[index], ...updatedCircle }
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// Lifecycle
onMounted(() => {
  loadCircles()
})
</script>