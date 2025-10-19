import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      // Optional: forward API calls to FastAPI during local dev
      "/health": "http://localhost:8000",
      "/setup": "http://localhost:8000",
      "/ask": "http://localhost:8000",
      "/docs": "http://localhost:8000"
    }
  }
});