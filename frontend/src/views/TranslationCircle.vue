<template>
  <div class="translation-circle">
    <h1>Translation Circle - Phase 1 Stub</h1>
    <p>This route will compose the 4 translation components with video integration.</p>

    <!-- 4-Window Layout (stubs not imported yet) -->
    <div class="placeholder-grid">
      <div class="placeholder">EnglishTextDisplay (engtxt1)</div>
      <div class="placeholder">AITranslationDisplay (aitrans1)</div>
      <div class="placeholder">CorrectedTextEditor (corrected1)</div>
      <div class="placeholder">DocumentNavigator (docnav1)</div>
    </div>
  </div>
</template>

<script>
/**
 * TranslationCircle View
 *
 * Main route for collaborative translation editing circles.
 * Composes 4 translation-specific display elements:
 * - engtxt1: English source text (read-only)
 * - aitrans1: AI translation (read-only)
 * - corrected1: Corrected translation (editable)
 * - docnav1: Document navigation
 *
 * Will also include shared elements:
 * - jitsiwin1: Video conferencing (Phase 5)
 * - topbar1: Navigation and user info
 * - Optional: reaction bars, status displays
 *
 * Status: Stub/Foundation (Phase 1)
 * TODO Phase 3: Import and wire up translation components
 * TODO Phase 4: Add circle authentication and membership
 * TODO Phase 5: Add Jitsi video integration
 * TODO Phase 6: Add facilitator controls
 */

export default {
  name: 'TranslationCircle',
  components: {
    // Components will be imported in Phase 3
    // EnglishTextDisplay,
    // AITranslationDisplay,
    // CorrectedTextEditor,
    // DocumentNavigator,
  },
  data() {
    return {
      circleId: null,
      documentId: null,
      currentParagraph: null,
      targetLanguage: 'thai'
    }
  },
  mounted() {
    // Will load circle and document data in Phase 4
    console.log('TranslationCircle view loaded (stub)')
  }
}
</script>

<style scoped>
.translation-circle {
  padding: 2rem;
}

.placeholder-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 2rem;
}

.placeholder {
  padding: 2rem;
  border: 2px dashed #ccc;
  background: #f9f9f9;
  text-align: center;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
