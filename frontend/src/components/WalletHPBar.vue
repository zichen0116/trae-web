<template>
  <div class="hp-bar-container" :class="{ shake: isShaking }">
    <div class="hp-bar-inner">
      <span class="hp-label">💰 钱包HP</span>
      <div class="hp-track">
        <div
          class="hp-fill"
          :style="{ width: hpPercent + '%', background: hpColor }"
        ></div>
      </div>
      <span class="hp-text" :style="{ color: hpColor }">{{ hpPercent }}%</span>
    </div>
    <div v-if="damageText" class="damage-popup">{{ damageText }}</div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  price: { type: Number, default: 0 },
})

const isShaking = ref(false)
const damageText = ref('')

// 价格越高，HP越低（最大参考价格5000元）
const hpPercent = computed(() => {
  const p = Math.min(props.price, 5000)
  return Math.max(0, Math.round(100 - (p / 5000) * 90))
})

const hpColor = computed(() => {
  if (hpPercent.value > 60) return '#00D68F'
  if (hpPercent.value > 30) return '#FFD700'
  return '#FF4444'
})

watch(() => props.price, (newVal, oldVal) => {
  if (newVal > 500 && newVal > oldVal) {
    isShaking.value = true
    damageText.value = `-${Math.round((newVal - oldVal) * 0.1) || '??'} HP`
    setTimeout(() => { isShaking.value = false }, 600)
    setTimeout(() => { damageText.value = '' }, 1200)
  }
})
</script>

<style scoped>
.hp-bar-container {
  position: fixed;
  top: 16px;
  right: 20px;
  z-index: 1000;
  background: rgba(10, 21, 16, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 214, 143, 0.2);
  border-radius: 10px;
  padding: 8px 14px;
  min-width: 200px;
}

.hp-bar-inner {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hp-label {
  font-size: 12px;
  white-space: nowrap;
  color: #a0c4ae;
}

.hp-track {
  flex: 1;
  height: 10px;
  background: rgba(255,255,255,0.1);
  border-radius: 5px;
  overflow: hidden;
}

.hp-fill {
  height: 100%;
  border-radius: 5px;
  transition: width 0.4s ease, background 0.4s ease;
}

.hp-text {
  font-size: 12px;
  font-weight: 700;
  min-width: 34px;
  text-align: right;
}

.damage-popup {
  text-align: right;
  font-size: 13px;
  font-weight: 700;
  color: #FF4444;
  animation: float-up 1.2s ease forwards;
}

@keyframes float-up {
  0%   { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-20px); }
}

.shake {
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%       { transform: translateX(-4px); }
  40%       { transform: translateX(4px); }
  60%       { transform: translateX(-4px); }
  80%       { transform: translateX(4px); }
}
</style>
