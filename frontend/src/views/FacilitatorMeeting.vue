<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Row Header: TitleBlock + StatusWin1 + TopMenu1 -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-4">
          <div class="grid grid-cols-12 gap-4 items-center">
            <!-- TitleBlock (Left - 6 columns) -->
            <div class="col-span-6">
              <h1 class="text-2xl font-bold text-gray-900">Facilitator's Meeting Page</h1>
              <p class="text-sm text-gray-500 mt-1">Facilitator view with enhanced controls</p>
            </div>

            <!-- StatusWin1 (Middle-Right - 4 columns, minimized) -->
            <div class="col-span-4">
              <div class="bg-gray-50 rounded-lg p-3">
                <h3 class="text-sm font-medium text-gray-700 mb-2">Status</h3>
                <div class="flex items-center space-x-4 text-xs">
                  <div>
                    <span :class="{
                      'text-green-600': isVideoJoined,
                      'text-gray-500': !isVideoJoined
                    }">
                      {{ isVideoJoined ? '● Connected' : '○ Not Connected' }}
                    </span>
                  </div>
                  <div v-if="videoParticipants.length > 0" class="text-gray-600">
                    {{ videoParticipants.length + 1 }} participants
                  </div>
                  <div class="text-gray-500">
                    Session: {{ mockSessionId.slice(-8) }}
                  </div>
                </div>
              </div>
            </div>

            <!-- TopMenu1 (Right - 2 columns) -->
            <div class="col-span-2">
              <div class="flex items-center justify-end space-x-2">
                <button class="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100">
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                  </svg>
                </button>
                <router-link
                  to="/"
                  class="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
                  title="Back to Home"
                >
                  <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                  </svg>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="max-w-full mx-auto py-6 px-4 space-y-6">
      <!-- Middle Row: JitsiWin1 (2/3) + ContentPanel1 (1/3) -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- JitsiWin1: Video Conference Area (2/3 width - 2 columns) -->
        <div class="lg:col-span-2">
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

        <!-- ContentPanel1: Right content area (1/3 width - 1 column) -->
        <div class="lg:col-span-1">
          <div class="h-[50vh] bg-white shadow overflow-hidden sm:rounded-lg">
            <HtmlWin1 />
          </div>
        </div>
      </div>

      <!-- Bottom Row: ContentPanel2 (Full Width) -->
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="h-auto">
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