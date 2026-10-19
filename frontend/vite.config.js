import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// The frontend talks to the backend only through /api.
// Locally the backend runs on :8000; in Docker Compose it is the "backend" service.
const backendUrl = process.env.BACKEND_URL ?? 'http://localhost:8000'
const proxy = { '/api': backendUrl }

export default defineConfig({
  plugins: [vue()],
  server: { host: true, proxy }, // npm run dev
  preview: { host: true, proxy }, // vite preview (Docker)
})
