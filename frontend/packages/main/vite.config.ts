import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import WindiCSS from "vite-plugin-windicss";
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
    WindiCSS(),
    svgLoader(),
    eslintPlugin(),
    checker({ typescript: true, vueTsc: true }),
  ],
  base: "./",
  server: {
    proxy: {
      "/api": {
        //target: "http://localhost:5000/",
        target: "http://learnware-backend-cluster.learnware:8088/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
    port: 5173,
  },
});
