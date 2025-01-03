// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  // route rules
  routeRules: {
    "/": {
      redirect: "/home"
    },
  },

  // use typescript type checking
  typescript: {
    typeCheck: true
  },

  // inject SCSS code (colors definition)
  css: [`assets/styles/main.scss`],

  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/styles/_colors.scss" as *; @use "~/assets/styles/_mixings.scss" as *; @use "~/assets/styles/_fonts.scss" as *;'
        }
      }
    }
  }

})
