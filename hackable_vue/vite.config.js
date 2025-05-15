import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
	plugins: [vue()],
	resolve: {
		alias: {
			'@': path.resolve(__dirname, './src'),
			'@articles': path.resolve(__dirname, './src/modules/articles'),
		},
	},
	server: {
		host: '0.0.0.0',
		port: 5137,
	},
})
