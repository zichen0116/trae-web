<template>
  <div
    class="upload-zone"
    :class="{ 'has-image': modelValue, 'drag-over': isDragging }"
    @click="triggerInput"
    @dragover.prevent="isDragging = true"
    @dragleave="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      style="display:none"
      @change="handleFile"
    />
    <div v-if="!modelValue" class="upload-placeholder">
      <span class="upload-icon">🖼️</span>
      <p>拖拽或点击上传商品图片</p>
      <p class="upload-hint">支持 JPG / PNG / WebP，最大 5MB</p>
    </div>
    <div v-else class="preview-wrapper">
      <img :src="modelValue" class="preview-img" alt="商品图片" />
      <button class="remove-btn" @click.stop="clearImage">✕ 移除</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({ modelValue: String })
const emit = defineEmits(['update:modelValue'])

const fileInput = ref(null)
const isDragging = ref(false)

function triggerInput() {
  if (!props.modelValue) fileInput.value.click()
}

function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) processFile(file)
}

function handleFile(e) {
  const file = e.target.files[0]
  if (file) processFile(file)
}

function processFile(file) {
  if (file.size > 5 * 1024 * 1024) {
    alert('图片不能超过 5MB')
    return
  }
  const reader = new FileReader()
  reader.onload = (e) => emit('update:modelValue', e.target.result)
  reader.readAsDataURL(file)
}

function clearImage() {
  emit('update:modelValue', '')
  fileInput.value.value = ''
}
</script>

<style scoped>
.upload-zone {
  border: 2px dashed rgba(0, 214, 143, 0.3);
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: rgba(255,255,255,0.02);
  min-height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-zone:hover,
.upload-zone.drag-over {
  border-color: #00D68F;
  background: rgba(0, 214, 143, 0.05);
}

.upload-zone.has-image {
  padding: 12px;
  cursor: default;
  border-style: solid;
  border-color: rgba(0, 214, 143, 0.4);
}

.upload-icon {
  font-size: 36px;
  display: block;
  margin-bottom: 8px;
}

.upload-placeholder p {
  color: #6b9e82;
  font-size: 14px;
  margin: 4px 0;
}

.upload-hint {
  font-size: 12px !important;
  opacity: 0.6;
}

.preview-wrapper {
  position: relative;
  width: 100%;
}

.preview-img {
  max-height: 200px;
  max-width: 100%;
  border-radius: 8px;
  object-fit: contain;
  display: block;
  margin: 0 auto;
}

.remove-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255,68,68,0.8);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 4px 10px;
  font-size: 12px;
  cursor: pointer;
  font-family: inherit;
}

.remove-btn:hover {
  background: #FF4444;
}
</style>
