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


// Lifecycle
onMounted(() => {
  console.log('HtmlWin2: Component mounted, loading basic1.html')
})
</script>

<style scoped>
.html-window-container {
  width: 100%;
  height: 800px;
  position: relative;
}

.html-frame {
  width: 100%;
  height: 800px;
  border: none;
}
</style>