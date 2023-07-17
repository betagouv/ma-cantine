const BundleTracker = require("webpack-bundle-tracker")
const debug = !process.env.DEBUG || process.env.DEBUG === "True"
const publicPath = debug ? "http://127.0.0.1:8080/" : "/static/"

module.exports = {
  transpileDependencies: ["vuetify"],
  runtimeCompiler: true,
  publicPath: publicPath,
  outputDir: "./dist/",

  configureWebpack: {
    devtool: "source-map",
  },

  css: {
    sourceMap: true,
    loaderOptions: {
      scss: {
        additionalData: '@import "@/scss/dsfr.scss";',
      },
    },
  },

  chainWebpack: (config) => {
    config.optimization.splitChunks(false)

    config.plugin("BundleTracker").use(BundleTracker, [{ filename: "../frontend/webpack-stats.json" }])

    config.resolve.alias.set("__STATIC__", "static")

    config.devServer
      .public("http://127.0.0.1:8080")
      .host("127.0.0.1")
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      // eslint-disable-next-line no-useless-escape
      .headers({ "Access-Control-Allow-Origin": ["*"] })
  },
}
