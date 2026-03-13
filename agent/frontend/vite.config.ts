import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    commonjsOptions: {
      // Vite's CJS→ESM transform only covers node_modules by default.
      // The generated protobuf files in src/generated/ use CommonJS
      // require() calls (goog.object.extend, google-protobuf), so they
      // must be explicitly included here or `require` stays in the bundle
      // and crashes in the browser.
      include: [/node_modules/, /src\/generated\//],
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://controller:8000',
        changeOrigin: true,
      },
    },
  },
})
