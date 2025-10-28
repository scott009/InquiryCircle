<template>
  <div class="ai-translation-display">
    <div class="header">
      <h3 class="title">AI Translation ({{ languageLabel }})</h3>
      <span class="badge">Original</span>
    </div>
    <div class="content">
      <p v-if="translationText" class="text">{{ translationText }}</p>
      <p v-else class="placeholder">No translation available</p>
    </div>
  </div>
</template>

<script lang="ts">
/**
 * AITranslationDisplay Component (aitrans1)
 *
 * Displays AI-generated translation from JSON.
 * Read-only display of the '<language>_text' field.
 *
 * Phase 3: Full implementation with styling
 */

export default {
  name: 'AITranslationDisplay',
  props: {
    translationText: {
      type: String,
      default: ''
    },
    language: {
      type: String,
      default: 'thai'
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
      return labels[this.language] || this.language.charAt(0).toUpperCase() + this.language.slice(1)
    }
  }
}
</script>

<style scoped>
.ai-translation-display {
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background: white;
  overflow: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #eff6ff;
  border-bottom: 1px solid #bfdbfe;
}

.title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1e40af;
}

.badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 0.25rem;
  font-weight: 500;
}

.content {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

.text {
  margin: 0;
  line-height: 1.6;
  color: #1f2937;
  white-space: pre-wrap;
}

.placeholder {
  margin: 0;
  color: #9ca3af;
  font-style: italic;
}
</style>
