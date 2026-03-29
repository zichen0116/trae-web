<template>
  <div class="clown-overlay">
    <div class="stamp" :class="{ stamped: isStamped }">
      <div class="stamp-inner">
        <div class="stamp-emoji">🤡</div>
        <div class="stamp-text">小丑竟是我自己</div>
      </div>
    </div>
    <p class="clown-msg" v-if="isStamped">财神爷已记录在案，祝您吃灰愉快 🪄</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isStamped = ref(false)

onMounted(() => {
  setTimeout(() => { isStamped.value = true }, 100)
})
</script>

<style scoped>
.clown-overlay {
  position: fixed;
  inset: 0;
  z-index: 9000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.75);
  animation: desaturate 0.5s ease forwards;
}

@keyframes desaturate {
  from { filter: none; }
  to   { filter: grayscale(0.6); }
}

.stamp {
  width: 280px;
  height: 280px;
  border: 8px solid #FF4444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(3) rotate(-15deg);
  transition: opacity 0.3s ease, transform 0.3s cubic-bezier(.36,.07,.19,.97);
}

.stamp.stamped {
  opacity: 1;
  transform: scale(1) rotate(-15deg);
}

.stamp-inner {
  text-align: center;
}

.stamp-emoji {
  font-size: 72px;
  animation: spin-once 0.4s ease 0.1s both;
}

@keyframes spin-once {
  from { transform: rotate(-180deg) scale(0.5); }
  to   { transform: rotate(0deg) scale(1); }
}

.stamp-text {
  font-size: 22px;
  font-weight: 900;
  color: #FF4444;
  letter-spacing: 2px;
  margin-top: 8px;
}

.clown-msg {
  margin-top: 24px;
  font-size: 14px;
  color: rgba(255,255,255,0.5);
  animation: fade-in 0.5s ease 0.6s both;
}

@keyframes fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}
</style>
