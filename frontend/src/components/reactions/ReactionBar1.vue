<template>
  <div class="reaction-bar bg-white border-2 border-gray-300 rounded-lg p-4">
    <!-- Horizontal Layout: Buttons in a row with radio controls below each -->
    <div class="grid grid-cols-12 gap-2">
      <!-- Like (like1) - 3 options -->
      <div class="flex flex-col gap-1">
        <button
          id="like1"
          @click="toggleReaction('like')"
          :class="['reaction-btn', reactionStates.like ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Like
        </button>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="like-mode" value="credited" v-model="reactionModes.like" class="mr-1" />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Credited</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="like-mode" value="secret" v-model="reactionModes.like" class="mr-1" />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="like-mode" value="anon" v-model="reactionModes.like" class="mr-1" />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
        </div>
      </div>

      <!-- Love (love1) - 3 options -->
      <div class="flex flex-col gap-1">
        <button
          id="love1"
          @click="toggleReaction('love')"
          :class="['reaction-btn', reactionStates.love ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Love
        </button>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="love-mode" value="credited" v-model="reactionModes.love" class="mr-1 " />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Credited</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="love-mode" value="secret" v-model="reactionModes.love" class="mr-1 " />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="love-mode" value="anon" v-model="reactionModes.love" class="mr-1 " />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
        </div>
      </div>

      <!-- Dislike (dislike1) - 3 options -->
      <div class="flex flex-col gap-1">
        <button
          id="dislike1"
          @click="toggleReaction('dislike')"
          :class="['reaction-btn', reactionStates.dislike ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Dislike
        </button>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="dislike-mode" value="credited" v-model="reactionModes.dislike" class="mr-1 " />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Credited</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="dislike-mode" value="secret" v-model="reactionModes.dislike" class="mr-1 " />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="dislike-mode" value="anon" v-model="reactionModes.dislike" class="mr-1 " />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
        </div>
      </div>

      <!-- Hate (hate1) - 3 options -->
      <div class="flex flex-col gap-1">
        <button
          id="hate1"
          @click="toggleReaction('hate')"
          :class="['reaction-btn', reactionStates.hate ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Hate
        </button>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="hate-mode" value="credited" v-model="reactionModes.hate" class="mr-1 " />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Credited</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="hate-mode" value="secret" v-model="reactionModes.hate" class="mr-1 " />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="hate-mode" value="anon" v-model="reactionModes.hate" class="mr-1 " />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
        </div>
      </div>

      <!-- Agree (agree1) - 3 options -->
      <div class="flex flex-col gap-1">
        <button
          id="agree1"
          @click="toggleReaction('agree')"
          :class="['reaction-btn', reactionStates.agree ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Agree
        </button>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="agree-mode" value="credited" v-model="reactionModes.agree" class="mr-1 " />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Credited</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="agree-mode" value="secret" v-model="reactionModes.agree" class="mr-1 " />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="agree-mode" value="anon" v-model="reactionModes.agree" class="mr-1 " />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
        </div>
      </div>

      <!-- Disagree (disagree1) - 3 options -->
      <div class="flex flex-col gap-1">
        <button
          id="disagree1"
          @click="toggleReaction('disagree')"
          :class="['reaction-btn', reactionStates.disagree ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Disagree
        </button>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="disagree-mode" value="credited" v-model="reactionModes.disagree" class="mr-1 " />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Credited</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="disagree-mode" value="secret" v-model="reactionModes.disagree" class="mr-1 " />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="disagree-mode" value="anon" v-model="reactionModes.disagree" class="mr-1 " />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
        </div>
      </div>

      <!-- Hurry Up (hurryup1) - 2 options -->
      <div class="flex flex-col gap-1">
        <button
          id="hurryup1"
          @click="toggleReaction('hurryup')"
          :class="['reaction-btn', reactionStates.hurryup ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Hurry Up
        </button>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="hurryup-mode" value="secret" v-model="reactionModes.hurryup" class="mr-1 " />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="hurryup-mode" value="anon" v-model="reactionModes.hurryup" class="mr-1 " />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
        </div>
      </div>

      <!-- Go on (goon1) - 2 options -->
      <div class="flex flex-col gap-1">
        <button
          id="goon1"
          @click="toggleReaction('goon')"
          :class="['reaction-btn', reactionStates.goon ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Go on
        </button>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="goon-mode" value="secret" v-model="reactionModes.goon" class="mr-1 " />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
          <label class="flex items-center cursor-pointer text-sm">
            <input type="radio" name="goon-mode" value="anon" v-model="reactionModes.goon" class="mr-1 " />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
        </div>
      </div>

      <!-- Interesting (interest1) - Secret only -->
      <div class="flex flex-col gap-1">
        <button
          id="interest1"
          @click="toggleReaction('interesting')"
          :class="['reaction-btn', reactionStates.interesting ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Interesting
        </button>
        <div class="flex items-center justify-center pt-1">
          <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
        </div>
      </div>

      <!-- Boring (boring1) - Secret only -->
      <div class="flex flex-col gap-1">
        <button
          id="boring1"
          @click="toggleReaction('boring')"
          :class="['reaction-btn', reactionStates.boring ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Boring
        </button>
        <div class="flex items-center justify-center pt-1">
          <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
        </div>
      </div>

      <!-- Sympathy (sympathy1) - Anon only (CORRECTED) -->
      <div class="flex flex-col gap-1">
        <button
          id="sympathy1"
          @click="toggleReaction('sympathy')"
          :class="['reaction-btn', reactionStates.sympathy ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Sympathy
        </button>
        <div class="flex items-center justify-center pt-1">
          <span class="px-2 py-1 bg-teal-500 text-white rounded text-sm">Anon</span>
        </div>
      </div>

      <!-- Laugh (laugh1) - Anon only (CORRECTED) -->
      <div class="flex flex-col gap-1">
        <button
          id="laugh1"
          @click="toggleReaction('laugh')"
          :class="['reaction-btn', reactionStates.laugh ? 'bg-blue-600' : 'bg-blue-400', 'hover:bg-blue-500', 'text-white', 'font-semibold', 'py-2', 'px-2', 'rounded', 'text-sm']"
        >
          Laugh
        </button>
        <div class="flex items-center justify-center pt-1">
          <span class="px-2 py-1 bg-teal-500 text-white rounded text-sm">Anon</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

