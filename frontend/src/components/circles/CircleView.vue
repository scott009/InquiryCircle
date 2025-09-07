<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center">
            <button
              @click="goBack"
              class="mr-4 p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <div class="flex-1">
              <h1 class="text-2xl font-bold text-gray-900">{{ circle?.name || 'Loading...' }}</h1>
              <p class="text-sm text-gray-500 mt-1">{{ circle?.description || 'No description' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Video Conference Area -->
        <div class="lg:col-span-2">
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                Video Conference
              </h3>
              
              <!-- Placeholder for Jitsi integration -->
              <div class="bg-gray-100 rounded-lg h-96 flex items-center justify-center">
                <div class="text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  <h3 class="mt-2 text-sm font-medium text-gray-900">Video Conference</h3>
                  <p class="mt-1 text-sm text-gray-500">
                    Jitsi Meet integration will be available here
                  </p>
                  <div class="mt-6">
                    <button
                      @click="joinVideoCall"
                      class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                      Join Video Call
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="lg:col-span-1">
          <!-- Circle Information -->
          <div class="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                Circle Information
              </h3>
              <dl class="grid grid-cols-1 gap-x-4 gap-y-4 sm:grid-cols-1">
                <div>
                  <dt class="text-sm font-medium text-gray-500">Status</dt>
                  <dd class="mt-1 text-sm text-gray-900">
                    <span :class="{
                      'text-green-600': circle?.status === 'active',
                      'text-yellow-600': circle?.status === 'inactive',
                      'text-gray-600': circle?.status === 'ended'
                    }">
                      {{ circle?.status?.charAt(0).toUpperCase() + circle?.status?.slice(1) }}
                    </span>
                  </dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Created</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ formatDate(circle?.created_at) }}</dd>
                </div>
                <div v-if="participants.length > 0">
                  <dt class="text-sm font-medium text-gray-500">Participants</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ participants.length }} participants</dd>
                </div>
              </dl>
            </div>
          </div>

          <!-- Messages Panel -->
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                Messages
              </h3>
              
              <!-- Messages List -->
              <div class="space-y-4 max-h-64 overflow-y-auto mb-4">
                <div v-if="messages.length === 0" class="text-center text-gray-500 py-4">
                  No messages yet
                </div>
                <div v-for="message in messages" :key="message.id" class="border-b border-gray-200 pb-2">
                  <div class="text-sm font-medium text-gray-900">{{ message.sender_role }}</div>
                  <div class="text-sm text-gray-600 mt-1">{{ message.content }}</div>
                  <div class="text-xs text-gray-400 mt-1">{{ formatDate(message.timestamp) }}</div>
                </div>
              </div>

              <!-- Message Input (only for facilitators) -->
              <div v-if="authStore.isFacilitator" class="mt-4">
                <div class="flex space-x-2">
                  <input
                    v-model="newMessage"
                    type="text"
                    placeholder="Type a message..."
                    class="flex-1 min-w-0 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    @keypress.enter="sendMessage"
                  >
                  <button
                    @click="sendMessage"
                    :disabled="!newMessage.trim()"
                    class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { apiService, type Circle, type Message } from '@/services/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const circle = ref<Circle | null>(null)
const messages = ref<Message[]>([])
const participants = ref<any[]>([])
const newMessage = ref('')
const isLoading = ref(true)

let messagePolling: number | null = null

const loadCircle = async () => {
  try {
    const circleId = route.params.id as string
    const response = await apiService.getCircles()
    circle.value = response.circles.find(c => c.id.toString() === circleId) || null
    
    if (!circle.value) {
      router.push('/circles')
      return
    }

    // Load messages
    await loadMessages()
    
    // Start polling for new messages
    startMessagePolling()
  } catch (error) {
    console.error('Failed to load circle:', error)
    router.push('/circles')
  } finally {
    isLoading.value = false
  }
}

const loadMessages = async () => {
  if (!circle.value) return
  
  try {
    const response = await apiService.getMessages(circle.value.id)
    messages.value = response.messages
  } catch (error) {
    console.error('Failed to load messages:', error)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || !circle.value) return

  try {
    await apiService.sendMessage(circle.value.id, newMessage.value.trim())
    newMessage.value = ''
    await loadMessages() // Refresh messages
  } catch (error) {
    console.error('Failed to send message:', error)
  }
}

const joinVideoCall = () => {
  // Placeholder for Jitsi Meet integration
  alert('Video call integration will be implemented in the next phase')
}

const startMessagePolling = () => {
  messagePolling = window.setInterval(loadMessages, 5000) // Poll every 5 seconds
}

const stopMessagePolling = () => {
  if (messagePolling) {
    clearInterval(messagePolling)
    messagePolling = null
  }
}

const goBack = () => {
  router.push('/circles')
}


const formatDate = (dateString?: string) => {
  if (!dateString) return 'Unknown'
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadCircle()
})

onUnmounted(() => {
  stopMessagePolling()
})
</script>