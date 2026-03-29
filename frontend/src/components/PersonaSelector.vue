<template>
  <div class="persona-section">
    <h3 class="section-label">选择你的「审判官」</h3>
    <div class="persona-grid">
      <button
        v-for="p in personas"
        :key="p.id"
        class="persona-card"
        :class="{ active: modelValue === p.id }"
        @click="$emit('update:modelValue', p.id)"
      >
        <span class="persona-emoji">{{ p.emoji }}</span>
        <span class="persona-name">{{ p.name }}</span>
        <span class="persona-desc">{{ p.desc }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({ modelValue: String })
defineEmits(['update:modelValue'])

const personas = [
  { id: 'caishen',     emoji: '🪙', name: '毒舌财神爷', desc: '钱财视角，傲慢辛辣' },
  { id: 'mama',        emoji: '👩', name: '暴躁老妈',   desc: '唠叨愤怒，专攻浪费' },
  { id: 'future_self', emoji: '😭', name: '吃土的自己', desc: '穿越懊悔，带哭腔乞求' },
  { id: 'cfo',         emoji: '📊', name: '刻薄财务总监', desc: 'ROI/IRR财务鄙视链' },
  { id: 'monk',        emoji: '🧘', name: '极简老禅师', desc: '万物皆空，当头棒喝' },
]
</script>

<style scoped>
.persona-section {}

.section-label {
  font-size: 13px;
  color: #6b9e82;
  margin-bottom: 12px;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.persona-grid {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.persona-card {
  flex: 1;
  min-width: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 14px 8px;
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  color: #e8f5e9;
  font-family: inherit;
}

.persona-card:hover {
  border-color: rgba(0, 214, 143, 0.4);
  background: rgba(0, 214, 143, 0.06);
}

.persona-card.active {
  border-color: #00D68F;
  background: rgba(0, 214, 143, 0.12);
  box-shadow: 0 0 16px rgba(0, 214, 143, 0.3);
}

.persona-emoji {
  font-size: 28px;
}

.persona-name {
  font-size: 13px;
  font-weight: 700;
}

.persona-desc {
  font-size: 11px;
  color: #6b9e82;
  text-align: center;
  line-height: 1.3;
}
</style>
