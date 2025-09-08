<template>
  <div v-if="circle" class="bg-white shadow overflow-hidden sm:rounded-lg">
    <!-- Header -->
    <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
      <div class="flex justify-between items-center">
        <div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            {{ circle.name }}
          </h3>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">
            {{ circle.description }}
          </p>
        </div>
        <div class="flex items-center space-x-3">
          <span :class="{
            'bg-green-100 text-green-800': circle.status === 'active',
            'bg-yellow-100 text-yellow-800': circle.status === 'inactive',
            'bg-gray-100 text-gray-800': circle.status === 'ended'
          }" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
            {{ circle.status }}
          </span>
          <button
            @click="showEditModal = true"
            class="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            <svg class="-ml-1 mr-1.5 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit
          </button>
          <button
            @click="showDeleteModal = true"
            class="inline-flex items-center px-3 py-1.5 border border-red-300 shadow-sm text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50"
          >
            <svg class="-ml-1 mr-1.5 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Circle Details -->
    <div class="px-4 py-5 sm:p-6">
      <dl class="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
        <div>
          <dt class="text-sm font-medium text-gray-500">Circle ID</dt>
          <dd class="mt-1 text-sm text-gray-900">{{ circle.id }}</dd>
        </div>
        <div>
          <dt class="text-sm font-medium text-gray-500">Created</dt>
          <dd class="mt-1 text-sm text-gray-900">{{ formatDate(circle.created_at) }}</dd>
        </div>
        <div>
          <dt class="text-sm font-medium text-gray-500">Jitsi Room ID</dt>
          <dd class="mt-1 text-sm text-gray-900 font-mono text-xs">{{ circle.jitsi_room_id }}</dd>
        </div>
        <div>
          <dt class="text-sm font-medium text-gray-500">Participants</dt>
          <dd class="mt-1 text-sm text-gray-900">{{ participantCount }} active keys</dd>
        </div>
      </dl>
    </div>

    <!-- Participant Keys Management -->
    <div class="border-t border-gray-200">
      <div class="px-4 py-5 sm:p-6">
        <div class="flex justify-between items-center mb-4">
          <h4 class="text-lg font-medium text-gray-900">Participant Access Keys</h4>
          <button
            @click="showGenerateKeyModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
          >
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Generate New Key
          </button>
        </div>

        <div v-if="participantKeys.length === 0" class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v-2H7v-2H4a1 1 0 01-1-1v-4a1 1 0 011-1h3V7a6 6 0 016-6z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No participant keys</h3>
          <p class="mt-1 text-sm text-gray-500">
            Generate access keys for participants to join this circle.
          </p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="key in participantKeys"
            :key="key.key_id"
            class="bg-gray-50 rounded-lg p-4 border border-gray-200"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1 min-w-0">
                <div class="flex items-center space-x-2 mb-2">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ key.role }}
                  </span>
                  <span class="text-xs text-gray-500">
                    ID: {{ key.key_id }}
                  </span>
                </div>
                <div class="mb-2">
                  <label class="block text-xs font-medium text-gray-500 mb-1">Access Key</label>
                  <div class="flex items-center space-x-2">
                    <code class="block text-sm font-mono bg-white px-2 py-1 border border-gray-200 rounded flex-1 truncate">
                      {{ key.access_key }}
                    </code>
                    <button
                      @click="copyToClipboard(key.access_key)"
                      class="inline-flex items-center px-2 py-1 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50"
                    >
                      <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                    </button>
                  </div>
                </div>
                <p class="text-xs text-gray-500">
                  Created {{ formatDate(key.created_at) }}
                </p>
              </div>
              <button
                @click="removeKey(key)"
                class="ml-4 inline-flex items-center px-2 py-1 border border-red-300 shadow-sm text-xs font-medium rounded text-red-700 bg-white hover:bg-red-50"
              >
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Circle Modal -->
    <div v-if="showEditModal" class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75" @click="showEditModal = false"></div>
        </div>
        
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Edit Circle</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Name</label>
                <input
                  v-model="editForm.name"
                  type="text"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                  v-model="editForm.description"
                  rows="3"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Status</label>
                <select
                  v-model="editForm.status"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="inactive">Inactive</option>
                  <option value="active">Active</option>
                  <option value="ended">Ended</option>
                </select>
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
            <button
              @click="saveChanges"
              :disabled="isSaving"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 disabled:opacity-50 sm:col-start-2 sm:text-sm"
            >
              {{ isSaving ? 'Saving...' : 'Save Changes' }}
            </button>
            <button
              @click="showEditModal = false"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:col-start-1 sm:text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75" @click="showDeleteModal = false"></div>
        </div>
        
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div class="sm:flex sm:items-start">
            <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
              <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Delete Circle</h3>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  Are you sure you want to delete "{{ circle?.name }}"? This action cannot be undone and will remove all participant keys and associated data.
                </p>
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
            <button
              @click="confirmDelete"
              :disabled="isDeleting"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 disabled:opacity-50 sm:ml-3 sm:w-auto sm:text-sm"
            >
              {{ isDeleting ? 'Deleting...' : 'Delete Circle' }}
            </button>
            <button
              @click="showDeleteModal = false"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:w-auto sm:text-sm"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Generate Key Modal -->
    <div v-if="showGenerateKeyModal" class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 transition-opacity" aria-hidden="true">
          <div class="absolute inset-0 bg-gray-500 opacity-75" @click="showGenerateKeyModal = false"></div>
        </div>
        
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
          <div>
            <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
              <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v-2H7v-2H4a1 1 0 01-1-1v-4a1 1 0 011-1h3V7a6 6 0 016-6z" />
              </svg>
            </div>
            <div class="mt-3 text-center sm:mt-5">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Generate Participant Key</h3>
              <div class="mt-4 text-left">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Custom Access Key (optional)
                </label>
                <input
                  v-model="generateKeyForm.customKey"
                  type="text"
                  placeholder="Leave empty for auto-generated key"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
                <p class="mt-2 text-xs text-gray-500">
                  Enter your own key (e.g., "student-alice", "workshop-participant-1") or leave empty to auto-generate one.
                </p>
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
            <button
              @click="generateNewKey"
              :disabled="isGenerating"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 disabled:opacity-50 sm:col-start-2 sm:text-sm"
            >
              {{ isGenerating ? 'Generating...' : 'Generate Key' }}
            </button>
            <button
              @click="showGenerateKeyModal = false"
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
import { ref, computed, onMounted } from 'vue'
import { apiService, type CircleDetail, type ParticipantKey } from '@/services/api'

