<template>
  <div class="hero">
    <div class="hero-title-wrapper">
      <h1 class="hero-title">Kytos</h1>
      <p class="hero-subtitle">
        局所解を超えろ。量子技術で実現する、真の負荷分散。
      </p>
    </div>
    <div class="hero-action-wrapper">
      <button class="hero-action-button" @click="$router.push('/demo')">
        試す
      </button>
    </div>
    <div class="hero-image-wrapper">
      <img src="/ship.svg" alt="Crate ship image" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "sass:color";
.hero {
  width: 100%;
  min-height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.hero-title-wrapper {
  margin: 0 1rem;
  margin-bottom: 2rem;
  text-align: center;
  width: 70%;
  max-width: 800px;
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  margin-bottom: 1rem;
  color: $on-surface-variant;
}

.hero-subtitle {
  font-size: clamp(1rem, 0.6875rem + 1vw, 1.25rem);
  color: $on-surface;
}
.hero-image-wrapper {
  width: 100%;
  overflow: hidden;
  img {
    max-height: 300px;
    position: relative;
    left: 0;
    animation: ship-move-left 20s linear infinite;
  }
}
.hero-action-button {
  border: none;
  border-radius: 8px;
  color: $on-primary;
  cursor: pointer;
  padding: 0.75rem 1.5rem;
  font-size: clamp(1rem, 1rem + 0vw, 1rem);
  background-color: $primary;
  transition: background-color 0.2s ease;
  &:hover {
    background-color: color.adjust($primary, $lightness: -10%);
  }
}

@keyframes ship-move-left {
  0% {
    transform: translateX(100vw);
  }
  100% {
    transform: translateX(-100%);
  }
}
</style>
