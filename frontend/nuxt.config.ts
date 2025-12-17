// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  modules: ["@nuxt/eslint", "@nuxt/ui", "@nuxt/image"],
  routeRules: {
    "/api/kytos/**": { proxy: process.env.KYTOS_API_PROXY },
  },
  css: ["~/assets/scss/main.scss", "~/assets/css/main.css", "katex/dist/katex.min.css"],
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/scss/_variables.scss" as *;',
        },
      },
    },
  },
});
