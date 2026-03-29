<template>
  <div class="result-panel" ref="panelEl">
    <div class="panel-header">
      <h2 class="panel-title">🔥 审判结果</h2>
      <div class="hp-damage-badge">💥 {{ result.hp_damage }} 点暴击伤害！</div>
    </div>

    <DustGauge :score="result.dust_score" :verdict="result.verdict" />

    <div class="roast-section">
      <h4 class="section-label">财神爷裁决</h4>
      <RoastMessages :lines="result.roast_lines" />
    </div>

    <EquivalentCard :items="result.equivalents" />

    <VerdictButtons @decision="$emit('decision', $event)" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DustGauge from './DustGauge.vue'
import RoastMessages from './RoastMessages.vue'
import EquivalentCard from './EquivalentCard.vue'
import VerdictButtons from './VerdictButtons.vue'

defineProps({ result: Object, price: Number })
defineEmits(['decision'])

const panelEl = ref(null)
onMounted(() => {
  panelEl.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
})
</script>

<style scoped>
.result-panel {
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 214, 143, 0.2);
  border-radius: 16px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  animation: slide-up 0.5s ease;
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}

.panel-title {
  font-size: 22px;
  font-weight: 900;
  color: #e8f5e9;
}

.hp-damage-badge {
  background: rgba(255,68,68,0.15);
  border: 1px solid rgba(255,68,68,0.4);
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 14px;
  font-weight: 700;
  color: #FF4444;
  animation: pulse 1s ease 3;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50%       { transform: scale(1.06); }
}

.roast-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-label {
  font-size: 13px;
  color: #6b9e82;
  letter-spacing: 1px;
  text-transform: uppercase;
}
</style>
