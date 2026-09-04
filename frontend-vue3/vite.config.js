import { fileURLToPath, URL } from "node:url"
import path from "node:path"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import vueDevTools from "vite-plugin-vue-devtools"

const rootDir = path.dirname(fileURLToPath(import.meta.url))

// https://vitejs.dev/config/
// Backend integration: https://vitejs.dev/guide/backend-integration.html
// Django bridge: https://github.com/MrBin99/django-vite
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
  ],
  base: "/static/",
  root: rootDir,
  build: {
    manifest: "manifest.json",
    outDir: path.resolve(rootDir, "../build"),
    emptyOutDir: true,
    rollupOptions: {
      input: path.resolve(rootDir, "src/main.js"),
    },
  },
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
    ],
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    origin: "http://localhost:5173",
  },
})
