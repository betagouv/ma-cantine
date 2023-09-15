module.exports = {
  root: true,

  env: {
    node: true,
  },

  extends: ["eslint:recommended", "plugin:vue/vue3-recommended", "prettier"],

  // parserOptions: {
  //   parser: "@babel/eslint-parser",
  // },

  rules: {
    "vue/no-mutating-props": "off",
    "vue/multi-word-component-names": "off",
    "vue/no-v-text-v-html-on-component": "off",
  },
  plugins: ["prettier"],

  overrides: [
    {
      files: ["**/__tests__/*.{j,t}s?(x)", "**/tests/unit/**/*.spec.{j,t}s?(x)"],
      env: {
        jest: true,
      },
    },
  ],
}
