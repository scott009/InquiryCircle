<template>
  <div class="corrected-text-editor">
    <div class="header">
      <h3 class="title">Corrected Translation</h3>
      <span v-if="hasChanges" class="badge unsaved">Unsaved</span>
      <span v-if="!hasChanges && correctedText" class="badge saved">Saved</span>
    </div>
    <div class="content">
      <textarea
        v-model="localText"
        :placeholder="placeholder"
        :disabled="!paragraphId"
        class="textarea"
        @input="onInput"
      ></textarea>
      <div class="footer">
        <button
          @click="handleSave"
          :disabled="!hasChanges || saving"
          class="save-button"
        >
          <span v-if="saving">Saving...</span>
          <span v-else>Save Changes</span>
        </button>
        <button
          v-if="hasChanges"
          @click="handleReset"
          :disabled="saving"
          class="reset-button"
        >
          Reset
        </button>
        <span v-if="saveMessage" :class="['message', saveMessageType]">
          {{ saveMessage }}
        </span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
/**
 * CorrectedTextEditor Component (corrected1)
 *
 * Editable textarea for human-corrected translation.
 * Displays and edits 'corrected_<language>_text' field.
 * Save button persists changes to backend.
 *
 * Phase 3: Full implementation with save functionality
 */

export default {
  name: 'CorrectedTextEditor',
  props: {
    correctedText: {
      type: String,
      default: ''
    },
    language: {
      type: String,
      default: 'thai'
    },
    paragraphId: {
      type: String,
      default: ''
    }
  },
  emits: ['save'],
  data() {
    return {
      localText: this.correctedText,
      hasChanges: false,
      saving: false,
      saveMessage: '',
      saveMessageType: 'success' as 'success' | 'error'
    }
  },
  computed: {
    placeholder(): string {
      if (!this.paragraphId) {
        return 'Select a paragraph to edit...'
      }
      return 'Enter corrected translation here...'
    }
  },
  watch: {
    correctedText(newVal) {
      this.localText = newVal
      this.hasChanges = false
    }
  },
  methods: {
    onInput() {
      this.hasChanges = this.localText !== this.correctedText
      this.saveMessage = ''
    },
    async handleSave() {
      if (!this.hasChanges || this.saving) return

      this.saving = true
      this.saveMessage = ''

      try {
        // Emit save event to parent
        this.$emit('save', this.localText)
        // Parent will handle the actual API call and update props
      } catch (error) {
        console.error('Error saving:', error)
        this.saveMessage = 'Failed to save'
        this.saveMessageType = 'error'
      } finally {
        this.saving = false
      }
    },
    handleReset() {
      this.localText = this.correctedText
      this.hasChanges = false
      this.saveMessage = ''
    },
    showSaveSuccess() {
      this.hasChanges = false
      this.saveMessage = 'Saved successfully!'
      this.saveMessageType = 'success'
      setTimeout(() => {
        this.saveMessage = ''
      }, 3000)
    },
    showSaveError(message: string) {
      this.saveMessage = message || 'Failed to save'
      this.saveMessageType = 'error'
    }
  }
}
</script>

<style scoped>
.corrected-text-editor {
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
  background: #f0fdf4;
  border-bottom: 1px solid #bbf7d0;
}

.title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #166534;
}

.badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-weight: 500;
}

.badge.unsaved {
  background: #fef3c7;
  color: #92400e;
}

.badge.saved {
  background: #dcfce7;
  color: #166534;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  overflow: hidden;
}

.textarea {
  flex: 1;
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-family: inherit;
  font-size: 1rem;
  line-height: 1.6;
  resize: none;
  overflow-y: auto;
}

.textarea:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.textarea:disabled {
  background: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
}

.footer {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-top: 0.75rem;
}

.save-button {
  padding: 0.5rem 1rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.save-button:hover:not(:disabled) {
  background: #059669;
}

.save-button:disabled {
  background: #d1d5db;
  color: #9ca3af;
  cursor: not-allowed;
}

.reset-button {
  padding: 0.5rem 1rem;
  background: #6b7280;
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.reset-button:hover:not(:disabled) {
  background: #4b5563;
}

.message {
  font-size: 0.875rem;
  font-weight: 500;
}

.message.success {
  color: #166534;
}

.message.error {
  color: #dc2626;
}
</style>
