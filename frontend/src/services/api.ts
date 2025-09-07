import axios from 'axios'

// API client configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for logging and auth
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging and error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error(`❌ API Error: ${error.response?.status} ${error.config?.url}`, error.response?.data);
    
    // Enhance error with user-friendly messages
    if (error.response?.status === 401) {
      console.warn('🔐 Authentication required or invalid key');
    } else if (error.response?.status === 403) {
      console.warn('🚫 Permission denied');
    } else if (error.response?.status === 404) {
      console.warn('📭 Resource not found');
    } else if (error.response?.status >= 500) {
      console.warn('🔥 Server error');
    }
    
    return Promise.reject(error);
  }
);

// Auth types
export interface AuthResponse {
  valid: boolean
  role?: 'facilitator' | 'participant'
  key_id?: number
  error?: string
}

// Circle types
export interface Circle {
  id: number
  name: string
  description: string
  status: 'inactive' | 'active' | 'ended'
  created_at: string
  jitsi_room_id: string
}

export interface CreateCircleRequest {
  name: string
  description?: string
}

export interface CirclesResponse {
  circles: Circle[]
}

// Message types
export interface Message {
  id: number
  content: string
  message_type: 'text' | 'html' | 'system'
  sent_at: string
  sender_role?: string
  timestamp?: string
}

export interface CreateMessageRequest {
  circle_id: number
  content: string
  message_type?: 'text' | 'html' | 'system'
}

export interface MessagesResponse {
  messages: Message[]
}

// Jitsi Room types
export interface JitsiRoomConfig {
  roomName: string
  password?: string
  moderator?: boolean
  subject?: string
  maxParticipants?: number
  enableLobby?: boolean
  enableRecording?: boolean
}

export interface JitsiRoom {
  room_id: number
  room_name: string
  room_password: string
  status: 'created' | 'active' | 'ended' | 'expired'
  config: JitsiRoomConfig
  participant_count: number
  max_participants: number
  created_at: string
  expires_at?: string
}

export interface CreateRoomRequest {
  circle_id: number
  enable_lobby?: boolean
  enable_recording?: boolean
  max_participants?: number
}

export interface JoinRoomRequest {
  participant_id: string
  display_name: string
}

export interface LeaveRoomRequest {
  participant_id: string
}

// API Service Class
export class ApiService {
  private accessKey: string | null = null

  setAccessKey(key: string) {
    this.accessKey = key
    // Set default authorization header
    apiClient.defaults.headers.common['Authorization'] = `Key ${key}`
  }

  clearAccessKey() {
    this.accessKey = null
    delete apiClient.defaults.headers.common['Authorization']
  }

  getAccessKey() {
    return this.accessKey
  }

  // Health check
  async healthCheck(): Promise<{ status: string; database: string }> {
    const response = await apiClient.get('/health/')
    return response.data
  }

  // Authentication
  async verifyKey(key?: string): Promise<AuthResponse> {
    const keyToUse = key || this.accessKey
    if (!keyToUse) {
      return { valid: false, error: 'No access key provided' }
    }

    try {
      const response = await apiClient.post(
        '/auth/verify-key/',
        {},
        {
          headers: {
            Authorization: `Key ${keyToUse}`,
          },
        }
      )
      return response.data
    } catch (error: any) {
      if (error.response?.data) {
        return error.response.data
      }
      return { valid: false, error: 'Network error' }
    }
  }

  // Circles
  async getCircles(): Promise<CirclesResponse> {
    const response = await apiClient.get('/circles/')
    return response.data
  }

  async createCircle(circleData: CreateCircleRequest): Promise<Circle> {
    const response = await apiClient.post('/circles/', circleData)
    return response.data
  }

  // Messages
  async getMessages(circleId: number): Promise<MessagesResponse> {
    const response = await apiClient.get(
      `/messages/?circle_id=${circleId}`
    )
    return response.data
  }

  async sendMessage(messageData: CreateMessageRequest): Promise<Message> {
    const response = await apiClient.post('/messages/', messageData)
    return response.data
  }

  // Jitsi Room Management
  async createRoom(roomData: CreateRoomRequest): Promise<JitsiRoom> {
    const response = await apiClient.post('/rooms/create/', roomData)
    return response.data
  }

  async getRoomConfig(circleId: number): Promise<JitsiRoom> {
    const response = await apiClient.get(`/rooms/circle/${circleId}/`)
    return response.data
  }

  async joinRoom(roomId: number, joinData: JoinRoomRequest): Promise<any> {
    const response = await apiClient.post(`/rooms/${roomId}/join/`, joinData)
    return response.data
  }

  async leaveRoom(roomId: number, leaveData: LeaveRoomRequest): Promise<any> {
    const response = await apiClient.post(`/rooms/${roomId}/leave/`, leaveData)
    return response.data
  }

  async getRoomStats(roomId: number): Promise<any> {
    const response = await apiClient.get(`/rooms/${roomId}/stats/`)
    return response.data
  }

  // Connection testing
  async testConnection(): Promise<boolean> {
    try {
      await this.healthCheck()
      console.log('✅ API connection successful')
      return true
    } catch (error) {
      console.error('❌ API connection failed:', error)
      return false
    }
  }

  // Error handling helper
  isAxiosError(error: any): boolean {
    return error && error.isAxiosError === true
  }

  // Get user-friendly error message
  getErrorMessage(error: any): string {
    if (this.isAxiosError(error)) {
      if (error.response?.data?.message) {
        return error.response.data.message
      }
      if (error.response?.data?.error) {
        return error.response.data.error
      }
      if (error.response?.status === 401) {
        return 'Authentication required. Please check your access key.'
      }
      if (error.response?.status === 403) {
        return 'Permission denied. You do not have access to this resource.'
      }
      if (error.response?.status === 404) {
        return 'Resource not found.'
      }
      if (error.response?.status >= 500) {
        return 'Server error. Please try again later.'
      }
      if (error.code === 'ECONNREFUSED') {
        return 'Cannot connect to server. Please ensure the backend is running.'
      }
      return error.message || 'An unexpected error occurred'
    }
    return error?.message || 'An unknown error occurred'
  }
}

// Export singleton instance
export const apiService = new ApiService()

// Export default
export default apiService