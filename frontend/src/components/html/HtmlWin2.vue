<template>
  <div class="html-window-container bg-green-100 border-2 border-green-500 p-4">
    <div class="html-window-header bg-yellow-100 p-2 mb-2">
      <h3 class="text-lg font-bold text-black">🟢 HTML Window 2 - Basic1 Component Loaded!</h3>
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
  return `${props.baseUrl}/basic1.html`
})

// Methods
const onFrameLoad = () => {
  isLoaded.value = true
  console.log('HtmlWin2: basic1.html loaded successfully')

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
  console.error('HtmlWin2: Error loading basic1.html:', error)
}

const testClick = () => {
  alert('HtmlWin2 component is working!')
  console.log('HtmlWin2: Test button clicked')
}

// Lifecycle
onMounted(() => {
  console.log('HtmlWin2: Component mounted, loading basic1.html')
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