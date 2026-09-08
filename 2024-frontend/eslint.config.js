import js from '@eslint/js'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'
import pluginVue from 'eslint-plugin-vue'
import pluginVueA11y from 'eslint-plugin-vuejs-accessibility'

export default [
  {
    files: ['**/*.{js,mjs,cjs,vue}']
  },
  {
    ignores: ['dist/**', 'public/**']
  },
  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  ...pluginVueA11y.configs['flat/recommended'],
  skipFormatting,
  {
    rules: {
      'vue/multi-word-component-names': 'off'
    }
  }
]
