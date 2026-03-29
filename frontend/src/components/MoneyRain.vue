<template>
  <div class="money-rain" @click="close">
    <div class="save-msg">
      <div class="save-icon">💰</div>
      <h2>恭喜你！成功守护钱包</h2>
      <p class="save-amount">+{{ price.toFixed(0) }} 元</p>
      <p class="save-hint">点击任意处关闭</p>
    </div>
    <span
      v-for="n in bills"
      :key="n.id"
      class="bill"
      :style="n.style"
    >💵</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({ price: { type: Number, default: 0 } })
const emit = defineEmits(['close'])

function close() { emit('close') }

const bills = ref(
  Array.from({ length: 30 }, (_, i) => ({
    id: i,
    style: {
      left: Math.random() * 100 + 'vw',
      animationDuration: (1.5 + Math.random() * 2) + 's',
      animationDelay: (Math.random() * 2) + 's',
      fontSize: (20 + Math.random() * 24) + 'px',
    }
  }))
)
</script>

<style scoped>
.money-rain {
  position: fixed;
  inset: 0;
  z-index: 9000;
  pointer-events: all;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.6);
  cursor: pointer;
}

.save-msg {
  text-align: center;
  z-index: 1;
  animation: pop-in 0.4s ease;
}

@keyframes pop-in {
  from { opacity: 0; transform: scale(0.7); }
  to   { opacity: 1; transform: scale(1); }
}

.save-icon {
  font-size: 64px;
  margin-bottom: 12px;
}

.save-msg h2 {
  font-size: 28px;
  font-weight: 900;
  color: #00D68F;
  margin-bottom: 8px;
}

.save-amount {
  font-size: 48px;
  font-weight: 900;
  color: #FFD700;
  margin-bottom: 12px;
}

.save-hint {
  font-size: 13px;
  color: rgba(255,255,255,0.4);
}

.bill {
  position: fixed;
  top: -60px;
  animation: fall linear infinite;
  user-select: none;
  pointer-events: none;
}

@keyframes fall {
  0%   { top: -60px; opacity: 1; transform: rotate(0deg); }
  100% { top: 110vh;  opacity: 0.6; transform: rotate(360deg); }
}
</style>
