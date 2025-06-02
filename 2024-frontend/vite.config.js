import { fileURLToPath, URL } from "node:url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import vueDevTools from "vite-plugin-vue-devtools"
import { djangoVitePlugin } from "django-vite-plugin"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          // https://vuejs.org/guide/extras/web-components.html#example-vite-config
          isCustomElement: (tag) => tag.includes("-chart"),
        },
      },
    }),
    vueDevTools(),
    djangoVitePlugin({
      input: ["src/main.js"],
      root: "../",
    }),
  ],
  resolve: {
    alias: [
      {
        find: "@",
        replacement: fileURLToPath(new URL("./src", import.meta.url)),
      },
      {
        find: "vue",
        replacement: fileURLToPath(new URL("./node_modules/vue/index.js", import.meta.url)),
      },
      {
        find: "mdi-icons/styles.css",
        replacement: fileURLToPath(new URL("./node_modules/vue-material-design-icons/styles.css", import.meta.url)),
      },
      {
        find: /^mdi-icons\/([\w]+)/,
        replacement: fileURLToPath(new URL("./node_modules/vue-material-design-icons/$1.vue", import.meta.url)),
      },
    ],
  },
  server: {
    host: "0.0.0.0",
    origin: "http://localhost:8000",
  },
})
