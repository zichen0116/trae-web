<template>
  <div class="app">
    <WalletHPBar :price="Number(form.price) || 0" />
    <HeroSection />
    <main class="main-content">
      <PersonaSelector v-model="form.persona" />
      <UploadZone v-model="form.imageBase64" />
      <InputForm v-model="form" />
      <button
        class="summon-btn"
        :disabled="loading || !isFormValid"
        @click="handleSummon"
      >
        <span v-if="loading" class="spinner"></span>
        <span v-else>⚡ 呼叫财神爷 拷打我</span>
      </button>
      <ResultPanel
        v-if="result"
        :result="result"
        :price="Number(form.price)"
        @decision="handleDecision"
      />
      <MoneyRain v-if="showMoneyRain" :price="Number(form.price)" @close="showMoneyRain = false" />
      <ClownStamp v-if="showClownStamp" />
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import WalletHPBar from './components/WalletHPBar.vue'
import HeroSection from './components/HeroSection.vue'
import PersonaSelector from './components/PersonaSelector.vue'
import UploadZone from './components/UploadZone.vue'
import InputForm from './components/InputForm.vue'
import ResultPanel from './components/ResultPanel.vue'
import MoneyRain from './components/MoneyRain.vue'
import ClownStamp from './components/ClownStamp.vue'
import { playAudio } from './utils/audio'

const form = ref({
  product_name: '',
  reason: '',
  price: '',
  persona: 'caishen',
  imageBase64: '',
})

const loading = ref(false)
const result = ref(null)
const showMoneyRain = ref(false)
const showClownStamp = ref(false)

const isFormValid = computed(() =>
  form.value.product_name.trim() &&
  form.value.reason.trim() &&
  Number(form.value.price) > 0
)

async function handleSummon() {
  loading.value = true
  result.value = null
  showMoneyRain.value = false
  showClownStamp.value = false
  playAudio('bell')
  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        product_name: form.value.product_name,
        reason: form.value.reason,
        price: Number(form.value.price),
        persona: form.value.persona,
        image_base64: form.value.imageBase64,
      }),
    })
    if (!res.ok) throw new Error(await res.text())
    result.value = await res.json()
  } catch (e) {
    alert('财神爷暂时不在线，请重试：' + e.message)
  } finally {
    loading.value = false
  }
}

function handleDecision(choice) {
  if (choice === 'save') {
    showMoneyRain.value = true
    playAudio('kaching')
    setTimeout(() => { showMoneyRain.value = false }, 4000)
  } else {
    showClownStamp.value = true
    playAudio('clown')
  }
}
</script>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Noto Sans SC', sans-serif;
  background: #0A1510;
  color: #e8f5e9;
  min-height: 100vh;
}

.app {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

.main-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px 20px 60px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.summon-btn {
  width: 100%;
  padding: 18px;
  font-size: 20px;
  font-weight: 900;
  font-family: 'Noto Sans SC', sans-serif;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #00D68F, #00B377);
  color: #0A1510;
  cursor: pointer;
  transition: transform 0.1s, box-shadow 0.3s;
  box-shadow: 0 0 20px rgba(0, 214, 143, 0.4);
  animation: pulse-glow 2s infinite;
}

.summon-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 0 40px rgba(0, 214, 143, 0.7);
}

.summon-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  animation: none;
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(0, 214, 143, 0.4); }
  50% { box-shadow: 0 0 40px rgba(0, 214, 143, 0.8); }
}

.spinner {
  display: inline-block;
  width: 22px;
  height: 22px;
  border: 3px solid rgba(10,21,16,0.3);
  border-top-color: #0A1510;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  vertical-align: middle;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>
