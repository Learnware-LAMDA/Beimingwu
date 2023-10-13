import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import WindiCSS from "vite-plugin-windicss";
import eslintPlugin from "vite-plugin-eslint";
import checker from "vite-plugin-checker";
import svgLoader from "vite-svg-loader";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), WindiCSS(), svgLoader(), eslintPlugin(), checker({ typescript: true })],
  base: "./",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@admin": path.resolve(__dirname, "../admin/src"),
      "@main": path.resolve(__dirname, "../main/src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        // target: "http://localhost:5000",
        target: "http://learnware-backend-cluster.learnware:8088/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
