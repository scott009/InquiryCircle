<template>
  <div class="corrected-text-editor">
    <!-- Editable textarea for corrected translation -->
    <p>CorrectedTextEditor Component - Phase 1 Stub</p>
    <textarea disabled placeholder="Corrected translation will be editable here"></textarea>
    <button disabled>Save</button>
  </div>
</template>

<script>
/**
 * CorrectedTextEditor Component (corrected1)
 *
 * Editable textarea for human-corrected translation.
 * Displays and edits 'corrected_<language>_text' field.
 * Save button persists changes to backend.
 *
 * Status: Stub/Foundation (Phase 1)
 * TODO: Implement in Phase 3
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
    }
  }
}
</script>

<style scoped>
.corrected-text-editor {
  padding: 1rem;
  border: 1px solid #ccc;
}

textarea {
  width: 100%;
  min-height: 150px;
  margin: 0.5rem 0;
}

button {
  padding: 0.5rem 1rem;
  background: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
