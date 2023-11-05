import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import eslintPlugin from "vite-plugin-eslint";
import checker from "vite-plugin-checker";
import svgLoader from "vite-svg-loader";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), svgLoader(), eslintPlugin(), checker({ typescript: true, vueTsc: true })],
  base: "./",
  resolve: {
    alias: {
      "@": resolve(__dirname, "./src"),
      "@admin": resolve(__dirname, "../admin/src"),
      "@main": resolve(__dirname, "../main/src"),
      "@beiming-system/types": resolve("../types/src/index"),
      "@beiming-system/hooks": resolve("../hooks/src/index"),
      "@beiming-system/locale": resolve("../locale/src/index"),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "https://www.lamda.nju.edu.cn/learnware/api/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
    port: 5174,
  },
});
