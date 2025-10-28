<template>
  <div class="english-text-display">
    <div class="header">
      <h3 class="title">English Text</h3>
      <span v-if="paragraphId" class="paragraph-id">{{ paragraphId }}</span>
    </div>
    <div class="content">
      <p v-if="text" class="text">{{ text }}</p>
      <p v-else class="placeholder">No paragraph selected</p>
    </div>
  </div>
</template>

<script lang="ts">
/**
 * EnglishTextDisplay Component (engtxt1)
 *
 * Displays English source text from translation JSON.
 * Read-only display of the 'text' field.
 *
 * Phase 3: Full implementation with styling
 */

export default {
  name: 'EnglishTextDisplay',
  props: {
    text: {
      type: String,
      default: ''
    },
    paragraphId: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.english-text-display {
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
  background: #f3f4f6;
  border-bottom: 1px solid #d1d5db;
}

.title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.paragraph-id {
  font-size: 0.875rem;
  color: #6b7280;
  font-family: monospace;
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
