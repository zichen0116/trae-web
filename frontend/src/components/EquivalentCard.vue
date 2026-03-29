<template>
  <div class="eq-section">
    <h4 class="eq-title">💸 这笔钱等于...</h4>
    <div class="eq-grid">
      <div
        v-for="(item, i) in items"
        :key="i"
        class="eq-item"
        :style="{ animationDelay: i * 0.15 + 's' }"
      >
        <span class="eq-emoji falling" :style="{ animationDelay: i * 0.2 + 's' }">{{ item.emoji }}</span>
        <span class="eq-text">{{ item.text }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  items: { type: Array, default: () => [] },
})
</script>

<style scoped>
.eq-section {
  background: rgba(255,215,0,0.05);
  border: 1px solid rgba(255,215,0,0.2);
  border-radius: 12px;
  padding: 16px 20px;
}

.eq-title {
  font-size: 14px;
  color: #FFD700;
  margin-bottom: 12px;
  font-weight: 700;
}

.eq-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.eq-item {
  display: flex;
  align-items: center;
  gap: 12px;
  animation: slide-in 0.4s ease both;
}

@keyframes slide-in {
  from { opacity: 0; transform: translateX(-16px); }
  to   { opacity: 1; transform: translateX(0); }
}

.eq-emoji {
  font-size: 28px;
  animation: fall-in 0.5s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes fall-in {
  from { opacity: 0; transform: translateY(-30px) rotate(-10deg); }
  to   { opacity: 1; transform: translateY(0) rotate(0); }
}

.eq-text {
  font-size: 15px;
  color: #e8f5e9;
  font-weight: 700;
}
</style>
