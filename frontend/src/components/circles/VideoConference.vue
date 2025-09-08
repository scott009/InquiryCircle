<template>
  <div class="video-conference">
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Conference Header -->
      <div class="bg-blue-600 text-white px-6 py-4">
        <h2 class="text-xl font-semibold">{{ circleTitle || 'InquiryCircle Session' }}</h2>
        <p class="text-blue-100 text-sm mt-1">
          Room: {{ roomName }} | Participants: {{ participantCount }}
        </p>
      </div>

      <!-- Conference Controls (if not joined) -->
      <div v-if="!isJoined" class="p-6">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Your Display Name
          </label>
          <input
            v-model="displayName"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your name"
          />
        </div>
        
        <button
          @click="joinConference"
          :disabled="!displayName.trim() || isLoading"
          class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ isLoading ? 'Connecting...' : 'Join Video Conference' }}
        </button>
      </div>

      <!-- Jitsi Conference Container -->
      <div
        v-show="isJoined"
        id="jitsi-conference"
        class="w-full"
        style="height: 500px;"
      ></div>

      <!-- Conference Footer (when joined) -->
      <div v-if="isJoined" class="bg-gray-50 px-6 py-3 border-t">
        <div class="flex justify-between items-center">
          <div class="text-sm text-gray-600">
            Connected as: {{ displayName }}
          </div>
          <button
            @click="leaveConference"
            class="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700 transition-colors"
          >
            Leave Conference
          </button>
        </div>
      </div>

      <!-- Error State -->
      <div v-if="error" class="p-6 bg-red-50 border-l-4 border-red-400">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-red-700">
              {{ error }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { apiService, type JitsiRoom } from '@/services/api';
import jitsiService, { JitsiService } from '../../services/jitsi';

interface Props {
  circleId: string;
  sessionId?: string;
  circleTitle?: string;
  userDisplayName?: string;
}

const props = withDefaults(defineProps<Props>(), {
  circleTitle: 'InquiryCircle Session',
  userDisplayName: ''
});

const emit = defineEmits<{
  joined: [participantInfo: any];
  left: [];
  participantJoined: [participant: any];
  participantLeft: [participant: any];
}>();

// Reactive state
const authStore = useAuthStore();
const displayName = ref(props.userDisplayName || '');
const isJoined = ref(false);
const isLoading = ref(false);
const participantCount = ref(0);
const error = ref('');
const jitsiApi = ref<any>(null);
const currentRoom = ref<JitsiRoom | null>(null);
const participantId = ref(`user-${Date.now()}-${Math.random().toString(36).substring(7)}`);

// Computed room name
const roomName = computed(() => {
  return currentRoom.value?.room_name || 
         JitsiService.generateRoomName(props.circleId, props.sessionId);
});

// Get or create room configuration
const getRoomConfig = async () => {
  // Validate circleId
  const circleIdNum = parseInt(props.circleId);
  if (isNaN(circleIdNum)) {
    throw new Error(`Invalid circle ID: ${props.circleId}`);
  }
  
  try {
    // First try to get existing room
    const roomConfig = await apiService.getRoomConfig(circleIdNum);
    currentRoom.value = roomConfig;
    return roomConfig;
  } catch (error: any) {
    if (error.response?.status === 404) {
      // No room exists, create one if user is facilitator
      if (authStore.isFacilitator) {
        const newRoom = await apiService.createRoom({
          circle_id: circleIdNum,
          enable_lobby: true,
          enable_recording: false,
          max_participants: 20
        });
        currentRoom.value = newRoom;
        return newRoom;
      } else {
        throw new Error('No active room found. Please ask the facilitator to start the video conference.');
      }
    }
    throw error;
  }
};

// Join conference
const joinConference = async () => {
  if (!displayName.value.trim()) {
    error.value = 'Please enter your display name';
    return;
  }

  try {
    isLoading.value = true;
    error.value = '';

    // Get room configuration from backend
    const roomConfig = await getRoomConfig();
    
    const api = await jitsiService.initializeConference({
      roomName: roomConfig.room_name,
      displayName: displayName.value.trim(),
      subject: roomConfig.config.subject || props.circleTitle,
      password: roomConfig.room_password,
      moderator: authStore.isFacilitator
    }, 'jitsi-conference');

    jitsiApi.value = api;

    // Notify backend of join
    try {
      await apiService.joinRoom(roomConfig.room_id, {
        participant_id: participantId.value,
        display_name: displayName.value.trim()
      });
    } catch (joinError) {
      console.warn('Failed to notify backend of room join:', joinError);
    }

    // Set up event listeners
    setupEventListeners();

    isJoined.value = true;
    
  } catch (err: any) {
    error.value = err.message || 'Failed to join conference. Please try again.';
    console.error('Conference join error:', err);
  } finally {
    isLoading.value = false;
  }
};

// Leave conference
const leaveConference = async () => {
  if (jitsiApi.value) {
    // Notify backend of leave
    if (currentRoom.value) {
      try {
        await apiService.leaveRoom(currentRoom.value.room_id, {
          participant_id: participantId.value
        });
      } catch (leaveError) {
        console.warn('Failed to notify backend of room leave:', leaveError);
      }
    }
    
    jitsiService.hangup();
  }
};

// Setup Jitsi event listeners
const setupEventListeners = () => {
  if (!jitsiApi.value) return;

  jitsiService.onVideoConferenceJoined((participant) => {
    console.log('Conference joined:', participant);
    emit('joined', participant);
  });

  jitsiService.onVideoConferenceLeft(() => {
    console.log('Conference left');
    isJoined.value = false;
    participantCount.value = 0;
    emit('left');
  });

  jitsiService.onParticipantJoined((participant) => {
    console.log('Participant joined:', participant);
    participantCount.value++;
    emit('participantJoined', participant);
  });

  jitsiService.onParticipantLeft((participant) => {
    console.log('Participant left:', participant);
    participantCount.value = Math.max(0, participantCount.value - 1);
    emit('participantLeft', participant);
  });

  jitsiService.onReadyToClose(() => {
    console.log('Ready to close');
    isJoined.value = false;
    participantCount.value = 0;
    emit('left');
  });
};

// Cleanup on unmount
onUnmounted(() => {
  if (jitsiApi.value) {
    jitsiService.dispose();
  }
});
</script>

<style scoped>
.video-conference {
  max-width: 100%;
}

#jitsi-conference {
  background: #000;
  border-radius: 0;
}
</style>