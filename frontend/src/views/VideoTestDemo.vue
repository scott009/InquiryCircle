<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Main content -->
    <div class="max-w-full mx-auto py-6 px-4 space-y-6">
      <!-- Middle Row: JitsiWin1 (2/3) + ContentPanel1 (1/3) -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- JitsiWin1: Video Conference Area (2/3 width - 2 columns) -->
        <div class="lg:col-span-2">
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                Circle: "{{ circleName }}"
              </h3>

              <!-- Loading State -->
              <div v-if="isLoading" class="text-center py-8">
                <p class="text-gray-600">Loading circle information...</p>
              </div>

              <!-- No Circle Error -->
              <div v-else-if="noCircleError" class="text-center py-8">
                <p class="text-red-600 mb-4">You are not assigned to any circle yet.</p>
                <p class="text-gray-600">Please contact your facilitator to be added to a circle.</p>
              </div>

              <!-- Jitsi Video Conference Component -->
              <VideoConference
                v-else
                :circleId="circleId"
                :sessionId="mockSessionId"
                :circleTitle="circleName"
                :userDisplayName="`${authStore.userRole || 'User'}`"
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

      <!-- ReactionBar1: Reaction buttons with display mode controls -->
      <div>
        <ReactionBar1 />
      </div>

      <!-- DescBar1: Element description display -->
      <div class="w-1/2">
        <DescBar1 />
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import VideoConference from '../components/circles/VideoConference.vue'
import HtmlWin1 from '../components/html/HtmlWin1.vue'
import HtmlWin2 from '../components/html/HtmlWin2.vue'
import ReactionBar1 from '../components/reactions/ReactionBar1.vue'
import DescBar1 from '../components/reactions/DescBar1.vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

// Get circle data from authenticated user
const userCircle = computed(() => authStore.userCircle)
const circleId = computed(() => userCircle.value?.jitsi_room_id || 'demo-fallback')
const circleName = computed(() => userCircle.value?.name || 'No Circle Assigned')

const mockSessionId = 'session-static-demo'  // Static session for testing
const isVideoJoined = ref(false)
const videoParticipants = ref<any[]>([])
const eventLog = ref<Array<{ timestamp: Date, message: string }>>([])
const isLoading = ref(true)
const noCircleError = ref(false)

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

// Check authentication and load circle on mount
onMounted(async () => {
  // Redirect to login if not authenticated
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: '/meeting' } })
    return
  }

  // Check if user has a circle assigned
  if (!authStore.userCircle) {
    console.warn('User is authenticated but not assigned to any circle')
    noCircleError.value = true
    isLoading.value = false
    addToEventLog('❌ No circle assigned')
    return
  }

  // Set circle name in TopBar
  const { useTopBar } = await import('../composables/useTopBar')
  const { setCircleName } = useTopBar()
  setCircleName(circleName.value)

  isLoading.value = false
  addToEventLog(`✅ Joined circle: ${circleName.value}`)
  console.log('Meeting view loaded:', {
    role: authStore.userRole,
    circle: authStore.userCircle
  })
})
</script>