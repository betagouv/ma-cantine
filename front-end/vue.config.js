module.exports = {
  css: {
    loaderOptions: {
      sass: {
        additionalData: '@import "@/styles/_variables.scss";'
      }
    }
  },
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.md$/i,
          loader: "raw-loader",
        },
      ],
    },
  },
}