<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50" @click="$emit('close')">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
      <div class="mt-3">
        <!-- Header -->
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            Create New Circle
          </h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">
              Circle Name
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              placeholder="Enter circle name"
              :disabled="isSubmitting"
            />
          </div>

          <div>
            <label for="description" class="block text-sm font-medium text-gray-700">
              Description (Optional)
            </label>
            <textarea
              id="description"
              v-model="form.description"
              rows="3"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              placeholder="Describe the purpose or topic of this circle"
              :disabled="isSubmitting"
            ></textarea>
          </div>

          <!-- Error message -->
          <div v-if="error" class="rounded-md bg-red-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">Error</h3>
                <div class="mt-2 text-sm text-red-700">{{ error }}</div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="$emit('close')"
              class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              :disabled="isSubmitting"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="isSubmitting || !form.name.trim()"
              class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isSubmitting ? 'Creating...' : 'Create Circle' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { apiService, type Circle } from '@/services/api'

const emit = defineEmits<{
  close: []
  created: [circle: Circle]
}>()

const form = reactive({
  name: '',
  description: ''
})

const isSubmitting = ref(false)
const error = ref<string | null>(null)

const handleSubmit = async () => {
  if (!form.name.trim()) return

  isSubmitting.value = true
  error.value = null

  try {
    const newCircle = await apiService.createCircle({
      name: form.name.trim(),
      description: form.description.trim() || undefined
    })

    emit('created', newCircle)
  } catch (err: any) {
    error.value = err.response?.data?.error || err.message || 'Failed to create circle'
  } finally {
    isSubmitting.value = false
  }
}
</script>