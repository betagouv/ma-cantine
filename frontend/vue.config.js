const BundleTracker = require("webpack-bundle-tracker")
const { VuetifyPlugin } = require("webpack-plugin-vuetify")
const debug = !process.env.DEBUG || process.env.DEBUG === "True"
const publicPath = debug ? "http://127.0.0.1:8080/" : "/static/"

module.exports = {
  transpileDependencies: ["vuetify"],
  runtimeCompiler: true,
  publicPath: publicPath,
  outputDir: "./dist/",

  pluginOptions: {
    vuetify: {
      // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
    },
  },

  configureWebpack: {
    devtool: "source-map",
  },

  css: {
    sourceMap: true,
  },

  chainWebpack: (config) => {
    config.optimization.splitChunks(false)

    config.plugin("BundleTracker").use(BundleTracker, [{ filename: "../frontend/webpack-stats.json" }])
    config.plugin("VuetifyPlugin").use(VuetifyPlugin, [{ autoimport: true }])

    config.resolve.alias.set("__STATIC__", "static")
    config.resolve.alias.set("vue", "@vue/compat")

    config.module
      .rule("vue")
      .use("vue-loader")
      .tap((options) => {
        return {
          ...options,
          compilerOptions: {
            compatConfig: {
              MODE: 2,
            },
          },
        }
      })

    config.devServer
      .host("127.0.0.1")
      .port(8080)
      .https(false)
      // eslint-disable-next-line no-useless-escape
      .headers({ "Access-Control-Allow-Origin": ["*"] })
  },
}
