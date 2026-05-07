import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Tauri expects a fixed port for the dev server
  server: {
    port: 1420,
    strictPort: true,
  },
  // prevent vite from obscuring rust errors
  clearScreen: false,
})
