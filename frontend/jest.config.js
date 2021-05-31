module.exports = {
  preset: "@vue/cli-plugin-unit-jest",
  setupFiles: ["./tests/setup.js"],
  moduleNameMapper: {
    "\\.(scss|sass|css|less)$": "identity-obj-proxy",
  },
}
