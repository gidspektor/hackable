import pluginVue from 'eslint-plugin-vue'
import vueEslintConfig from '@vue/eslint-config'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'

export default [
	{
		name: 'app/files-to-lint',
		files: ['**/*.{mts,vue}'],
	},

	{
		name: 'app/files-to-ignore',
		ignores: ['**/dist/**', '**/dist-ssr/**', '**/coverage/**'],
	},

	...pluginVue.configs['flat/essential'],
	...vueEslintConfig(),
	skipFormatting,
]
