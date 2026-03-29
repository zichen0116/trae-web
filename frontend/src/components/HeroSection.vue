<template>
  <header class="hero">
    <div class="hero-deco left">🪙</div>
    <div class="hero-center">
      <h1 class="hero-title">
        <span class="gold">财神爷</span>的凝视
      </h1>
      <p class="hero-subtitle">敢买就剁手！！</p>
      <p class="hero-desc">你的冲动消费，由本神亲自审判</p>
    </div>
    <div class="hero-deco right">🧧</div>
  </header>
</template>

<style scoped>
.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px 32px;
  position: relative;
  text-align: center;
}

.hero-center {
  flex: 1;
}

.hero-deco {
  font-size: 48px;
  opacity: 0.6;
  user-select: none;
  animation: float 3s ease-in-out infinite;
}

.hero-deco.right {
  animation-delay: 1.5s;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-10px); }
}

.hero-title {
  font-size: clamp(36px, 6vw, 64px);
  font-weight: 900;
  letter-spacing: 2px;
  line-height: 1.1;
  color: #e8f5e9;
  text-shadow: 0 0 30px rgba(0, 214, 143, 0.3);
}

.gold {
  color: #FFD700;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
}

.hero-subtitle {
  font-size: clamp(18px, 3vw, 26px);
  font-weight: 700;
  color: #FF4444;
  margin-top: 8px;
  letter-spacing: 1px;
  animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.6; }
}

.hero-desc {
  margin-top: 10px;
  font-size: 14px;
  color: #6b9e82;
  letter-spacing: 1px;
}
</style>
