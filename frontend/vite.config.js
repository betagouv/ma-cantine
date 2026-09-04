import fs from "node:fs"
import path from "node:path"
import { fileURLToPath, URL } from "node:url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue2"
import Components from "unplugin-vue-components/vite"
import { VuetifyResolver } from "unplugin-vue-components/resolvers"

const rootDir = path.dirname(fileURLToPath(import.meta.url))
const OUT_DIR = path.resolve(rootDir, "dist")
const STATS_FILE = path.resolve(OUT_DIR, "webpack-stats.json")
const DEV_ORIGIN = "http://localhost:8080"

/**
 * Emits a django-webpack-loader compatible webpack-stats.json so we can keep
 * {% render_bundle 'app' %} without django-vite (for now).
 */
function djangoWebpackStatsPlugin() {
  const writeStats = (stats) => {
    fs.mkdirSync(path.dirname(STATS_FILE), { recursive: true })
    fs.writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2))
  }

  return {
    name: "django-webpack-stats",
    apply: () => true,
    configureServer(server) {
      writeStats({ status: "compile", publicPath: `${DEV_ORIGIN}/`, assets: {}, chunks: {} })

      const writeDevStats = () => {
        // Chunk keys must end with .js so webpack_loader emits <script> tags.
        // publicPath points at the real Vite URLs (HMR client has no .js suffix).
        writeStats({
          status: "done",
          publicPath: `${DEV_ORIGIN}/`,
          chunks: {
            app: ["@vite/client.js", "src/main.js"],
          },
          assets: {
            "@vite/client.js": {
              name: "@vite/client.js",
              publicPath: `${DEV_ORIGIN}/@vite/client`,
            },
            "src/main.js": {
              name: "src/main.js",
              publicPath: `${DEV_ORIGIN}/src/main.js`,
            },
          },
        })
      }

      server.httpServer?.once("listening", writeDevStats)

      const clean = () => {
        if (fs.existsSync(STATS_FILE)) {
          writeStats({ status: "compile", publicPath: `${DEV_ORIGIN}/`, assets: {}, chunks: {} })
        }
      }
      process.on("exit", clean)
      process.on("SIGINT", () => process.exit())
      process.on("SIGTERM", () => process.exit())
    },
    writeBundle(_options, bundle) {
      const assets = {}
      const chunkFiles = []

      for (const [fileName, output] of Object.entries(bundle)) {
        if (fileName.endsWith(".map")) continue

        const publicPath = `/static/${fileName}`
        assets[fileName] = {
          name: fileName,
          path: path.join(OUT_DIR, fileName),
          publicPath,
        }

        if (output.type === "chunk" && output.isEntry) {
          // CSS imported by the entry is listed in vite's importedCss (vite 5+)
          if (output.viteMetadata?.importedCss) {
            for (const cssFile of output.viteMetadata.importedCss) {
              if (!chunkFiles.includes(cssFile)) {
                chunkFiles.push(cssFile)
              }
              if (!assets[cssFile]) {
                assets[cssFile] = {
                  name: cssFile,
                  path: path.join(OUT_DIR, cssFile),
                  publicPath: `/static/${cssFile}`,
                }
              }
            }
          }
          chunkFiles.push(fileName)
        } else if (fileName.endsWith(".css") && !chunkFiles.includes(fileName)) {
          // fallback: include top-level css assets
          chunkFiles.push(fileName)
        }
      }

      writeStats({
        status: "done",
        publicPath: "/static/",
        chunks: {
          app: chunkFiles,
        },
        assets,
      })
    },
  }
}

// https://vitejs.dev/config/
export default defineConfig(({ command }) => ({
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
    // Replaces vuetify-loader: auto-import Vuetify 2 components used in templates
    Components({
      dirs: [],
      resolvers: [VuetifyResolver()],
    }),
    djangoWebpackStatsPlugin(),
  ],
  base: command === "build" ? "/static/" : "/",
  root: rootDir,
  publicDir: false,
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      // Keep runtime compiler available (was runtimeCompiler: true in vue-cli)
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
    manifest: false,
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
}))