// Reaction button states (all start as off/false)
const reactionStates = reactive({
  like: false,
  love: false,
  dislike: false,
  hate: false,
  agree: false,
  disagree: false,
  hurryup: false,
  goon: false,
  interesting: false,
  boring: false,
  sympathy: false,
  laugh: false
})

// Reaction mode states (individual radio button choices per reaction)
const reactionModes = reactive({
  like: 'credited',
  love: 'credited',
  dislike: 'credited',
  hate: 'credited',
  agree: 'credited',
  disagree: 'credited',
  hurryup: 'secret',     // Default to secret (2 options)
  goon: 'secret',        // Default to secret (2 options)
  interesting: 'secret', // Fixed as secret
  boring: 'secret',      // Fixed as secret
  sympathy: 'anon',      // Fixed as anon (CORRECTED)
  laugh: 'anon'          // Fixed as anon (CORRECTED)
})

// Toggle reaction on/off
const toggleReaction = (reactionType: string) => {
  // Toggle the state
  reactionStates[reactionType as keyof typeof reactionStates] = !reactionStates[reactionType as keyof typeof reactionStates]

  const isOn = reactionStates[reactionType as keyof typeof reactionStates]
  const mode = reactionModes[reactionType as keyof typeof reactionModes]

  console.log(`Reaction ${reactionType}: ${isOn ? 'ON' : 'OFF'} with mode: ${mode}`)

  // TODO: Integrate with WebSocket or API to send reaction state and mode
  // This will eventually call the backend reactions.py classes
}
</script>

<style scoped>
.reaction-btn {
  min-width: 60px;
  transition: all 0.2s;
}

.reaction-btn:active {
  transform: scale(0.95);
}
</style>
