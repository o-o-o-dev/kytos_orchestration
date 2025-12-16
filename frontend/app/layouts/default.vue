<template>
    <div class="default-wrapper">
        <main>
            <slot />
        </main>
        <footer>
            <div>
                <p>
                    &copy; 2025 Morio Chiba, Tatsuhiro Araki, Soma Terao. All
                    rights reserved.
                </p>
            </div>
        </footer>
    </div>
</template>

<style lang="scss" scoped>
.default-wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    min-height: 100vh;
    main {
        flex: 1;
        width: 100%;
    }

    footer {
        margin-top: 2rem;
        div {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 1rem 0;
            img {
                margin-bottom: 0.5rem;
            }
            p {
                font-size: 0.875rem;
                color: $on-surface;
            }
        }
    }
}
</style>
