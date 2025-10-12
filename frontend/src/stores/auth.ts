import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService, type AuthResponse, type CircleInfo } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const accessKey = ref<string | null>(null)
  const userRole = ref<'facilitator' | 'participant' | null>(null)
  const keyId = ref<number | null>(null)
  const userCircle = ref<CircleInfo | null>(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isFacilitator = computed(() => userRole.value === 'facilitator')
  const isParticipant = computed(() => userRole.value === 'participant')
  const hasCircle = computed(() => userCircle.value !== null)

  // Actions
  async function login(key: string): Promise<boolean> {
    isLoading.value = true
    error.value = null

    try {
      const response: AuthResponse = await apiService.verifyKey(key)

      if (response.valid && response.role) {
        // Set authentication state
        accessKey.value = key
        userRole.value = response.role
        keyId.value = response.key_id || null
        userCircle.value = response.circle || null
        isAuthenticated.value = true

        // Set API service key
        apiService.setAccessKey(key)

        // Store in localStorage for persistence
        localStorage.setItem('ic_access_key', key)
        localStorage.setItem('ic_user_role', response.role)
        if (response.key_id) {
          localStorage.setItem('ic_key_id', response.key_id.toString())
        }
        if (response.circle) {
          localStorage.setItem('ic_user_circle', JSON.stringify(response.circle))
        }

        return true
      } else {
        error.value = response.error || 'Invalid access key'
        return false
      }
    } catch (err: any) {
      error.value = err.message || 'Authentication failed'
      return false
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    // Clear state
    accessKey.value = null
    userRole.value = null
    keyId.value = null
    userCircle.value = null
    isAuthenticated.value = false
    error.value = null

    // Clear API service
    apiService.clearAccessKey()

    // Clear localStorage
    localStorage.removeItem('ic_access_key')
    localStorage.removeItem('ic_user_role')
    localStorage.removeItem('ic_key_id')
    localStorage.removeItem('ic_user_circle')
  }

  function restoreSession(): boolean {
    // Try to restore from localStorage
    const storedKey = localStorage.getItem('ic_access_key')
    const storedRole = localStorage.getItem('ic_user_role') as 'facilitator' | 'participant' | null
    const storedKeyId = localStorage.getItem('ic_key_id')
    const storedCircle = localStorage.getItem('ic_user_circle')

    if (storedKey && storedRole) {
      accessKey.value = storedKey
      userRole.value = storedRole
      keyId.value = storedKeyId ? parseInt(storedKeyId) : null
      userCircle.value = storedCircle ? JSON.parse(storedCircle) : null
      isAuthenticated.value = true

      // Set API service key
      apiService.setAccessKey(storedKey)

      return true
    }

    return false
  }

  async function checkAuthStatus(): Promise<boolean> {
    if (!accessKey.value) {
      return false
    }

    isLoading.value = true
    
    try {
      const response: AuthResponse = await apiService.verifyKey()
      
      if (response.valid) {
        return true
      } else {
        // Key is no longer valid, logout
        logout()
        return false
      }
    } catch (err) {
      logout()
      return false
    } finally {
      isLoading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    accessKey,
    userRole,
    keyId,
    userCircle,
    isAuthenticated,
    isLoading,
    error,

    // Getters
    isFacilitator,
    isParticipant,
    hasCircle,

    // Actions
    login,
    logout,
    restoreSession,
    checkAuthStatus,
    clearError,
  }
})