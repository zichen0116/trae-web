# 财神爷的凝视 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个单页面冲动消费劝阻工具，用AI多角色拷打+视觉特效让用户三思而后行。

**Architecture:** Vue 3 前端单页 + FastAPI 后端，前端 base64 编码图片 POST 到 `/api/analyze`，后端调用阿里云百炼视觉/文本模型返回结构化 JSON，前端渲染动画特效。无数据库，无状态。

**Tech Stack:** Vue 3 + Vite、FastAPI、Python openai SDK（兼容阿里云百炼）、纯 CSS 动画、SVG 仪表盘

---

## Task 1: 创建 git 分支 + 后端骨架

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/prompts.py`
- Create: `backend/ai_service.py`
- Create: `backend/main.py`

- [ ] **Step 1: 创建开发分支**

```bash
cd D:/Develop/Project/trae && git checkout -b feature/caishen-gaze
```

Expected: `Switched to a new branch 'feature/caishen-gaze'`

- [ ] **Step 2: 创建 `backend/requirements.txt`**

```
fastapi==0.115.0
uvicorn==0.30.0
openai==1.40.0
python-multipart==0.0.9
```

- [ ] **Step 3: 创建 `backend/prompts.py`**

```python
PERSONA_PROMPTS = {
    "caishen": "你是毒舌财神爷，掌管天下财富，说话毒舌讽刺、金句频出。用钱财、投资、机会成本的视角嘲讽。语气傲慢、辛辣、偶尔带点老北京腔。",
    "mama": "你是暴躁老妈，省吃俭用养大孩子，看到孩子乱花钱就心疼+愤怒。专攻浪费钱和不务正业。语气唠叨、情绪激动、夹杂'你这孩子''我的老天爷'等口头语。",
    "future_self": "你是'下个月吃土的自己'，穿越回来的穷鬼。因为用户今天的冲动消费，你下个月花呗还不上、泡面买不起。语气充满懊悔、绝望、乞求，说话带哭腔，偶尔崩溃。",
    "cfo": "你是刻薄财务总监，CFA持证人，用ROI、IRR、机会成本、NPV等财务术语鄙视用户的购买决定。语气冷漠、专业、充满鄙视，把买东西说成一场失败的投资决策。",
    "monk": "你是极简老禅师，看破红尘，万物皆空。用佛理、禅语、顿悟式语言劝导用户放下执念。语气平和却犀利，每句话都像当头棒喝。",
}

SYSTEM_SUFFIX = """

用户会告诉你他们想买的商品名称、购买理由、价格，可能附有商品图片。请用你的人设对这个购买决定进行辛辣点评。

【重要】你必须严格按照以下JSON格式返回，不要有任何多余文字：
{
  "roast_lines": ["第一句拷打（15-40字）", "第二句拷打（15-40字）", "第三句拷打（15-40字）"],
  "dust_score": <0-100的整数，代表这个商品最终变成吃灰废品的概率>,
  "equivalents": [
    {"emoji": "<食物或生活用品emoji>", "text": "<这笔钱能买多少XX，要具体有趣>"},
    {"emoji": "<另一个emoji>", "text": "<另一个等价物>"},
    {"emoji": "<第三个emoji>", "text": "<第三个等价物>"}
  ],
  "hp_damage": <500-9999的整数，代表对钱包造成的伤害值>,
  "verdict": "<一句话终极判决，10-20字，辛辣>"
}

只返回JSON，不要有任何旁白、解释或markdown格式。
"""


def build_system_prompt(persona: str) -> str:
    base = PERSONA_PROMPTS.get(persona, PERSONA_PROMPTS["caishen"])
    return base + SYSTEM_SUFFIX


def build_user_message(product_name: str, reason: str, price: float) -> str:
    return f"商品名称：{product_name}\n购买理由：{reason}\n商品价格：{price}元\n请开始拷打。"
```

- [ ] **Step 4: 创建 `backend/ai_service.py`**

```python
import json
import re
from openai import OpenAI
from prompts import build_system_prompt, build_user_message

