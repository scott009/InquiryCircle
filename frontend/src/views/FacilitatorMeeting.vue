<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <h1 class="text-2xl font-bold text-gray-900">Facilitator's Meeting Page</h1>
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

// Mock data for demonstration - MUST match across /meeting and /facmeet
const mockCircle = {
  id: 'demo-circle-main',  // Static ID ensures same room
  name: 'Test Circle (Video Demo)',
  description: 'Demonstration of video conference integration'
}

const mockSessionId = 'session-static-demo'  // Static session for testing
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