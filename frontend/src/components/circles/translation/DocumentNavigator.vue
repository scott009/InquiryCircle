<template>
  <div class="document-navigator">
    <div class="header">
      <h3 class="title">Document Navigator</h3>
      <span v-if="paragraphs.length" class="count">
        {{ paragraphs.length }} paragraphs
      </span>
    </div>
    <div class="content">
      <div v-if="loading" class="loading">Loading paragraphs...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="paragraphs.length === 0" class="empty">
        No paragraphs available
      </div>
      <ul v-else class="paragraph-list">
        <li
          v-for="para in paragraphs"
          :key="para.id"
          @click="selectParagraph(para)"
          :class="['paragraph-item', { active: isSelected(para.id), modified: isModified(para) }]"
        >
          <div class="paragraph-header">
            <span class="paragraph-id">{{ para.paragraph_id }}</span>
            <span v-if="para.status === 'approved'" class="status-badge approved">✓</span>
            <span v-else-if="para.status === 'in_progress'" class="status-badge in-progress">•</span>
          </div>
          <div class="paragraph-preview">{{ getPreview(para.text) }}</div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
/**
 * DocumentNavigator Component (docnav1)
 *
 * Displays JSON document structure and allows navigation.
 * Shows paragraphs list with status indicators.
 * Clicking items loads corresponding paragraph.
 *
 * Phase 3: Full implementation with paragraph list
 */

import type { ParagraphCorrection } from '@/services/api'

export default {
  name: 'DocumentNavigator',
  props: {
    paragraphs: {
      type: Array as () => ParagraphCorrection[],
      default: () => []
    },
    selectedParagraphId: {
      type: Number,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    }
  },
  emits: ['select'],
  methods: {
    selectParagraph(paragraph: ParagraphCorrection) {
      this.$emit('select', paragraph)
    },
    isSelected(id: number): boolean {
      return this.selectedParagraphId === id
    },
    isModified(paragraph: ParagraphCorrection): boolean {
      return paragraph.status === 'in_progress' || paragraph.status === 'approved'
    },
    getPreview(text: string): string {
      if (!text) return '(empty)'
      return text.length > 60 ? text.substring(0, 60) + '...' : text
    }
  }
}
</script>

<style scoped>
.document-navigator {
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
  background: #f9fafb;
  border-bottom: 1px solid #d1d5db;
}

.title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.count {
  font-size: 0.875rem;
  color: #6b7280;
}

.content {
  flex: 1;
  overflow-y: auto;
}

.loading,
.error,
.empty {
  padding: 2rem 1rem;
  text-align: center;
  color: #6b7280;
}

.error {
  color: #dc2626;
}

.paragraph-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.paragraph-item {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  transition: background 0.15s;
}

.paragraph-item:hover {
  background: #f9fafb;
}

.paragraph-item.active {
  background: #eff6ff;
  border-left: 3px solid #3b82f6;
}

.paragraph-item.modified {
  border-left: 3px solid #10b981;
}

.paragraph-item.active.modified {
  border-left: 3px solid #3b82f6;
}

.paragraph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
}

.paragraph-id {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  font-family: monospace;
}

.status-badge {
  font-size: 0.75rem;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-weight: 500;
}

.status-badge.approved {
  background: #dcfce7;
  color: #166534;
}

.status-badge.in-progress {
  background: #fef3c7;
  color: #92400e;
}

.paragraph-preview {
  font-size: 0.875rem;
  color: #4b5563;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
