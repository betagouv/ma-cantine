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
  },

  chainWebpack: (config) => {
    config.optimization.splitChunks(false)

    config.plugin("BundleTracker").use(BundleTracker, [{ path: "../frontend/", filename: "webpack-stats.json" }])

    config.resolve.alias.set("__STATIC__", "static")

    config.devServer
      .public("http://127.0.0.1:8080")
      .host("127.0.0.1")
      .port(8080)
      .hot("only")
      .https(false)
      .headers({ "Access-Control-Allow-Origin": ["*"] })
  },
}
