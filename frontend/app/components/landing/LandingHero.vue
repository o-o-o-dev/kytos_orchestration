<template>
    <div class="hero">
        <div class="hero-inner">
            <div class="hero-text">
                <div class="hero-logos">
                    <div class="logo-container">
                        <img ref="tompediaLogo" class="tompedia-logo" src="/Tompedia_Labo-wordmark-jp-color.svg"
                            alt="Tompedia Logo" />
                        <svg width="32px" height="32px" class="multiply-logo" fill="none" stroke="currentColor"
                            viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path ref="multiplyLogo"
                                d="M13.41,12l6.3-6.29a1,1,0,1,0-1.42-1.42L12,10.59,5.71,4.29A1,1,0,0,0,4.29,5.71L10.59,12l-6.3,6.29a1,1,0,0,0,0,1.42,1,1,0,0,0,1.42,0L12,13.41l6.29,6.3a1,1,0,0,0,1.42,0,1,1,0,0,0,0-1.42Z" />
                        </svg>
                        <img ref="ohzekiLogo" class="ohzeki-logo" src="/ohzeki_logo.webp" alt="Ohzeki Lab Logo" />
                    </div>
                </div>
                <p class="hero-kicker">Quantum-inspired container orchestration</p>
                <h1 class="hero-title">Kytos Orchestration</h1>
                <p class="hero-subtitle">
                    量子アニーリングで「最小の移動」と「均等な負荷」を両立する、
                    次世代のサーバーオーケストレーション。
                </p>

                <div class="hero-actions">
                    <NuxtLink class="hero-action-button" to="/demo">試す</NuxtLink>
                </div>
            </div>

            <div class="hero-visual" aria-hidden="true">
                <div class="sea">
                    <div class="cargo">
                        <span class="box" />
                        <span class="box" />
                        <span class="box" />
                        <span class="box" />
                        <span class="box" />
                        <span class="box" />
                    </div>
                    <img class="ship" src="/ship.svg" alt="" />
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
@use "sass:color";

.hero {
    width: 100%;
    padding: 2.5rem 0 1.5rem;
    background: linear-gradient(180deg,
            color.adjust($surface, $lightness: 0%) 0%,
            color.adjust($surface, $lightness: -2%) 100%);
}

.hero-inner {
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 1.25rem;
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 2rem;
    align-items: center;
}

.hero-kicker {
    color: color.adjust($on-surface, $lightness: -5%);
    font-size: 0.9rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.hero-title {
    font-size: clamp(2.25rem, 4.5vw, 3.75rem);
    font-weight: 800;
    margin-bottom: 0.75rem;
    color: $on-surface-variant;
}

.hero-subtitle {
    font-size: clamp(1rem, 0.85rem + 0.6vw, 1.15rem);
    color: $on-surface;
    line-height: 1.9;
    max-width: 60ch;
}

.hero-actions {
    margin-top: 1.25rem;
}

.hero-action-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: none;
    border-radius: 12px;
    color: $on-primary;
    cursor: pointer;
    padding: 0.85rem 1.35rem;
    font-size: 1rem;
    font-weight: 700;
    background-color: $primary;
    transition:
        transform 0.15s ease,
        background-color 0.2s ease;

    &:hover {
        background-color: color.adjust($primary, $lightness: -10%);
        transform: translateY(-1px);
    }

    &:active {
        transform: translateY(0);
    }
}

.hero-metrics {
    margin-top: 1.5rem;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.75rem;
}

.metric {
    border-radius: 12px;
    padding: 0.85rem 0.9rem;
    background: color.adjust($surface, $lightness: -1%);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
}

.metric-label {
    font-size: 0.8rem;
    color: $on-surface;
}

.metric-value {
    margin-top: 0.25rem;
    font-weight: 800;
    color: $on-surface-variant;
    font-size: 1rem;
}

.hero-visual {
    position: relative;
    min-height: 260px;
}

.sea {
    position: relative;
    border-radius: 18px;
    height: 260px;
    overflow: hidden;
    background: linear-gradient(180deg,
            color.adjust($secondary, $alpha: -0.82) 0%,
            color.adjust($secondary, $alpha: -0.9) 100%);
    border: 1px solid color.adjust($on-surface, $alpha: -0.85);
}

.sea::after {
    content: "";
    position: absolute;
    left: -30%;
    right: -30%;
    bottom: -45px;
    height: 110px;
    background: radial-gradient(closest-side,
            color.adjust($primary, $alpha: -0.7),
            transparent);
    filter: blur(12px);
}

.cargo {
    position: absolute;
    top: 1rem;
    left: 1rem;
    display: grid;
    grid-template-columns: repeat(3, 14px);
    gap: 8px;
    opacity: 0.9;
}

.box {
    width: 14px;
    height: 14px;
    border-radius: 4px;
    background: color.adjust($primary, $lightness: 4%);
    border: 1px solid color.adjust($primary, $lightness: -6%);
}

.ship {
    max-height: 190px;
    position: absolute;
    bottom: 18px;
    left: 0;
    animation: ship-move-left 18s linear infinite;
    opacity: 0.95;
}

@keyframes ship-move-left {
    0% {
        transform: translateX(110%);
    }

    100% {
        transform: translateX(-120%);
    }
}

@media (max-width: 900px) {
    .hero-inner {
        grid-template-columns: 1fr;
    }

    .hero-visual {
        order: 2;
    }

    .hero-metrics {
        grid-template-columns: 1fr;
    }
}


.hero-logos {
  margin: 2rem 0;
}

.logo-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 1rem;
  padding: 0;

  .tompedia-logo {
    height: 16px;
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
    height: 20px;
    width: auto;
  }
}
</style>
