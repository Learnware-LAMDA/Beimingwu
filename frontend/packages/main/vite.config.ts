import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import eslintPlugin from "vite-plugin-eslint";
import checker from "vite-plugin-checker";
import svgLoader from "vite-svg-loader";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@beiming-system/types": resolve("../types/src/index"),
      "@beiming-system/hooks": resolve("../hooks/src/index"),
      "@beiming-system/locale": resolve("../locale/src/index"),
    },
  },
  plugins: [
    vue(),
    svgLoader(),
    eslintPlugin({
      cache: false,
      emitWarning: true,
      emitError: true,
      include: ["src/**/*.vue", "src/**/*.ts"],
      exclude: ["node_modules", "dist"],
    }),
    checker({ typescript: true, vueTsc: true }),
  ],
  base: "./",
  server: {
    proxy: {
      "/api": {
        target: "https://www.lamda.nju.edu.cn/learnware/api/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
    port: 5173,
  },
});
