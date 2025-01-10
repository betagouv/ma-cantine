const BundleTracker = require("webpack-bundle-tracker")
const debug = !process.env.DEBUG || process.env.DEBUG === "True"

const FRONTEND_URL = "http://localhost:8080"

const publicPath = debug ? FRONTEND_URL : "/static/"

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
      sass: {
        sassOptions: {
          silenceDeprecations: ["slash-div", "legacy-js-api", "global-builtin", "import"],
        },
      },
    },
  },

  chainWebpack: (config) => {
    config.optimization.splitChunks(false)

    config.plugin("BundleTracker").use(BundleTracker)

    config.resolve.alias.set("__STATIC__", "static")

    config.devServer
      .public(FRONTEND_URL)
      .host("0.0.0.0")
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      // eslint-disable-next-line no-useless-escape
      .headers({ "Access-Control-Allow-Origin": ["*"] })
  },
}
