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
                Circle: "{{ circleName }}"
              </h3>

              <!-- Loading State -->
              <div v-if="isLoading" class="text-center py-8">
                <p class="text-gray-600">Loading circle information...</p>
              </div>

              <!-- No Circle Error -->
              <div v-else-if="noCircleError" class="text-center py-8">
                <p class="text-red-600 mb-4">You don't have any circles created yet.</p>
                <p class="text-gray-600">Please create a circle in the Administration section first.</p>
              </div>

              <!-- Jitsi Video Conference Component -->
              <VideoConference
                v-else
                :circleId="circleId"
                :sessionId="mockSessionId"
                :circleTitle="circleName"
                userDisplayName="Facilitator"
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import VideoConference from '../components/circles/VideoConference.vue'
import HtmlWin1 from '../components/html/HtmlWin1.vue'
import HtmlWin2 from '../components/html/HtmlWin2.vue'
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
    router.push({ name: 'login', query: { redirect: '/facmeet' } })
    return
  }

  // Facilitators must have circles
  if (!authStore.userCircle) {
    console.warn('Facilitator is authenticated but has no circles')
    noCircleError.value = true
    isLoading.value = false
    addToEventLog('❌ No circle found - please create one in Administration')
    return
  }

  // Set circle name in TopBar (if available)
  try {
    const { useTopBar } = await import('../composables/useTopBar')
    const { setCircleName } = useTopBar()
    setCircleName(circleName.value)
  } catch (error) {
    console.warn('TopBar composable not available:', error)
  }

  isLoading.value = false
  addToEventLog(`✅ Facilitator joined circle: ${circleName.value}`)
  console.log('Facilitator meeting view loaded:', {
    role: authStore.userRole,
    circle: authStore.userCircle
  })
})
</script>