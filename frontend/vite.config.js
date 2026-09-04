import path from "node:path"
import { fileURLToPath, URL } from "node:url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue2"
import Components from "unplugin-vue-components/vite"
import { VuetifyResolver } from "unplugin-vue-components/resolvers"

const rootDir = path.dirname(fileURLToPath(import.meta.url))
const OUT_DIR = path.resolve(rootDir, "dist")
const DEV_ORIGIN = "http://localhost:8080"

// https://vitejs.dev/config/
// Backend integration: https://vitejs.dev/guide/backend-integration.html
// Django bridge: https://github.com/MrBin99/django-vite (app="vue2")
export default defineConfig({
  plugins: [
    vue({
      template: {
        // Keep Django absolute URLs like /static/images/... as browser paths
        // (plugin-vue2 defaults includeAbsolute: true in production builds)
        transformAssetUrlsOptions: {
          includeAbsolute: false,
        },
      },
    }),
    // Auto-import Vuetify 2 components used in templates
    Components({
      dirs: [],
      resolvers: [VuetifyResolver()],
    }),
  ],
  // Must match STATIC_URL so django-vite can resolve both dev and prod URLs
  base: "/static/",
  root: rootDir,
  publicDir: false,
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      vue: "vue/dist/vue.esm.js",
    },
    extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
  },
  css: {
    preprocessorOptions: {
      sass: {
        // Inject DSFR / Vuetify variable overrides into Vuetify's indented sass sources
        additionalData: `@import "@/scss/variables.scss"\n`,
        quietDeps: true,
        silenceDeprecations: [
          "slash-div",
          "legacy-js-api",
          "global-builtin",
          "import",
          "color-functions",
          "if-function",
        ],
      },
      scss: {
        additionalData: `@import "@/scss/variables.scss";`,
        quietDeps: true,
        silenceDeprecations: [
          "slash-div",
          "legacy-js-api",
          "global-builtin",
          "import",
          "color-functions",
          "if-function",
        ],
      },
    },
  },
  optimizeDeps: {
    include: ["vuetify", "vue", "vue-router", "vuex", "vue-matomo"],
  },
  build: {
    outDir: OUT_DIR,
    emptyOutDir: true,
    manifest: "manifest.json",
    sourcemap: true,
    rollupOptions: {
      input: path.resolve(rootDir, "src/main.js"),
      output: {
        entryFileNames: "js/app.[hash].js",
        chunkFileNames: "js/[name].[hash].js",
        assetFileNames: "assets/[name].[hash][extname]",
      },
    },
  },
  server: {
    host: "0.0.0.0",
    port: 8080,
    strictPort: true,
    origin: DEV_ORIGIN,
    cors: true,
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  },
})
