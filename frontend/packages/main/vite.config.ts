import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vuetify from "vite-plugin-vuetify";
import eslintPlugin from "vite-plugin-eslint";
import checker from "vite-plugin-checker";
import svgLoader from "vite-svg-loader";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@main": resolve(__dirname, "../main/src"),
      "@beiming-system/types": resolve("../types/src/index"),
      "@beiming-system/hooks": resolve("../hooks/src/index"),
      "@beiming-system/locale": resolve("../locale/src/index"),
    },
  },
  plugins: [
    vue(),
    vuetify(),
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
        target: "https://bmwu.cloud/api/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
      "/static": {
        target: "https://bmwu.cloud/static",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/static/, ""),
      },
    },
    port: 5173,
  },
  define: {
    __VUE_I18N_FULL_INSTALL__: true,
    __VUE_I18N_LEGACY_API__: true,
    __INTLIFY_PROD_DEVTOOLS__: false,
  },
});
