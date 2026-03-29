<template>
  <div class="roast-container">
    <div
      v-for="(line, i) in visibleLines"
      :key="i"
      class="roast-line"
      :style="lineStyle(i)"
    >
      <span class="roast-quote">「</span>
      <span class="roast-text">{{ line }}</span>
      <span class="roast-quote">」</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  lines: { type: Array, default: () => [] },
})

const visibleLines = ref([])

onMounted(() => {
  props.lines.forEach((line, i) => {
    setTimeout(() => {
      visibleLines.value.push(line)
    }, i * 900)
  })
})

function lineStyle(i) {
  const sizes = ['18px', '22px', '16px']
  const colors = ['#e8f5e9', '#FFD700', '#FF4444']
  return {
    fontSize: sizes[i % sizes.length],
    color: colors[i % colors.length],
  }
}
</script>

<style scoped>
.roast-container {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.roast-line {
  animation: fade-slide-in 0.6s ease forwards;
  line-height: 1.5;
  font-weight: 700;
  text-align: center;
}

@keyframes fade-slide-in {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

.roast-quote {
  color: rgba(255,215,0,0.5);
  font-size: 0.9em;
}
</style>
