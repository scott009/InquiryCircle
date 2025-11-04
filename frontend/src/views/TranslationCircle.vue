<template>
  <div class="translation-circle">
    <!-- Header with session info -->
    <div class="header">
      <div class="header-top">
        <div class="header-left">
          <h1 class="title">Translation Circle</h1>
          <div v-if="session" class="session-info">
            <span class="info-item">Document: {{ document?.title || 'Loading...' }}</span>
            <span class="info-item">Language: {{ languageLabel }}</span>
            <span class="info-item">Paragraphs: {{ paragraphs.length }}</span>
          </div>
          <div v-else class="loading">Loading session...</div>
        </div>
        <div class="header-right">
          <span v-if="authStore.userRole" class="user-display-name">
            {{ authStore.userRole === 'facilitator' ? 'Facilitator' : 'Participant' }}
          </span>
          <button v-if="authStore.isFacilitator && session" @click="handleEndSession" class="end-session-button">
            End Session
          </button>
        </div>
      </div>

      <!-- Facilitator Controls + English Text Row (only for facilitators) -->
      <div v-if="authStore.isFacilitator" class="controls-content-row">
        <div class="facilitator-controls-container">
          <FacilitatorControls
            :documents="availableDocuments"
            :current-document="document"
            :current-language="targetLanguage"
            :paragraphs="paragraphs"
            @document-change="handleDocumentChange"
            @language-change="handleLanguageChange"
          />
        </div>
        <div class="english-text-container">
          <EnglishTextDisplay
            :text="currentParagraph?.text"
            :paragraph-id="currentParagraph?.paragraph_id"
          />
        </div>
      </div>

      <!-- English Text for Participants (full width when no facilitator controls) -->
      <div v-else class="participant-english-container">
        <EnglishTextDisplay
          :text="currentParagraph?.text"
          :paragraph-id="currentParagraph?.paragraph_id"
        />
      </div>
    </div>

    <!-- Main content: 2-row layout -->
    <div class="content-grid">
      <!-- Top Row: Video Conference -->
      <div class="video-container">
        <!-- Loading state for video -->
        <div v-if="!circleId" class="loading-box">
          <p>Error: No circle ID provided</p>
        </div>

        <!-- Video conference (render independently of session) -->
        <VideoConference
          v-else
          :circleId="circleId.toString()"
          :sessionId="session?.id.toString() || 'pending'"
          :circleTitle="`Translation: ${document?.title || 'Loading...'}`"
          userDisplayName="Translator"
        />
      </div>

      <!-- Bottom Row: Navigator + AI Translation + Editor -->
      <div class="document-navigator">
        <DocumentNavigator
          :paragraphs="paragraphs"
          :selected-paragraph-id="currentParagraph?.id"
          :loading="loadingParagraphs"
          :error="error"
          @select="handleSelectParagraph"
        />
      </div>

      <div class="ai-translation-display">
        <AITranslationDisplay
          :translation-text="currentParagraph?.original_translation"
          :language="targetLanguage"
        />
      </div>

      <div class="corrected-text-editor">
        <CorrectedTextEditor
          ref="editor"
          :corrected-text="currentParagraph?.corrected_translation"
          :language="targetLanguage"
          :paragraph-id="currentParagraph?.paragraph_id"
          @save="handleSave"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
/**
 * TranslationCircle View
 *
 * Main route for collaborative translation editing circles.
 * Composes 5 display elements: video + 4 translation-specific elements.
 *
 * Phase 4: Circle integration with authentication and membership ✅
 * Phase 5: Jitsi video integration ✅
 * TODO Phase 6: Add facilitator controls
 * TODO Phase 7: Real-time collaboration with paragraph locking
 */