interface Props {
  circleId: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  deleted: []
  updated: [circle: CircleDetail]
}>()

// Reactive state
const circle = ref<CircleDetail | null>(null)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showGenerateKeyModal = ref(false)
const isGenerating = ref(false)
const isSaving = ref(false)
const isDeleting = ref(false)

const editForm = ref({
  name: '',
  description: '',
  status: 'inactive' as 'inactive' | 'active' | 'ended'
})

const generateKeyForm = ref({
  customKey: ''
})

// Computed
const participantKeys = computed(() => 
  circle.value?.participants?.filter(p => p.role === 'participant') || []
)

const participantCount = computed(() => participantKeys.value.length)

// Methods
const loadCircle = async () => {
  try {
    const data = await apiService.getCircle(props.circleId)
    circle.value = data
    
    // Initialize edit form
    editForm.value = {
      name: data.name,
      description: data.description,
      status: data.status as 'inactive' | 'active' | 'ended'
    }
  } catch (error: any) {
    console.error('Failed to load circle:', error)
  }
}

const generateNewKey = async () => {
  if (!circle.value) return
  
  try {
    isGenerating.value = true
    const keyData = generateKeyForm.value.customKey.trim() 
      ? { custom_key: generateKeyForm.value.customKey.trim() }
      : {}
    
    await apiService.generateParticipantKey(circle.value.id, keyData)
    
    // Reset form and close modal
    generateKeyForm.value.customKey = ''
    showGenerateKeyModal.value = false
    
    await loadCircle() // Refresh to show new key
  } catch (error: any) {
    console.error('Failed to generate key:', error)
    alert('Failed to generate new participant key: ' + (error.response?.data?.error || error.message))
  } finally {
    isGenerating.value = false
  }
}

const removeKey = async (key: ParticipantKey) => {
  if (!circle.value) return
  
  if (!confirm(`Are you sure you want to remove this participant key?`)) {
    return
  }
  
  try {
    await apiService.removeParticipantKey(circle.value.id, key.key_id)
    await loadCircle() // Refresh to remove key from list
  } catch (error: any) {
    console.error('Failed to remove key:', error)
    alert('Failed to remove participant key')
  }
}

const saveChanges = async () => {
  if (!circle.value) return
  
  try {
    isSaving.value = true
    const updated = await apiService.updateCircle(circle.value.id, editForm.value)
    circle.value = { ...circle.value, ...updated }
    showEditModal.value = false
    emit('updated', circle.value)
  } catch (error: any) {
    console.error('Failed to update circle:', error)
    alert('Failed to update circle')
  } finally {
    isSaving.value = false
  }
}

const confirmDelete = async () => {
  if (!circle.value) return
  
  try {
    isDeleting.value = true
    await apiService.deleteCircle(circle.value.id)
    showDeleteModal.value = false
    emit('deleted')
  } catch (error: any) {
    console.error('Failed to delete circle:', error)
    alert('Failed to delete circle')
  } finally {
    isDeleting.value = false
  }
}

const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text)
    // Could add a toast notification here
  } catch (error) {
    console.error('Failed to copy to clipboard:', error)
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Lifecycle
onMounted(() => {
  loadCircle()
})
</script>