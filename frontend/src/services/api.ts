import axios, { AxiosInstance, AxiosResponse } from 'axios'

// API client configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

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
}

export interface CreateMessageRequest {
  circle_id: number
  content: string
  message_type?: 'text' | 'html'
}

export interface MessagesResponse {
  messages: Message[]
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
    const response: AxiosResponse = await apiClient.get('/health/')
    return response.data
  }

  // Authentication
  async verifyKey(key?: string): Promise<AuthResponse> {
    const keyToUse = key || this.accessKey
    if (!keyToUse) {
      return { valid: false, error: 'No access key provided' }
    }

    try {
      const response: AxiosResponse<AuthResponse> = await apiClient.post(
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
    const response: AxiosResponse<CirclesResponse> = await apiClient.get('/circles/')
    return response.data
  }

  async createCircle(circleData: CreateCircleRequest): Promise<Circle> {
    const response: AxiosResponse<Circle> = await apiClient.post('/circles/', circleData)
    return response.data
  }

  // Messages
  async getMessages(circleId: number): Promise<MessagesResponse> {
    const response: AxiosResponse<MessagesResponse> = await apiClient.get(
      `/messages/?circle_id=${circleId}`
    )
    return response.data
  }

  async sendMessage(messageData: CreateMessageRequest): Promise<Message> {
    const response: AxiosResponse<Message> = await apiClient.post('/messages/', messageData)
    return response.data
  }
}

// Export singleton instance
export const apiService = new ApiService()

// Export default
export default apiService