API_KEY = "sk-be0e3af7df284df5abe735dce5ca6953"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
VISION_MODEL = "qwen-vl-max"
TEXT_MODEL = "qwen3.5-flash"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def analyze(product_name: str, reason: str, price: float, persona: str, image_base64: str) -> dict:
    system_prompt = build_system_prompt(persona)
    user_text = build_user_message(product_name, reason, price)

    if image_base64:
        model = VISION_MODEL
        content = [
            {"type": "image_url", "image_url": {"url": image_base64}},
            {"type": "text", "text": user_text},
        ]
    else:
        model = TEXT_MODEL
        content = user_text

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
    )

    raw = response.choices[0].message.content.strip()
    match = re.search(r'\{[\s\S]*\}', raw)
    if not match:
        raise ValueError(f"AI未返回有效JSON: {raw}")
    return json.loads(match.group())
```

- [ ] **Step 5: 创建 `backend/main.py`**

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_service import analyze

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    product_name: str
    reason: str
    price: float
    persona: str = "caishen"
    image_base64: str = ""


@app.post("/api/analyze")
def analyze_endpoint(req: AnalyzeRequest):
    try:
        result = analyze(
            product_name=req.product_name,
            reason=req.reason,
            price=req.price,
            persona=req.persona,
            image_base64=req.image_base64,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI解析失败，请重试: {str(e)}")


@app.get("/health")
def health():
    return {"status": "ok"}
```

- [ ] **Step 6: Commit**

```bash
cd D:/Develop/Project/trae
git add backend/
git commit -m "feat: 后端骨架 FastAPI + 阿里云百炼AI调用"
```

---

## Task 2: 初始化 Vue 3 前端 + App.vue 骨架

**Files:**
- Create: `frontend/` (Vite scaffold)
- Modify: `frontend/vite.config.js`
- Modify: `frontend/index.html`
- Create: `frontend/src/utils/audio.js`
- Modify: `frontend/src/App.vue`

- [ ] **Step 1: Vite 脚手架**

```bash
cd D:/Develop/Project/trae
npm create vite@latest frontend -- --template vue
cd frontend && npm install
```

- [ ] **Step 2: 修改 `frontend/vite.config.js`**

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
```

- [ ] **Step 3: 修改 `frontend/index.html`**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>财神爷的凝视 - 敢买就剁手</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

- [ ] **Step 4: 创建 `frontend/src/utils/audio.js`**

```javascript
const audioCache = {}

export function playAudio(name) {
  try {
    if (!audioCache[name]) {
      audioCache[name] = new Audio(`/src/assets/audio/${name}.mp3`)
    }
    audioCache[name].currentTime = 0
    audioCache[name].play().catch(() => {})
  } catch {}
}
```

- [ ] **Step 5: 创建音效目录**

```bash
mkdir -p D:/Develop/Project/trae/frontend/src/assets/audio
```

- [ ] **Step 6: 替换 `frontend/src/App.vue`**

```vue
<template>
  <div class="app">
    <WalletHPBar :price="Number(form.price) || 0" />
    <HeroSection />
    <main class="main-content">
      <PersonaSelector v-model="form.persona" />
      <UploadZone v-model="form.imageBase64" />
      <InputForm v-model="form" />
      <button
        class="summon-btn"
        :disabled="loading || !isFormValid"
        @click="handleSummon"
      >
        <span v-if="loading" class="spinner"></span>
        <span v-else>⚡ 呼叫财神爷 拷打我</span>
      </button>
      <ResultPanel
        v-if="result"
        :result="result"
        :price="Number(form.price)"
        @decision="handleDecision"
      />
      <MoneyRain v-if="showMoneyRain" :price="Number(form.price)" />
      <ClownStamp v-if="showClownStamp" />
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import WalletHPBar from './components/WalletHPBar.vue'
import HeroSection from './components/HeroSection.vue'
import PersonaSelector from './components/PersonaSelector.vue'
import UploadZone from './components/UploadZone.vue'
import InputForm from './components/InputForm.vue'
import ResultPanel from './components/ResultPanel.vue'
import MoneyRain from './components/MoneyRain.vue'
import ClownStamp from './components/ClownStamp.vue'
import { playAudio } from './utils/audio'

const form = ref({
  product_name: '',
  reason: '',
  price: '',
  persona: 'caishen',
  imageBase64: '',
})

const loading = ref(false)
const result = ref(null)
const showMoneyRain = ref(false)
const showClownStamp = ref(false)

const isFormValid = computed(() =>
  form.value.product_name.trim() &&
  form.value.reason.trim() &&
  Number(form.value.price) > 0
)

async function handleSummon() {
  loading.value = true
  result.value = null
  showMoneyRain.value = false
  showClownStamp.value = false
  playAudio('bell')
