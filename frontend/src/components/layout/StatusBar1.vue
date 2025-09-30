<template>
  <div class="flex items-center space-x-4 text-sm">
    <!-- User Name -->
    <div v-if="authStore.isAuthenticated" class="text-gray-700">
      <span class="font-medium">{{ userName }}</span>
    </div>

    <!-- User Role -->
    <div v-if="authStore.isAuthenticated" class="text-gray-600">
      <span class="px-2 py-1 bg-gray-100 rounded text-xs">
        {{ authStore.userRole === 'facilitator' ? 'Facilitator' : 'Participant' }}
      </span>
    </div>

    <!-- Circle Name -->
    <div v-if="circleName" class="text-gray-600">
      <span class="px-2 py-1 bg-blue-50 rounded text-xs">
        {{ circleName }}
      </span>
    </div>

    <!-- Key Info (optional debug) -->
    <div v-if="authStore.isAuthenticated && authStore.accessKey" class="text-xs text-gray-400">
      {{ authStore.accessKey.substring(0, 8) }}...
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '../../stores/auth'

interface Props {
  circleName?: string
  userName?: string
}

const props = withDefaults(defineProps<Props>(), {
  circleName: '',
  userName: 'User'
})

const authStore = useAuthStore()

const userName = computed(() => {
  return props.userName || 'User'
})
</script>
