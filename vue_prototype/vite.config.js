import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// npm add -D @vitejs/plugin-legacy
import legacy from '@vitejs/plugin-legacy';
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    legacy({
      targets: ["defaults", "not IE 11"],
    })
  ],
  // resolve: {
  //   alias: {
  //     '@': fileURLToPath(new URL('./src', import.meta.url))
  //   }
  // },
  base: './', // 设置为相对路径
  // base: '/vue_test/', // 设置为相对路径
  build: {
    outDir: 'out_file',
  },
})
