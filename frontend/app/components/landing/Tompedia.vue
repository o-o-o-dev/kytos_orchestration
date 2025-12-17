<template>
  <div class="hero-logos">
    <div class="logo-container">
      <img ref="tompediaLogo" class="tompedia-logo" src="/Tompedia_Labo-wordmark-jp-color.svg" alt="Tompedia Logo" />
      <svg width="32px" height="32px" class="multiply-logo" fill="none" stroke="currentColor" viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg">
        <path ref="multiplyLogo"
          d="M13.41,12l6.3-6.29a1,1,0,1,0-1.42-1.42L12,10.59,5.71,4.29A1,1,0,0,0,4.29,5.71L10.59,12l-6.3,6.29a1,1,0,0,0,0,1.42,1,1,0,0,0,1.42,0L12,13.41l6.29,6.3a1,1,0,0,0,1.42,0,1,1,0,0,0,0-1.42Z" />
      </svg>
      <img ref="ohzekiLogo" class="ohzeki-logo" src="/ohzeki_logo.webp" alt="Ohzeki Lab Logo" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.hero-logos {
  margin-top: 2rem;
}

.logo-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 0;

  .tompedia-logo {
    height: 32px;
    width: auto;
  }

  .multiply-logo {
    width: 18px;
    height: 18px;
    color: $on-surface;
    opacity: 0.35;
    flex-shrink: 0;
  }

  .ohzeki-logo {
    height: 40px;
    width: auto;
  }
}
</style>