<template>
  <div id="descbar1" class="description-bar bg-gray-50 p-4">
    <!-- Empty State -->
    <div v-if="!selectedElement" class="empty-state text-gray-600 text-sm">
      <span class="font-mono text-xs text-gray-400">{{ descriptions.defaultMessage.id }}</span>
      <p class="mt-1">{{ descriptions.defaultMessage.text }}</p>
    </div>

    <!-- Element Description Display -->
    <div v-else-if="currentDescription" class="element-description">
      <!-- Header with Label and ID -->
      <div class="description-header mb-2 pb-2 border-b border-gray-300">
        <h3 class="text-lg font-semibold text-gray-800">{{ currentDescription.label }}</h3>
        <span class="font-mono text-xs text-gray-500">{{ currentDescription.id }}</span>
      </div>

      <!-- Description Content -->
      <div class="description-content">
        <p class="text-sm text-gray-700">{{ currentDescription.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// Type definitions
interface ElementDescription {
  label: string
  id: string
  description: string
}

interface Descriptions {
  defaultMessage: {
    id: string
    text: string
  }
  elements: Record<string, ElementDescription>
}

// Reactive state
const descriptions = ref<Descriptions>({
  defaultMessage: {
    id: 'descbar-empty-state',
    text: 'Click an element to see what it does'
  },
  elements: {}
})

const selectedElement = ref<string | null>(null)

// Computed property for current description
const currentDescription = computed(() => {
  if (!selectedElement.value) return null
  return descriptions.value.elements[selectedElement.value] || null
})

// Load descriptions from JSON
const loadDescriptions = async () => {
  try {
    const response = await fetch('/data/element-descriptions.json')
    if (response.ok) {
      descriptions.value = await response.json()
      console.log('✅ Loaded element descriptions:', Object.keys(descriptions.value.elements).length, 'elements')
    } else {
      console.error('❌ Failed to load element descriptions:', response.status)
    }
  } catch (error) {
    console.error('❌ Error loading element descriptions:', error)
  }
}

// Handle element click from global event bus
const handleElementClick = (elementId: string) => {
  // Toggle behavior: if clicking the same element, clear it
  if (selectedElement.value === elementId) {
    selectedElement.value = null
  } else {
    selectedElement.value = elementId
  }
  console.log('DescBar1: Selected element:', selectedElement.value)
}

// Expose handler to parent components via window global
// This allows ReactionBar1/ReactionBar2 to notify DescBar1 of clicks
onMounted(() => {
  loadDescriptions()

  // Register global handler
  ;(window as any).descBarHandler = handleElementClick
  console.log('✅ DescBar1 mounted and ready')
})
</script>

<style scoped>
.description-bar {
  min-height: 120px;
  max-height: 200px;
  overflow-y: auto;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100px;
}

.description-header h3 {
  margin: 0;
}

.description-content {
  line-height: 1.6;
}
</style>
