<template>
  <div class="gauge-wrapper">
    <svg class="gauge-svg" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
      <!-- 背景弧 -->
      <path
        d="M 20 100 A 80 80 0 0 1 180 100"
        fill="none"
        stroke="rgba(255,255,255,0.1)"
        stroke-width="16"
        stroke-linecap="round"
      />
      <!-- 进度弧 -->
      <path
        d="M 20 100 A 80 80 0 0 1 180 100"
        fill="none"
        :stroke="arcColor"
        stroke-width="16"
        stroke-linecap="round"
        :stroke-dasharray="arcLength"
        :stroke-dashoffset="arcOffset"
        style="transition: stroke-dashoffset 1.2s ease, stroke 0.5s ease"
      />
      <!-- 指针 -->
      <line
        x1="100" y1="100"
        :x2="needleX" :y2="needleY"
        :stroke="arcColor"
        stroke-width="3"
        stroke-linecap="round"
        style="transition: x2 1.2s ease, y2 1.2s ease, stroke 0.5s ease"
      />
      <circle cx="100" cy="100" r="6" :fill="arcColor" style="transition: fill 0.5s ease" />
      <!-- 数值 -->
      <text x="100" y="82" text-anchor="middle" :fill="arcColor" font-size="28" font-weight="900"
        style="transition: fill 0.5s ease">{{ displayScore }}%</text>
      <text x="100" y="115" text-anchor="middle" fill="#6b9e82" font-size="11">吃灰指数</text>
    </svg>
    <div class="verdict-badge" :style="{ borderColor: arcColor, color: arcColor }">
      {{ verdict }}
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'

const props = defineProps({
  score: { type: Number, default: 0 },
  verdict: { type: String, default: '' },
})

const displayScore = ref(0)

onMounted(() => {
  setTimeout(() => { displayScore.value = props.score }, 100)
})

const arcColor = computed(() => {
  if (displayScore.value > 80) return '#FF4444'
  if (displayScore.value > 50) return '#FFD700'
  return '#00D68F'
})

// 半圆总长度 = π * r = π * 80 ≈ 251.3
const ARC_LEN = Math.PI * 80

const arcLength = ARC_LEN

const arcOffset = computed(() =>
  ARC_LEN - (displayScore.value / 100) * ARC_LEN
)

// 指针：从左端(-180deg)到右端(0deg)，score=0在左，score=100在右
const angle = computed(() => {
  const deg = -180 + (displayScore.value / 100) * 180
  return (deg * Math.PI) / 180
})

const needleX = computed(() => 100 + 70 * Math.cos(angle.value))
const needleY = computed(() => 100 + 70 * Math.sin(angle.value))
</script>

<style scoped>
.gauge-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.gauge-svg {
  width: 100%;
  max-width: 260px;
}

.verdict-badge {
  border: 2px solid;
  border-radius: 20px;
  padding: 6px 18px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  background: rgba(0,0,0,0.3);
}
</style>