import EnglishTextDisplay from '@/components/circles/translation/EnglishTextDisplay.vue'
import AITranslationDisplay from '@/components/circles/translation/AITranslationDisplay.vue'
import CorrectedTextEditor from '@/components/circles/translation/CorrectedTextEditor.vue'
import DocumentNavigator from '@/components/circles/translation/DocumentNavigator.vue'
import VideoConference from '@/components/circles/VideoConference.vue'
import FacilitatorControls from '@/components/circles/translation/FacilitatorControls.vue'
import { apiService } from '@/services/api'
import type { TranslationDocument, TranslationSession, ParagraphCorrection } from '@/services/api'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'TranslationCircle',
  components: {
    EnglishTextDisplay,
    AITranslationDisplay,
    CorrectedTextEditor,
    DocumentNavigator,
    VideoConference,
    FacilitatorControls,
  },
  setup() {
    const authStore = useAuthStore()
    return {
      authStore
    }
  },
  data() {
    return {
      // Get from route params (Phase 4)
      circleId: parseInt(this.$route.params.circleId as string),

      // Phase 6: Facilitator can select document and language
      documentId: 1,
      targetLanguage: 'thai',
      availableDocuments: [] as TranslationDocument[],

      // State
      document: null as TranslationDocument | null,
      session: null as TranslationSession | null,
      paragraphs: [] as ParagraphCorrection[],
      currentParagraph: null as ParagraphCorrection | null,

      // UI state
      loadingParagraphs: false,
      error: ''
    }
  },
  computed: {
    languageLabel(): string {
      const labels: Record<string, string> = {
        'thai': 'Thai',
        'vietnamese': 'Vietnamese',
        'korean': 'Korean',
        'japanese': 'Japanese',
        'tibetan': 'Tibetan',
        'chinese_simplified': 'Simplified Chinese',
        'chinese_traditional': 'Traditional Chinese'
      }
      return labels[this.targetLanguage] || this.targetLanguage
    }
  },
  async mounted() {
    console.log('TranslationCircle view loaded - Phase 6')
    console.log('Route params:', this.$route.params)
    console.log('Circle ID:', this.circleId)
    console.log('Document ID:', this.documentId)
    console.log('User role:', this.authStore.userRole)
    console.log('Is facilitator:', this.authStore.isFacilitator)

    if (!this.circleId || isNaN(this.circleId)) {
      console.error('Invalid circle ID:', this.$route.params.circleId)
      this.error = 'Invalid circle ID in URL'
      return
    }

    // Phase 6: Load available documents for facilitator
    if (this.authStore.isFacilitator) {
      await this.loadAvailableDocuments()
    }

    await this.initializeSession()
  },
  methods: {
    async initializeSession() {
      try {
        // Start a new translation session
        console.log('Starting translation session...')
        this.session = await apiService.startTranslationSession({
          document_id: this.documentId,
          circle_id: this.circleId
        })

        console.log('Session started:', this.session)

        // Load paragraphs for this session
        await this.loadParagraphs()

        // Select first paragraph by default
        if (this.paragraphs.length > 0) {
          this.currentParagraph = this.paragraphs[0]
        }
      } catch (error: any) {
        console.error('Failed to initialize session:', error)
        if (error.response?.status === 409) {
          // Session already exists, try to load it
          console.log('Active session exists, loading existing session...')
          await this.loadExistingSession()
        } else {
          this.error = apiService.getErrorMessage(error)
        }
      }
    },

    async loadExistingSession() {
      try {
        // Try to load the most recent active session (Phase 3 testing)
        // In Phase 4, we'll get this from backend or store
        const sessionId = 2  // Updated to use the working session
        this.session = await apiService.getTranslationSession(sessionId)
        await this.loadParagraphs()
        if (this.paragraphs.length > 0) {
          this.currentParagraph = this.paragraphs[0]
        }
      } catch (error: any) {
        this.error = 'Failed to load existing session'
        console.error(error)
      }
    },

    async loadParagraphs() {
      if (!this.session) return

      this.loadingParagraphs = true
      this.error = ''

      try {
        const response = await apiService.getSessionParagraphs(this.session.id)
        this.paragraphs = response.paragraphs
        console.log(`Loaded ${this.paragraphs.length} paragraphs`)
      } catch (error: any) {
        this.error = apiService.getErrorMessage(error)
        console.error('Failed to load paragraphs:', error)
      } finally {
        this.loadingParagraphs = false
      }
    },

    handleSelectParagraph(paragraph: ParagraphCorrection) {
      console.log('Selected paragraph:', paragraph.paragraph_id)
      this.currentParagraph = paragraph
    },

    async handleSave(correctedText: string) {
      if (!this.currentParagraph) return

      try {
        console.log('Saving paragraph:', this.currentParagraph.paragraph_id)

        const updated = await apiService.updateParagraph(
          this.currentParagraph.id,
          {
            corrected_translation: correctedText,
            status: 'in_progress'
          }
        )

        // Update the paragraph in our list
        const index = this.paragraphs.findIndex(p => p.id === updated.id)
        if (index !== -1) {
          this.paragraphs[index] = updated
        }

        // Update current paragraph
        this.currentParagraph = updated

        // Show success message in editor
        const editor = this.$refs.editor as any
        if (editor && editor.showSaveSuccess) {
          editor.showSaveSuccess()
        }

        console.log('Paragraph saved successfully')
      } catch (error: any) {
        console.error('Failed to save paragraph:', error)
        const errorMessage = apiService.getErrorMessage(error)

        // Show error in editor
        const editor = this.$refs.editor as any
        if (editor && editor.showSaveError) {
          editor.showSaveError(errorMessage)
        }
      }
    },

    async handleEndSession() {
      if (!this.session) return

      const confirmed = confirm(
        'Are you sure you want to end this session? All corrections will be saved to the JSON file.'
      )

      if (!confirmed) return

      try {
        console.log('Ending session...')
        const result = await apiService.endTranslationSession(this.session.id)
        console.log('Session ended:', result.message)
        alert('Session ended successfully! Corrections saved to JSON file.')

        // Could redirect to another page or reload
        // For now, just refresh
        window.location.reload()
      } catch (error: any) {
        console.error('Failed to end session:', error)
        alert('Failed to end session: ' + apiService.getErrorMessage(error))
      }
    },

    // Phase 6: Facilitator control handlers
    async loadAvailableDocuments() {
      try {
        // TODO: Add API endpoint to get available translation documents
        // For now, we'll create a mock list
        this.availableDocuments = [
          {
            id: 1,
            title: 'Recovery Dharma - Full Text',
            filename: 'rdg_en_v3.json'
          } as unknown as TranslationDocument
        ]
      } catch (error: any) {
        console.error('Failed to load documents:', error)
      }
    },

    async handleDocumentChange(documentId: number) {
      if (this.documentId === documentId) return

      console.log('Changing document to:', documentId)
      this.documentId = documentId

      // End current session and start a new one with the new document
      if (this.session) {
        try {
          await apiService.endTranslationSession(this.session.id)
        } catch (error: any) {
          console.error('Failed to end session:', error)
        }
      }

      // Reinitialize with new document
      await this.initializeSession()
    },

    async handleLanguageChange(language: string) {
      if (this.targetLanguage === language) return

      console.log('Changing language to:', language)
      this.targetLanguage = language

      // Reload paragraphs with new language
      await this.loadParagraphs()

      // Reset to first paragraph
      if (this.paragraphs.length > 0) {
        this.currentParagraph = this.paragraphs[0]
      }
    }
  }
}
</script>

