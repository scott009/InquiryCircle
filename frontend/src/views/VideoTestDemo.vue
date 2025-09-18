<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="flex items-center">
            <router-link 
              to="/"
              class="mr-4 p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </router-link>
            <div class="flex-1">
              <h1 class="text-2xl font-bold text-gray-900">Video Conference Demo</h1>
              <p class="text-sm text-gray-500 mt-1">Stage 2.2.2: Video conferencing with HTML window components</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="max-w-full mx-auto py-6 px-4 space-y-6">
      <!-- Top Row: Video Conference (75%) + Status Window (25%) -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Video Conference Area (75% width - 3 columns) -->
        <div class="lg:col-span-3">
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                Demo Circle: "{{ mockCircle.name }}"
              </h3>

              <!-- Jitsi Video Conference Component -->
              <VideoConference
                :circleId="mockCircle.id"
                :sessionId="mockSessionId"
                :circleTitle="mockCircle.name"
                userDisplayName="Demo User"
                @joined="onVideoJoined"
                @left="onVideoLeft"
                @participantJoined="onParticipantJoined"
                @participantLeft="onParticipantLeft"
              />
            </div>
          </div>
        </div>

        <!-- Status Window (25% width - 1 column) -->
        <div class="lg:col-span-1">
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                Demo Information
              </h3>
              <dl class="space-y-4">
                <div>
                  <dt class="text-sm font-medium text-gray-500">Circle ID</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ mockCircle.id }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Session ID</dt>
                  <dd class="mt-1 text-sm text-gray-900 font-mono text-xs break-all">{{ mockSessionId }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Jitsi Room</dt>
                  <dd class="mt-1 text-sm text-gray-900 font-mono text-xs break-all">
                    inquirycircle-{{ mockCircle.id }}-{{ mockSessionId }}
                  </dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Status</dt>
                  <dd class="mt-1">
                    <span :class="{
                      'text-green-600': isVideoJoined,
                      'text-gray-500': !isVideoJoined
                    }">
                      {{ isVideoJoined ? '● Connected' : '○ Not Connected' }}
                    </span>
                  </dd>
                </div>
                <div v-if="videoParticipants.length > 0">
                  <dt class="text-sm font-medium text-gray-500">Video Participants</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ videoParticipants.length + 1 }} total</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Row: HTML Windows (100% width) -->
      <div class="bg-red-500 text-white p-8 text-center text-2xl font-bold">
        🚨 TEST: If you see this red box, Vue is working! 🚨
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-4">
        <div class="min-h-[500px] bg-yellow-400 p-4">
          <h2 class="text-xl font-bold mb-4">DEBUGGING: HtmlWin1 should appear below</h2>
          <HtmlWin1 />
        </div>
        <div class="min-h-[500px] bg-purple-400 p-4">
          <h2 class="text-xl font-bold mb-4">DEBUGGING: HtmlWin2 should appear below</h2>
          <HtmlWin2 />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import VideoConference from '../components/circles/VideoConference.vue'
import HtmlWin1 from '../components/html/HtmlWin1.vue'
import HtmlWin2 from '../components/html/HtmlWin2.vue'
import { useAuthStore } from '../stores/auth'

// Mock data for demonstration  
const mockCircle = {
  id: '1',
  name: 'Test Circle (Video Demo)',
  description: 'Demonstration of video conference integration'
}

const mockSessionId = `session-${Date.now()}`
const isVideoJoined = ref(false)
const videoParticipants = ref<any[]>([])
const eventLog = ref<Array<{ timestamp: Date, message: string }>>([])
const authStore = useAuthStore()

// Event handlers
const onVideoJoined = (participantInfo: any) => {
  isVideoJoined.value = true
  addToEventLog('✅ Successfully joined video conference')
  console.log('Demo: Video conference joined:', participantInfo)
}

const onVideoLeft = () => {
  isVideoJoined.value = false
  videoParticipants.value = []
  addToEventLog('❌ Left video conference')
  console.log('Demo: Video conference left')
}

const onParticipantJoined = (participant: any) => {
  videoParticipants.value.push(participant)
  addToEventLog(`👋 Participant joined: ${participant.displayName || 'Unknown'}`)
  console.log('Demo: Participant joined:', participant)
}

const onParticipantLeft = (participant: any) => {
  videoParticipants.value = videoParticipants.value.filter(p => p.id !== participant.id)
  addToEventLog(`👋 Participant left: ${participant.displayName || 'Unknown'}`)
  console.log('Demo: Participant left:', participant)
}

const addToEventLog = (message: string) => {
  eventLog.value.unshift({
    timestamp: new Date(),
    message
  })
  
  // Keep only last 20 events
  if (eventLog.value.length > 20) {
    eventLog.value = eventLog.value.slice(0, 20)
  }
}

// Auto-authenticate with demo facilitator key
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    try {
      const success = await authStore.login('facilitator-key-123')
      if (success) {
        addToEventLog('🔑 Authenticated as demo facilitator')
      } else {
        addToEventLog('❌ Authentication failed: Invalid key')
      }
    } catch (error) {
      addToEventLog('❌ Authentication failed: ' + error)
      console.error('Demo authentication failed:', error)
    }
  }
})
</script>