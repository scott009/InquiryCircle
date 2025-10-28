<template>
  <div class="translation-circle">
    <!-- Header with session info -->
    <div class="header">
      <h1 class="title">Translation Circle</h1>
      <div v-if="session" class="session-info">
        <span class="info-item">Document: {{ document?.title || 'Loading...' }}</span>
        <span class="info-item">Language: {{ languageLabel }}</span>
        <span class="info-item">Paragraphs: {{ paragraphs.length }}</span>
        <button @click="handleEndSession" class="end-session-button">
          End Session
        </button>
      </div>
      <div v-else class="loading">Loading session...</div>
    </div>

    <!-- Main content: 2x2 grid layout -->
    <div class="content-grid">
      <!-- Top-left: English Text Display -->
      <EnglishTextDisplay
        :text="currentParagraph?.text"
        :paragraph-id="currentParagraph?.paragraph_id"
      />

      <!-- Top-right: AI Translation Display -->
      <AITranslationDisplay
        :translation-text="currentParagraph?.original_translation"
        :language="targetLanguage"
      />

      <!-- Bottom-left: Document Navigator -->
      <DocumentNavigator
        :paragraphs="paragraphs"
        :selected-paragraph-id="currentParagraph?.id"
        :loading="loadingParagraphs"
        :error="error"
        @select="handleSelectParagraph"
      />

      <!-- Bottom-right: Corrected Text Editor -->
      <CorrectedTextEditor
        ref="editor"
        :corrected-text="currentParagraph?.corrected_translation"
        :language="targetLanguage"
        :paragraph-id="currentParagraph?.paragraph_id"
        @save="handleSave"
      />
    </div>
  </div>
</template>

<script lang="ts">
/**
 * TranslationCircle View
 *
 * Main route for collaborative translation editing circles.
 * Composes 4 translation-specific display elements.
 *
 * Phase 3: Full implementation without authentication
 * TODO Phase 4: Add circle authentication and membership
 * TODO Phase 5: Add Jitsi video integration
 * TODO Phase 6: Add facilitator controls
 */

import EnglishTextDisplay from '@/components/circles/translation/EnglishTextDisplay.vue'
import AITranslationDisplay from '@/components/circles/translation/AITranslationDisplay.vue'
import CorrectedTextEditor from '@/components/circles/translation/CorrectedTextEditor.vue'
import DocumentNavigator from '@/components/circles/translation/DocumentNavigator.vue'
import { apiService } from '@/services/api'
import type { TranslationDocument, TranslationSession, ParagraphCorrection } from '@/services/api'

export default {
  name: 'TranslationCircle',
  components: {
    EnglishTextDisplay,
    AITranslationDisplay,
    CorrectedTextEditor,
    DocumentNavigator,
  },
  data() {
    return {
      // Hardcoded for Phase 3 testing (no auth)
      documentId: 1,
      circleId: 7, // Updated to match database

      // State
      document: null as TranslationDocument | null,
      session: null as TranslationSession | null,
      paragraphs: [] as ParagraphCorrection[],
      currentParagraph: null as ParagraphCorrection | null,
      targetLanguage: 'thai',

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
    console.log('TranslationCircle view loaded - Phase 3')
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
  padding: 1rem 1.5rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
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

.end-session-button {
  margin-left: auto;
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

.loading {
  color: #6b7280;
  font-style: italic;
}

.content-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
  overflow: hidden;
}

.content-grid > * {
  min-height: 0;
}
</style>