<style scoped>
.translation-circle {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f3f4f6;
}

.header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.header-top {
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.title {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.session-info {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.info-item {
  font-size: 0.875rem;
  color: #6b7280;
}

.user-display-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border-radius: 0.375rem;
}

.end-session-button {
  padding: 0.5rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.end-session-button:hover {
  background: #dc2626;
}

.controls-content-row {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 1rem;
  padding: 0 1.5rem 1rem 1.5rem;
}

.facilitator-controls-container {
  min-height: 0;
}

.english-text-container {
  min-height: 0;
  max-height: 400px;
  overflow: hidden;
}

.participant-english-container {
  padding: 0 1.5rem 1rem 1.5rem;
  max-height: 400px;
  overflow: hidden;
}

.loading {
  color: #6b7280;
  font-style: italic;
}

.loading-box {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: white;
  border-radius: 0.5rem;
  padding: 2rem;
  color: #ef4444;
  font-weight: 500;
}

.content-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 2fr 2fr;
  grid-template-rows: 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
  overflow: hidden;
}

/* Top row: Video full width */
.video-container {
  grid-column: 1 / 4;
  grid-row: 1;
  min-height: 0;
  height: 100%;
  width: 100%;
}

/* Bottom row: Navigator narrow (1 column), AI wide (1 column), Corrected wide (1 column) */
.document-navigator {
  grid-column: 1;
  grid-row: 2;
  min-height: 0;
  height: 100%;
  width: 100%;
}

.ai-translation-display {
  grid-column: 2;
  grid-row: 2;
  min-height: 0;
  height: 100%;
  width: 100%;
}

.corrected-text-editor {
  grid-column: 3;
  grid-row: 2;
  min-height: 0;
  height: 100%;
  width: 100%;
}
</style>
