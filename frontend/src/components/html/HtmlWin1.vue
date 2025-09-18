<template>
  <div class="html-window-container bg-red-100 border-2 border-red-500 p-4">
    <div class="html-window-header bg-yellow-100 p-2 mb-2">
      <h3 class="text-lg font-bold text-black">🟢 HTML Window 1 - Ring14Web Component Loaded!</h3>
      <p class="text-sm text-gray-700">Loading URL: {{ htmlUrl }}</p>
      <p class="text-sm font-bold" :class="isLoaded ? 'text-green-600' : 'text-red-600'">
        Iframe Status: {{ isLoaded ? '✅ Loaded' : '⏳ Loading...' }}
      </p>
      <button @click="testClick" class="bg-blue-500 text-white px-2 py-1 text-xs">Test Click</button>
    </div>
    <div class="html-window-content bg-blue-100 border border-blue-300">
      <iframe
        ref="htmlFrame"
        :src="htmlUrl"
        class="html-frame"
        @load="onFrameLoad"
        @error="onFrameError"
        frameborder="0"
        sandbox="allow-same-origin allow-scripts"
      ></iframe>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

// Props
interface Props {
  baseUrl?: string
}

const props = withDefaults(defineProps<Props>(), {
  baseUrl: window.location.origin
})

// Refs
const htmlFrame = ref<HTMLIFrameElement | null>(null)
const isLoaded = ref(false)

// Computed
const htmlUrl = computed(() => {
  return `${props.baseUrl}/ring14web.html`
})

// Methods
const onFrameLoad = () => {
  isLoaded.value = true
  console.log('HtmlWin1: ring14web.html loaded successfully')

  // Apply ada3.css stylesheet to the iframe content
  if (htmlFrame.value?.contentDocument) {
    const doc = htmlFrame.value.contentDocument
    const link = doc.createElement('link')
    link.rel = 'stylesheet'
    link.href = `${props.baseUrl}/ada3.css`
    doc.head?.appendChild(link)
  }
}

const onFrameError = (error: any) => {
  console.error('HtmlWin1: Error loading ring14web.html:', error)
}

const testClick = () => {
  alert('HtmlWin1 component is working!')
  console.log('HtmlWin1: Test button clicked')
}

// Lifecycle
onMounted(() => {
  console.log('HtmlWin1: Component mounted, loading ring14web.html')
})
</script>

<style scoped>
.html-window-container {
  @apply bg-white shadow overflow-hidden rounded-lg;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.html-window-header {
  @apply px-4 py-3 border-b border-gray-200 bg-gray-50;
  flex-shrink: 0;
}

.html-window-content {
  @apply flex-1;
  min-height: 400px;
}

.html-frame {
  width: 100%;
  height: 100%;
  border: none;
}
</style>