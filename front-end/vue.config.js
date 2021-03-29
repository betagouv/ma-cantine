module.exports = {
  css: {
    loaderOptions: {
      sass: {
        additionalData: '@import "@/styles/_variables.scss";'
      }
    }
  },
  // devServer: {
  //   proxy: {
  //     '^/api/': {
  //       target: 'http://localhost:3000',
  //       changeOrigin: true,
  //       logLevel: "debug"
  //     },
  //   }
  // }
}