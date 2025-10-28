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
export interface CircleInfo {
  id: number
  name: string
  jitsi_room_id: string
  circle_type?: 'discussion' | 'translation' | 'study'
}

export interface AuthResponse {
  valid: boolean
  role?: 'facilitator' | 'participant'
  key_id?: number
  circle?: CircleInfo
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
  circle_type: 'discussion' | 'translation' | 'study'
}

export interface CircleDetail extends Circle {
  participants: ParticipantKey[]
}

export interface ParticipantKey {
  key_id: number
  access_key: string
  role: 'participant' | 'facilitator'
  created_at: string
}

export interface CreateCircleRequest {
  name: string
  description?: string
}

export interface UpdateCircleRequest {
  name?: string
  description?: string
  status?: 'inactive' | 'active' | 'ended'
}

export interface GenerateKeyRequest {
  key_name?: string
  custom_key?: string
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

  async getCircle(circleId: number): Promise<CircleDetail> {
    const response = await apiClient.get(`/circles/${circleId}/`)
    return response.data
  }

  async updateCircle(circleId: number, circleData: UpdateCircleRequest): Promise<Circle> {
    const response = await apiClient.put(`/circles/${circleId}/`, circleData)
    return response.data
  }

  async deleteCircle(circleId: number): Promise<{ message: string }> {
    const response = await apiClient.delete(`/circles/${circleId}/`)
    return response.data
  }

  async generateParticipantKey(circleId: number, keyData?: GenerateKeyRequest): Promise<ParticipantKey> {
    const response = await apiClient.post(`/circles/${circleId}/keys/generate/`, keyData || {})
    return response.data
  }

  async removeParticipantKey(circleId: number, keyId: number): Promise<{ message: string }> {
    const response = await apiClient.delete(`/circles/${circleId}/keys/${keyId}/remove/`)
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

  // Translation API Methods

  // Get all translation documents
  async getTranslationDocuments(circleId?: number): Promise<TranslationDocument[]> {
    const url = circleId ? `/translation/documents/?circle=${circleId}` : '/translation/documents/'
    const response = await apiClient.get(url)
    return response.data
  }

  // Get single translation document
  async getTranslationDocument(documentId: number): Promise<TranslationDocument> {
    const response = await apiClient.get(`/translation/documents/${documentId}/`)
    return response.data
  }

  // Start translation session
  async startTranslationSession(data: SessionStartRequest): Promise<TranslationSession> {
    const response = await apiClient.post('/translation/sessions/start/', data)
    return response.data
  }

  // Get session details
  async getTranslationSession(sessionId: number): Promise<TranslationSession> {
    const response = await apiClient.get(`/translation/sessions/${sessionId}/`)
    return response.data
  }

  // End translation session
  async endTranslationSession(sessionId: number): Promise<{ message: string; session: TranslationSession }> {
    const response = await apiClient.post(`/translation/sessions/${sessionId}/end/`)
    return response.data
  }

  // List all paragraphs in a session
  async getSessionParagraphs(
    sessionId: number,
    filters?: { status?: string; chapter?: string }
  ): Promise<ParagraphsResponse> {
    let url = `/translation/sessions/${sessionId}/paragraphs/`
    if (filters) {
      const params = new URLSearchParams()
      if (filters.status) params.append('status', filters.status)
      if (filters.chapter) params.append('chapter', filters.chapter)
      if (params.toString()) url += `?${params.toString()}`
    }
    const response = await apiClient.get(url)
    return response.data
  }

  // Get single paragraph
  async getParagraph(paragraphId: number): Promise<ParagraphCorrection> {
    const response = await apiClient.get(`/translation/paragraphs/${paragraphId}/`)
    return response.data
  }

  // Update paragraph correction
  async updateParagraph(
    paragraphId: number,
    data: ParagraphUpdateRequest
  ): Promise<ParagraphCorrection> {
    const response = await apiClient.patch(`/translation/paragraphs/${paragraphId}/update/`, data)
    return response.data
  }

  // Approve paragraph (facilitator only)
  async approveParagraph(paragraphId: number): Promise<ParagraphCorrection> {
    const response = await apiClient.post(`/translation/paragraphs/${paragraphId}/approve/`)
    return response.data
  }
}

// Translation types
export interface TranslationDocument {
  id: number
  circle: number
  file_path: string
  language: string
  status: 'uploaded' | 'loaded' | 'in_session' | 'saved' | 'archived'
  title: string
  edition: string
  json_version: string
  created_by: number | null
  created_at: string
  last_loaded_at: string | null
  last_saved_at: string | null
}

export interface TranslationSession {
  id: number
  document: number
  circle: number
  status: 'active' | 'completed' | 'aborted'
  started_by: number | null
  started_at: string
  ended_at: string | null
  ended_by: number | null
  total_paragraphs: number
  paragraphs_modified: number
}

export interface ParagraphCorrection {
  id: number
  session: number
  paragraph_id: string
  chapter_id: string
  section_id: string
  text: string
  original_translation: string
  corrected_translation: string
  status: 'unchecked' | 'in_progress' | 'approved'
  last_modified_by: number | null
  last_modified_at: string
  approved_by: number | null
  approved_at: string | null
}

export interface SessionStartRequest {
  document_id: number
  circle_id: number
}

export interface ParagraphUpdateRequest {
  corrected_translation: string
  status?: 'unchecked' | 'in_progress' | 'approved'
}

export interface ParagraphsResponse {
  session_id: number
  total_paragraphs: number
  paragraphs: ParagraphCorrection[]
}

// Export singleton instance
export const apiService = new ApiService()

// Export default
export default apiService