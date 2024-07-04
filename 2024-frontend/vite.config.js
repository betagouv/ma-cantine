import { fileURLToPath, URL } from "node:url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import vueDevTools from "vite-plugin-vue-devtools"
import { djangoVitePlugin } from "django-vite-plugin"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    djangoVitePlugin({
      input: ["src/main.js"],
      root: "../",
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      vue: fileURLToPath(new URL("./node_modules/vue/index.js", import.meta.url)),
    },
  },
  build: {
    manifest: true,
  },
})
