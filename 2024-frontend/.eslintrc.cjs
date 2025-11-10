/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  parserOptions: {
    ecmaVersion: 'latest'
  },
  plugins: [
    'vuejs-accessibility'
  ],
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/eslint-config-prettier/skip-formatting',
    'plugin:vuejs-accessibility/recommended'
  ],
  ignorePatterns: [
    '.gitignore'
  ],
  rules: {
    "vue/multi-word-component-names": "off"
  },
}
