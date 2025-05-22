<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const BACKEND_HOST = '/api'

const providers = [
  { id: 'openai', name: 'OpenAI', models: [
    { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo' },
    { id: 'gpt-4', name: 'GPT-4' },
    { id: 'gpt-4-turbo', name: 'GPT-4 Turbo' }
  ]},
  { id: 'grok', name: 'Grok', models: [
    { id: 'grok-1', name: 'Grok-1' }
  ]},
  { id: 'deepseek', name: 'DeepSeek', models: [
    { id: 'deepseek-chat', name: 'DeepSeek Chat' }
  ]}
]

const selectedProvider = ref(providers[0].id)
const selectedModel = ref(providers[0].models[0].id)
const prompt = ref('')
const response = ref('')
const isLoading = ref(false)
const error = ref('')

const availableModels = computed(() => {
  const provider = providers.find(p => p.id === selectedProvider.value)
  return provider ? provider.models : []
})

const sendPrompt = async () => {
  if (!prompt.value.trim()) return
  
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await axios.post(`${BACKEND_HOST}/v1/chat/completions`, {
      model: selectedModel.value,
      provider: selectedProvider.value,
      messages: [{ role: 'user', content: prompt.value }]
    })
    
    response.value = response.data.choices[0].message.content
  } catch (err) {
    error.value = err.response?.data?.detail || 'An error occurred'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-center mb-8">AI Chat Interface</h1>
      
      <!-- Provider Selection -->
      <div class="mb-6 min-w-[400px]">
        <label class="block text-sm font-medium text-gray-700 mb-2">Select Provider</label>
        <select
          v-model="selectedProvider"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option v-for="provider in providers" :key="provider.id" :value="provider.id">
            {{ provider.name }}
          </option>
        </select>
      </div>

      <!-- Model Selection -->
      <div class="mb-6 min-w-[400px]">
        <label class="block text-sm font-medium text-gray-700 mb-2">Select Model</label>
        <select
          v-model="selectedModel"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option v-for="model in availableModels" :key="model.id" :value="model.id">
            {{ model.name }}
          </option>
        </select>
      </div>
      
      <!-- Prompt Input -->
      <div class="mb-6 min-w-[400px]">
        <label class="block text-sm font-medium text-gray-700 mb-2">Your Message</label>
        <textarea
          v-model="prompt"
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Type your message here..."
        ></textarea>
      </div>
      
      <!-- Submit Button -->
      <button
        @click="sendPrompt"
        :disabled="isLoading || !prompt.trim()"
        class="w-full min-w-[400px] bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ isLoading ? 'Sending...' : 'Send Message' }}
      </button>
      
      <!-- Error Message -->
      <div v-if="error" class="mt-4 p-4 min-w-[400px] bg-red-50 text-red-700 rounded-md">
        {{ error }}
      </div>
      
      <!-- Response -->
      <div v-if="response" class="mt-6 min-w-[400px]">
        <h2 class="text-lg font-medium text-gray-900 mb-2">Response</h2>
        <div class="p-4 bg-white border border-gray-200 rounded-md shadow-sm">
          {{ response }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
