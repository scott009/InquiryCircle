<template>
  <div class="reaction-bar bg-white border-2 border-gray-300 rounded-lg p-4">
    <!-- Horizontal Layout: Labels in a row with checkboxes below each -->
    <div class="grid grid-cols-12 gap-2">
      <!-- Like (like_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Like</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-like"
              type="checkbox"
              v-model="reactionSettings.like.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-like"
              type="checkbox"
              v-model="reactionSettings.like.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-like"
              type="checkbox"
              v-model="reactionSettings.like.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Love (love_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Love</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-love"
              type="checkbox"
              v-model="reactionSettings.love.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-love"
              type="checkbox"
              v-model="reactionSettings.love.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-love"
              type="checkbox"
              v-model="reactionSettings.love.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Dislike (dislike_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Dislike</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-dislike"
              type="checkbox"
              v-model="reactionSettings.dislike.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-dislike"
              type="checkbox"
              v-model="reactionSettings.dislike.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-dislike"
              type="checkbox"
              v-model="reactionSettings.dislike.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Hate (hate_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Hate</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-hate"
              type="checkbox"
              v-model="reactionSettings.hate.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-hate"
              type="checkbox"
              v-model="reactionSettings.hate.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-hate"
              type="checkbox"
              v-model="reactionSettings.hate.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Agree (agreel1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Agree</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-agree"
              type="checkbox"
              v-model="reactionSettings.agree.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-agree"
              type="checkbox"
              v-model="reactionSettings.agree.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-agree"
              type="checkbox"
              v-model="reactionSettings.agree.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Disagree (disagree_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Disagree</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-disagree"
              type="checkbox"
              v-model="reactionSettings.disagree.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-disagree"
              type="checkbox"
              v-model="reactionSettings.disagree.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-disagree"
              type="checkbox"
              v-model="reactionSettings.disagree.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Hurry Up (hurryup_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Hurry Up</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-hurryup"
              type="checkbox"
              v-model="reactionSettings.hurryup.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-hurryup"
              type="checkbox"
              v-model="reactionSettings.hurryup.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-hurryup"
              type="checkbox"
              v-model="reactionSettings.hurryup.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Go on (goon_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Go on</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-goon"
              type="checkbox"
              v-model="reactionSettings.goon.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-goon"
              type="checkbox"
              v-model="reactionSettings.goon.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-goon"
              type="checkbox"
              v-model="reactionSettings.goon.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Interesting (interest_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Interesting</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-interesting"
              type="checkbox"
              v-model="reactionSettings.interesting.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-interesting"
              type="checkbox"
              v-model="reactionSettings.interesting.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-interesting"
              type="checkbox"
              v-model="reactionSettings.interesting.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Boring (boring_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Boring</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-boring"
              type="checkbox"
              v-model="reactionSettings.boring.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-boring"
              type="checkbox"
              v-model="reactionSettings.boring.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-boring"
              type="checkbox"
              v-model="reactionSettings.boring.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Sympathy (sympathy_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Sympathy</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-sympathy"
              type="checkbox"
              v-model="reactionSettings.sympathy.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-sympathy"
              type="checkbox"
              v-model="reactionSettings.sympathy.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-sympathy"
              type="checkbox"
              v-model="reactionSettings.sympathy.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>

      <!-- Laugh (laugh_l1) -->
      <div class="flex flex-col gap-1">
        <div class="text-center font-semibold text-sm py-2">Laugh</div>
        <div class="flex flex-col gap-1">
          <label class="flex items-center cursor-pointer">
            <input
              id="rch1-laugh"
              type="checkbox"
              v-model="reactionSettings.laugh.public"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-green-500 text-white rounded text-sm">Public</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch2-laugh"
              type="checkbox"
              v-model="reactionSettings.laugh.anon"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-blue-500 text-white rounded text-sm">Anon</span>
          </label>
          <label class="flex items-center cursor-pointer">
            <input
              id="rch3-laugh"
              type="checkbox"
              v-model="reactionSettings.laugh.secret"
              class="mr-2"
            />
            <span class="px-2 py-1 bg-red-600 text-white rounded text-sm">Secret</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'

// Reaction settings state (checkboxes for each reaction type)
const reactionSettings = reactive({
  like: { public: true, anon: false, secret: false },
  love: { public: true, anon: false, secret: false },
  dislike: { public: true, anon: false, secret: false },
  hate: { public: true, anon: false, secret: false },
  agree: { public: true, anon: false, secret: false },
  disagree: { public: true, anon: false, secret: false },
  hurryup: { public: true, anon: false, secret: false },
  goon: { public: true, anon: false, secret: false },
  interesting: { public: true, anon: false, secret: false },
  boring: { public: true, anon: false, secret: false },
  sympathy: { public: true, anon: false, secret: false },
  laugh: { public: true, anon: false, secret: false }
})

// Watch for changes and log (placeholder for future backend integration)
watch(reactionSettings, (newSettings) => {
  console.log('Reaction settings updated:', newSettings)
  // TODO: Send settings to backend to configure reaction visibility
}, { deep: true })
</script>

<style scoped>
/* Additional styles if needed */
</style>
