<template>
  <div class="facilitator-controls">
    <div class="controls-header">
      <h3>Facilitator Controls</h3>
      <button @click="toggleExpanded" class="toggle-button">
        {{ isExpanded ? '▼' : '▶' }}
      </button>
    </div>

    <div v-if="isExpanded" class="controls-content">
      <!-- Document Selection -->
      <div class="control-group">
        <label for="document-select">Document:</label>
        <select
          id="document-select"
          v-model="selectedDocumentId"
          @change="handleDocumentChange"
          class="control-input"
        >
          <option v-for="doc in documents" :key="doc.id" :value="doc.id">
            {{ doc.title }}
          </option>
        </select>
      </div>

      <!-- Language Selection -->
      <div class="control-group">
        <label for="language-select">Target Language:</label>
        <select
          id="language-select"
          v-model="selectedLanguage"
          @change="handleLanguageChange"
          class="control-input"
        >
          <option value="thai">Thai</option>
          <option value="vietnamese">Vietnamese</option>
          <option value="korean">Korean</option>
          <option value="japanese">Japanese</option>
          <option value="tibetan">Tibetan</option>
          <option value="chinese_simplified">Simplified Chinese</option>
          <option value="chinese_traditional">Traditional Chinese</option>
        </select>
      </div>

      <!-- Progress Tracking -->
      <div class="control-group progress-section">
        <h4>Progress</h4>
        <div class="progress-stats">
          <div class="stat-item">
            <span class="stat-label">Total:</span>
            <span class="stat-value">{{ totalParagraphs }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Reviewed:</span>
            <span class="stat-value">{{ reviewedParagraphs }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Progress:</span>
            <span class="stat-value">{{ progressPercentage }}%</span>
          </div>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import type { TranslationDocument, ParagraphCorrection } from '@/services/api'

export default defineComponent({
  name: 'FacilitatorControls',
  props: {
    documents: {
      type: Array as PropType<TranslationDocument[]>,
      default: () => []
    },
    currentDocument: {
      type: Object as PropType<TranslationDocument | null>,
      default: null
    },
    currentLanguage: {
      type: String,
      required: true
    },
    paragraphs: {
      type: Array as PropType<ParagraphCorrection[]>,
      default: () => []
    }
  },
  emits: ['document-change', 'language-change'],
  data() {
    return {
      isExpanded: true,
      selectedDocumentId: this.currentDocument?.id || 1,
      selectedLanguage: this.currentLanguage
    }
  },
  computed: {
    totalParagraphs(): number {
      return this.paragraphs.length
    },
    reviewedParagraphs(): number {
      // Count paragraphs with corrected_translation that differs from original
      return this.paragraphs.filter(p =>
        p.corrected_translation &&
        p.corrected_translation !== p.original_translation
      ).length
    },
    progressPercentage(): number {
      if (this.totalParagraphs === 0) return 0
      return Math.round((this.reviewedParagraphs / this.totalParagraphs) * 100)
    }
  },
  watch: {
    currentDocument(newDoc) {
      if (newDoc) {
        this.selectedDocumentId = newDoc.id
      }
    },
    currentLanguage(newLang) {
      this.selectedLanguage = newLang
    }
  },
  methods: {
    toggleExpanded() {
      this.isExpanded = !this.isExpanded
    },
    handleDocumentChange() {
      this.$emit('document-change', this.selectedDocumentId)
    },
    handleLanguageChange() {
      this.$emit('language-change', this.selectedLanguage)
    }
  }
})
</script>

<style scoped>
.facilitator-controls {
  background: #1e40af;
  color: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.controls-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #1e3a8a;
}

.controls-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.toggle-button {
  background: none;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
}

.toggle-button:hover {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.25rem;
}

.controls-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.control-group label {
  font-size: 0.875rem;
  font-weight: 500;
}

.control-input {
  padding: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.375rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 0.875rem;
}

.control-input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.15);
}

.control-input option {
  background: #1e3a8a;
  color: white;
}

.progress-section h4 {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  font-weight: 600;
}

.progress-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.375rem;
}

.stat-label {
  font-size: 0.75rem;
  opacity: 0.8;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 700;
}

.progress-bar {
  height: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 0.25rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #10b981;
  transition: width 0.3s ease;
}
</style>
