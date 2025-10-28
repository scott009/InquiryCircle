<template>
  <div class="document-navigator">
    <!-- JSON-based document structure navigation -->
    <p>DocumentNavigator Component - Phase 1 Stub</p>
    <ul>
      <li>Chapter 1</li>
      <li>Chapter 2</li>
      <li>...</li>
    </ul>
  </div>
</template>

<script>
/**
 * DocumentNavigator Component (docnav1)
 *
 * Displays JSON document structure and allows navigation.
 * Shows chapters, sections, paragraphs hierarchy.
 * Clicking items loads corresponding paragraph.
 *
 * Status: Stub/Foundation (Phase 1)
 * TODO: Implement in Phase 3
 */

export default {
  name: 'DocumentNavigator',
  props: {
    documentStructure: {
      type: Object,
      default: () => ({})
    }
  }
}
</script>

<style scoped>
.document-navigator {
  padding: 1rem;
  border: 1px solid #ccc;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  padding: 0.25rem 0;
  cursor: pointer;
}

li:hover {
  background: #f0f0f0;
}
</style>
