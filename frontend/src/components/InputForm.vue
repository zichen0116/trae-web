<template>
  <div class="input-form">
    <div class="field">
      <label>商品名称 <span class="required">*</span></label>
      <input
        type="text"
        v-model="local.product_name"
        placeholder="例如：拍立得、跑步机、空气炸锅..."
        @input="emit('update:modelValue', { ...local })"
      />
    </div>
    <div class="field">
      <label>购买理由 <span class="required">*</span></label>
      <input
        type="text"
        v-model="local.reason"
        placeholder="例如：看起来很好玩、网红都在用..."
        @input="emit('update:modelValue', { ...local })"
      />
    </div>
    <div class="field">
      <label>商品价格（元）<span class="required">*</span></label>
      <input
        type="number"
        v-model="local.price"
        placeholder="例如：699"
        min="0"
        @input="emit('update:modelValue', { ...local })"
      />
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({ modelValue: Object })
const emit = defineEmits(['update:modelValue'])

const local = reactive({ ...props.modelValue })

watch(() => props.modelValue, (val) => {
  Object.assign(local, val)
}, { deep: true })
</script>

<style scoped>
.input-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 13px;
  color: #a0c4ae;
  letter-spacing: 0.5px;
}

.required {
  color: #FF4444;
}

input {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  padding: 14px 16px;
  color: #e8f5e9;
  font-size: 15px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  width: 100%;
}

input::placeholder {
  color: rgba(255,255,255,0.25);
}

input:focus {
  border-color: #00D68F;
  box-shadow: 0 0 0 3px rgba(0, 214, 143, 0.15);
}

input[type=number]::-webkit-inner-spin-button {
  opacity: 0.3;
}
</style>
