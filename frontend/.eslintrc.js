module.exports = {
  root: true,

  env: {
    node: true,
  },

  extends: ["plugin:vue/essential", "eslint:recommended", "plugin:prettier/recommended"],

  parserOptions: {
    parser: "babel-eslint",
  },

  rules: {
    "vue/no-mutating-props": "off",
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
