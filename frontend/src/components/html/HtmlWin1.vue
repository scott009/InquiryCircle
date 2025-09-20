<template>
  <div class="html-window-container">
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


// Lifecycle
onMounted(() => {
  console.log('HtmlWin1: Component mounted, loading ring14web.html')
})
</script>

<style scoped>
.html-window-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.html-frame {
  width: 100%;
  height: 100%;
  border: none;
}
</style>