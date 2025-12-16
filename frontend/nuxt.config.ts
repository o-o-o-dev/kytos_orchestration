// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  modules: ["@nuxt/eslint", "@nuxt/ui", "@nuxt/image"],
  routeRules: {
    // "/api/kytos/**": { proxy: "https://api.kytos.o-o-o.dev/**" },
    "/api/kytos/**": { proxy: "http://172.17.32.155:8000/**" },
  },
  css: ["~/assets/scss/main.scss", "~/assets/css/main.css"],
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
