# 财神爷的凝视 — 设计文档

**日期：** 2026-03-29
**项目类型：** Mini 黑客松
**技术栈：** Vue 3 + Vite / FastAPI / 阿里云百炼（qwen-vl-max + qwen3.5-flash）

---

## 1. 问题与目标

**痛点：** 深夜刷淘宝/抖音容易冲动消费，买回来的东西大多吃灰。

**目标：** 用幽默、毒舌、视觉冲击的方式让用户在下单前三思，通过AI多角色"拷打"降低冲动消费。

---

## 2. 整体架构

```
用户浏览器（Vue 3）
    │  POST /api/analyze（图片base64 + 文字）
    ▼
FastAPI 后端
    │  OpenAI兼容SDK调用
    ▼
阿里云百炼（qwen-vl-max / qwen3.5-flash）
    │  返回结构化JSON
    ▼
前端渲染动画特效
```

**无数据库，无用户状态，每次分析独立无状态。**

---

## 3. 项目结构

```
trae/
├── frontend/                    # Vue 3 + Vite
│   ├── src/
│   │   ├── App.vue              # 单页主组件，管理全局状态
│   │   ├── components/
│   │   │   ├── HeroSection.vue          # 标题区
│   │   │   ├── UploadZone.vue           # 拖拽上传+预览
│   │   │   ├── InputForm.vue            # 商品名/理由/价格
│   │   │   ├── PersonaSelector.vue      # 5个人设卡片
│   │   │   ├── WalletHPBar.vue          # 右上角钱包血条
│   │   │   ├── ResultPanel.vue          # 结果面板容器
│   │   │   ├── DustGauge.vue            # 吃灰指数仪表盘
│   │   │   ├── RoastMessages.vue        # 逐条弹出拷打文案
│   │   │   ├── EquivalentCard.vue       # 等价物换算卡片
│   │   │   ├── VerdictButtons.vue       # 灵魂抉择按钮
│   │   │   ├── MoneyRain.vue            # 钞票雨特效
│   │   │   └── ClownStamp.vue           # 小丑印章特效
│   │   └── assets/
│   │       └── audio/                   # 音效文件（用户提供）
│   │           ├── bell.mp3
│   │           ├── coin.mp3
│   │           ├── kaching.mp3
│   │           └── clown.mp3
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── backend/                     # FastAPI
    ├── main.py                  # 入口+路由+CORS
    ├── ai_service.py            # 阿里云AI调用逻辑
    └── prompts.py               # 5个人设Prompt模板
```

---

## 4. UI/UX 视觉规范

**色彩：**
- 主色：`#00D68F`（Trae绿）/ `#00B377`（深绿）
- 强调：`#FFD700`（金色）
- 背景：深色 `#0A1510`，毛玻璃卡片 `rgba(255,255,255,0.05)` + `backdrop-filter: blur(12px)`
- 危险色：`#FF4444`（吃灰指数>80%时）

**字体：** 现代无衬线，标题加粗，拷打文案可用不同大小/颜色强调情绪

**页面从上到下布局（单页滚动）：**

1. **固定顶部** — 钱包血条（WalletHPBar），右上角，游戏风格HP条
2. **Hero区** — 大标题「财神爷的凝视」+ 副标题「敢买就剁手！！」+ 金色装饰
3. **人设选择器** — 5张毛玻璃横排卡片，选中时绿色发光边框
4. **上传区** — 虚线框，支持拖拽+点击，上传后显示图片预览
5. **输入表单** — 商品名称（必填）/ 购买理由（必填）/ 商品价格（必填）
6. **召唤按钮** — `⚡ 呼叫财神爷 拷打我`，绿色渐变+发光脉冲
7. **结果面板** — 分析完成后从底部展开，包含：
   - 吃灰指数仪表盘
   - 拷打文案逐条弹出
   - 等价物换算卡片
   - 灵魂抉择按钮

---

## 5. 人设列表

| Emoji | 名称 | 拷打风格 |
|-------|------|----------|
| 🪙 | 毒舌财神爷 | 毒舌讽刺，以钱财为视角 |
| 👩 | 暴躁老妈 | 专攻浪费钱和不务正业 |
| 😭 | 下个月吃土的自己 | 充满懊悔、绝望和乞求的穿越者 |
| 📊 | 刻薄财务总监 | 用ROI/IRR等财务术语鄙视购买决定 |
| 🧘 | 极简老禅师 | 看破红尘，"万物皆空，买来何用" |

---

## 6. 后端 API

### `POST /api/analyze`

**请求体：**
```json
{
  "product_name": "拍立得",
  "reason": "看起来很好玩",
  "price": 699,
  "persona": "caishen",
  "image_base64": "data:image/jpeg;base64,..."
}
```

**persona 枚举值：** `caishen` / `mama` / `future_self` / `cfo` / `monk`

**image_base64：** 可为空字符串（无图片时退化为纯文本模型）

**AI调用策略：**
- 有图片 → `qwen-vl-max`（视觉理解）
- 无图片 → `qwen3.5-flash`（纯文本）
- base_url: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- 使用 OpenAI Python SDK 兼容调用

**AI返回JSON（严格约束）：**
```json
{
  "roast_lines": ["第一句拷打", "第二句拷打", "第三句拷打"],
  "dust_score": 95,
  "equivalents": [
    {"emoji": "🍚", "text": "500斤东北大米"},
    {"emoji": "🧅", "text": "300斤山东大葱"},
    {"emoji": "🍔", "text": "233个麦辣鸡腿堡"}
  ],
  "hp_damage": 8800,
  "verdict": "终将沦为晾衣架"
}
```

**响应体（FastAPI透传给前端）：** 同上JSON结构，HTTP 200。

**错误处理：** AI返回非JSON或解析失败时，返回HTTP 500 + `{"error": "AI解析失败，请重试"}`。

---

## 7. 前端特效规范

| 时机 | 特效实现 |
|------|----------|
| 输入价格 | 血条实时计算，价格>500抖动动画（CSS keyframes shake） |
| 召唤按钮点击 | 发光脉冲 + loading spinner，禁用重复提交 |
| 拷打文案弹出 | 每条淡入+打字机效果，间隔800ms |
| 吃灰仪表盘 | SVG弧形，指针从0动画到目标值，>80%变红 |
| 等价物出现 | Emoji从顶部掉落CSS动画 |
| 点击「我悟了」 | 绿色钞票DOM粒子雨，提示守护金额 |
| 点击「我是小丑」 | 屏幕shake → 变灰 → 🤡印章scale弹入 |
| 悬停「我是小丑」 | 按钮随机translate逃跑一次，然后灰色倒计时3s |

**音效（HTML5 Audio，文件不存在时静默降级）：**
- `bell.mp3` — 召唤时
- `coin.mp3` — 等价物出现时
- `kaching.mp3` — 我悟了
- `clown.mp3` — 我是小丑

---

## 8. 音效/图片资源占位清单

以下文件需用户自行搜集并放入对应目录：

```
frontend/src/assets/audio/bell.mp3       # 寺庙钟声或子弹上膛声
frontend/src/assets/audio/coin.mp3       # 马里奥金币叮叮叮
frontend/src/assets/audio/kaching.mp3    # 收银机Ka-Ching
frontend/src/assets/audio/clown.mp3      # 滑稽小丑音效或Womp Womp
```

---

## 9. 开发边界

- 不做用户登录/注册
- 不做历史记录存储
- 不做多语言
- 不做移动端专属适配（响应式基础布局即可）
- 图片上传大小建议前端限制在5MB以内（阿里云限制）
