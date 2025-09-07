<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4">
      <div class="mb-6">
        <router-link 
          to="/" 
          class="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium"
        >
          ← Back to Dashboard
        </router-link>
      </div>

      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">API Client Test</h1>
        <p class="text-gray-600 mt-2">Test the API client connection to Django backend</p>
      </div>

      <!-- Connection Status -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Connection Test</h2>
        <div class="flex items-center space-x-4">
          <button
            @click="testConnection"
            :disabled="isLoading"
            class="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {{ isLoading ? 'Testing...' : 'Test Connection' }}
          </button>
          
          <div v-if="connectionStatus !== null" class="flex items-center">
            <div 
              :class="connectionStatus ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" 
              class="px-3 py-1 rounded-full text-sm font-medium"
            >
              {{ connectionStatus ? '✅ Connected' : '❌ Failed' }}
            </div>
          </div>
        </div>
      </div>

      <!-- Health Check -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Health Check</h2>
        <button
          @click="performHealthCheck"
          :disabled="isLoading"
          class="bg-green-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 transition-colors mb-4"
        >
          {{ isLoading ? 'Checking...' : 'Check Health' }}
        </button>
        
        <div v-if="healthData" class="bg-gray-50 p-4 rounded-lg">
          <pre class="text-sm">{{ JSON.stringify(healthData, null, 2) }}</pre>
        </div>
      </div>

      <!-- Key Verification Test -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Key Verification Test</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Access Key (optional - for testing)
            </label>
            <input
              v-model="testKey"
              type="text"
              placeholder="Enter access key to test verification"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            @click="verifyKey"
            :disabled="isLoading || !testKey.trim()"
            class="bg-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-700 disabled:opacity-50 transition-colors"
          >
            {{ isLoading ? 'Verifying...' : 'Verify Key' }}
          </button>
          
          <div v-if="keyVerificationResult" class="bg-gray-50 p-4 rounded-lg">
            <pre class="text-sm">{{ JSON.stringify(keyVerificationResult, null, 2) }}</pre>
          </div>
        </div>
      </div>

      <!-- Circles Test -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Circles API Test</h2>
        <button
          @click="fetchCircles"
          :disabled="isLoading"
          class="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors mb-4"
        >
          {{ isLoading ? 'Loading...' : 'Get Circles' }}
        </button>
        
        <div v-if="circles" class="bg-gray-50 p-4 rounded-lg">
          <pre class="text-sm">{{ JSON.stringify(circles, null, 2) }}</pre>
        </div>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error</h3>
            <p class="text-sm text-red-700 mt-1">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- API Logs -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">API Logs</h2>
        <p class="text-sm text-gray-600 mb-4">Check the browser console for detailed API request/response logs</p>
        <button
          @click="clearLogs"
          class="bg-gray-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-700 transition-colors"
        >
          Clear Console
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { apiService, type AuthResponse, type CirclesResponse } from '../services/api';

// Reactive state
const isLoading = ref(false);
const connectionStatus = ref<boolean | null>(null);
const healthData = ref<{ status: string; database: string } | null>(null);
const testKey = ref('');
const keyVerificationResult = ref<AuthResponse | null>(null);
const circles = ref<CirclesResponse | null>(null);
const error = ref('');

// Test connection
const testConnection = async () => {
  isLoading.value = true;
  error.value = '';
  try {
    const connected = await apiService.testConnection();
    connectionStatus.value = connected;
  } catch (err) {
    connectionStatus.value = false;
    error.value = apiService.getErrorMessage(err);
  } finally {
    isLoading.value = false;
  }
};

// Health check
const performHealthCheck = async () => {
  isLoading.value = true;
  error.value = '';
  try {
    const health = await apiService.healthCheck();
    healthData.value = health;
    connectionStatus.value = true;
  } catch (err) {
    error.value = apiService.getErrorMessage(err);
    connectionStatus.value = false;
  } finally {
    isLoading.value = false;
  }
};

// Verify key
const verifyKey = async () => {
  isLoading.value = true;
  error.value = '';
  try {
    const result = await apiService.verifyKey(testKey.value);
    keyVerificationResult.value = result;
  } catch (err) {
    error.value = apiService.getErrorMessage(err);
  } finally {
    isLoading.value = false;
  }
};

// Fetch circles
const fetchCircles = async () => {
  isLoading.value = true;
  error.value = '';
  try {
    const result = await apiService.getCircles();
    circles.value = result;
  } catch (err) {
    error.value = apiService.getErrorMessage(err);
  } finally {
    isLoading.value = false;
  }
};

// Clear console logs
const clearLogs = () => {
  console.clear();
};
</script>