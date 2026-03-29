<template>
  <div class="verdict-section">
    <p class="verdict-prompt">⚖️ 财神爷已审判完毕，你的选择是？</p>
    <div class="verdict-btns">
      <button class="btn-save" @click="$emit('decision', 'save')">
        ✅ 我悟了，不买了
      </button>
      <button
        class="btn-clown"
        ref="clownBtn"
        :disabled="countdown > 0"
        @mouseenter="handleHover"
        @click="handleClownClick"
      >
        <span v-if="countdown > 0">🔒 财神爷锁定中 {{ countdown }}s</span>
        <span v-else>🤡 我是小丑，还要买</span>
      </button>
    </div>
    <p v-if="countdown > 0" class="lock-tip">财神爷锁死了你的按钮，让你再冷静 {{ countdown }} 秒</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['decision'])

const clownBtn = ref(null)
const countdown = ref(0)
const hasEscaped = ref(false)

function handleHover() {
  if (hasEscaped.value || countdown.value > 0) return
  hasEscaped.value = true
  const dx = (Math.random() - 0.5) * 200
  const dy = (Math.random() - 0.5) * 80
  if (clownBtn.value) {
    clownBtn.value.style.transform = `translate(${dx}px, ${dy}px)`
    setTimeout(() => {
      if (clownBtn.value) clownBtn.value.style.transform = ''
      startCountdown()
    }, 400)
  }
}

function startCountdown() {
  countdown.value = 3
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
      hasEscaped.value = false
    }
  }, 1000)
}

function handleClownClick() {
  if (countdown.value > 0) return
  if (clownBtn.value) {
    clownBtn.value.classList.add('shake')
    setTimeout(() => clownBtn.value?.classList.remove('shake'), 500)
  }
  setTimeout(() => emit('decision', 'buy'), 300)
}
</script>

<style scoped>
.verdict-section {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.verdict-prompt {
  text-align: center;
  color: #a0c4ae;
  font-size: 14px;
}

.verdict-btns {
  display: flex;
  gap: 12px;
}

.btn-save, .btn-clown {
  flex: 1;
  padding: 16px;
  font-size: 16px;
  font-weight: 700;
  font-family: inherit;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.4s cubic-bezier(.36,.07,.19,.97), box-shadow 0.2s;
}

.btn-save {
  background: linear-gradient(135deg, #00D68F, #00B377);
  color: #0A1510;
}

.btn-save:hover {
  box-shadow: 0 0 20px rgba(0, 214, 143, 0.5);
  transform: translateY(-2px);
}

.btn-clown {
  background: rgba(255,255,255,0.08);
  color: #a0a0a0;
  border: 1px solid rgba(255,255,255,0.1);
}

.btn-clown:not(:disabled):hover {
  background: rgba(255,68,68,0.1);
  border-color: rgba(255,68,68,0.3);
}

.btn-clown:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-clown.shake {
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%       { transform: translateX(-8px); }
  40%       { transform: translateX(8px); }
  60%       { transform: translateX(-8px); }
  80%       { transform: translateX(8px); }
}

.lock-tip {
  text-align: center;
  font-size: 12px;
  color: #FFD700;
  opacity: 0.8;
}
</style>
