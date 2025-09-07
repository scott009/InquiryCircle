<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4">
      <div class="mb-6">
        <router-link 
          to="/" 
          class="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium"
        >
          ← Back to Dashboard
        </router-link>
      </div>

      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Jitsi Meet Integration Test</h1>
        <p class="text-gray-600 mt-2">Test the video conferencing functionality using Jitsi Meet</p>
      </div>

      <VideoConference 
        :circleId="testCircleId"
        :sessionId="testSessionId"
        :circleTitle="testCircleTitle"
        @joined="onConferenceJoined"
        @left="onConferenceLeft"
        @participantJoined="onParticipantJoined"
        @participantLeft="onParticipantLeft"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import VideoConference from '../components/circles/VideoConference.vue';

// Test configuration
const testCircleId = ref('test-circle-123');
const testSessionId = ref('session-' + Date.now());
const testCircleTitle = ref('InquiryCircle Test Session');

// Event handlers
const onConferenceJoined = (participantInfo: any) => {
  console.log('Conference joined event:', participantInfo);
};

const onConferenceLeft = () => {
  console.log('Conference left event');
};

const onParticipantJoined = (participant: any) => {
  console.log('New participant joined:', participant);
};

const onParticipantLeft = (participant: any) => {
  console.log('Participant left:', participant);
};
</script>