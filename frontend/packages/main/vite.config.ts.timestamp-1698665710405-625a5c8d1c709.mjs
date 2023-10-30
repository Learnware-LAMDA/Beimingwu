// vite.config.ts
import { defineConfig } from "file:///Users/qinchengzheng/Nextcloud/Projects/Web/Beiming-System/frontend/node_modules/.pnpm/vite@4.5.0_@types+node@20.8.4_sass@1.60.0/node_modules/vite/dist/node/index.js";
import vue from "file:///Users/qinchengzheng/Nextcloud/Projects/Web/Beiming-System/frontend/node_modules/.pnpm/@vitejs+plugin-vue@4.1.0_vite@4.5.0_vue@3.2.47/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import WindiCSS from "file:///Users/qinchengzheng/Nextcloud/Projects/Web/Beiming-System/frontend/node_modules/.pnpm/vite-plugin-windicss@1.8.10_vite@4.5.0/node_modules/vite-plugin-windicss/dist/index.mjs";
import eslintPlugin from "file:///Users/qinchengzheng/Nextcloud/Projects/Web/Beiming-System/frontend/node_modules/.pnpm/vite-plugin-eslint@1.8.1_eslint@8.43.0_vite@4.5.0/node_modules/vite-plugin-eslint/dist/index.mjs";
import checker from "file:///Users/qinchengzheng/Nextcloud/Projects/Web/Beiming-System/frontend/node_modules/.pnpm/vite-plugin-checker@0.6.2_eslint@8.43.0_typescript@5.2.2_vite@4.5.0_vue-tsc@1.8.19/node_modules/vite-plugin-checker/dist/esm/main.js";
import svgLoader from "file:///Users/qinchengzheng/Nextcloud/Projects/Web/Beiming-System/frontend/node_modules/.pnpm/vite-svg-loader@4.0.0/node_modules/vite-svg-loader/index.js";
import { resolve } from "path";
var vite_config_default = defineConfig({
  resolve: {
    alias: {
      "@beiming-system/types": resolve("../types/src/index"),
      "@beiming-system/hooks": resolve("../hooks/src/index"),
      "@beiming-system/locale": resolve("../locale/src/index")
    }
  },
  plugins: [
    vue(),
    WindiCSS(),
    svgLoader(),
    eslintPlugin(),
    checker({ typescript: true, vueTsc: true })
  ],
  base: "./",
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8088/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, "")
      }
    },
    port: 5173
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvVXNlcnMvcWluY2hlbmd6aGVuZy9OZXh0Y2xvdWQvUHJvamVjdHMvV2ViL0JlaW1pbmctU3lzdGVtL2Zyb250ZW5kL3BhY2thZ2VzL21haW5cIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIi9Vc2Vycy9xaW5jaGVuZ3poZW5nL05leHRjbG91ZC9Qcm9qZWN0cy9XZWIvQmVpbWluZy1TeXN0ZW0vZnJvbnRlbmQvcGFja2FnZXMvbWFpbi92aXRlLmNvbmZpZy50c1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vVXNlcnMvcWluY2hlbmd6aGVuZy9OZXh0Y2xvdWQvUHJvamVjdHMvV2ViL0JlaW1pbmctU3lzdGVtL2Zyb250ZW5kL3BhY2thZ2VzL21haW4vdml0ZS5jb25maWcudHNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tIFwidml0ZVwiO1xuaW1wb3J0IHZ1ZSBmcm9tIFwiQHZpdGVqcy9wbHVnaW4tdnVlXCI7XG5pbXBvcnQgV2luZGlDU1MgZnJvbSBcInZpdGUtcGx1Z2luLXdpbmRpY3NzXCI7XG5pbXBvcnQgZXNsaW50UGx1Z2luIGZyb20gXCJ2aXRlLXBsdWdpbi1lc2xpbnRcIjtcbmltcG9ydCBjaGVja2VyIGZyb20gXCJ2aXRlLXBsdWdpbi1jaGVja2VyXCI7XG5pbXBvcnQgc3ZnTG9hZGVyIGZyb20gXCJ2aXRlLXN2Zy1sb2FkZXJcIjtcbmltcG9ydCB7IHJlc29sdmUgfSBmcm9tIFwicGF0aFwiO1xuXG4vLyBodHRwczovL3ZpdGVqcy5kZXYvY29uZmlnL1xuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKHtcbiAgcmVzb2x2ZToge1xuICAgIGFsaWFzOiB7XG4gICAgICBcIkBiZWltaW5nLXN5c3RlbS90eXBlc1wiOiByZXNvbHZlKFwiLi4vdHlwZXMvc3JjL2luZGV4XCIpLFxuICAgICAgXCJAYmVpbWluZy1zeXN0ZW0vaG9va3NcIjogcmVzb2x2ZShcIi4uL2hvb2tzL3NyYy9pbmRleFwiKSxcbiAgICAgIFwiQGJlaW1pbmctc3lzdGVtL2xvY2FsZVwiOiByZXNvbHZlKFwiLi4vbG9jYWxlL3NyYy9pbmRleFwiKSxcbiAgICB9LFxuICB9LFxuICBwbHVnaW5zOiBbXG4gICAgdnVlKCksXG4gICAgV2luZGlDU1MoKSxcbiAgICBzdmdMb2FkZXIoKSxcbiAgICBlc2xpbnRQbHVnaW4oKSxcbiAgICBjaGVja2VyKHsgdHlwZXNjcmlwdDogdHJ1ZSwgdnVlVHNjOiB0cnVlIH0pLFxuICBdLFxuICBiYXNlOiBcIi4vXCIsXG4gIHNlcnZlcjoge1xuICAgIHByb3h5OiB7XG4gICAgICBcIi9hcGlcIjoge1xuICAgICAgICB0YXJnZXQ6IFwiaHR0cDovL2xvY2FsaG9zdDo4MDg4L1wiLFxuICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXG4gICAgICAgIHJld3JpdGU6IChwYXRoKSA9PiBwYXRoLnJlcGxhY2UoL15cXC9hcGkvLCBcIlwiKSxcbiAgICAgIH0sXG4gICAgfSxcbiAgICBwb3J0OiA1MTczLFxuICB9LFxufSk7XG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQXFhLFNBQVMsb0JBQW9CO0FBQ2xjLE9BQU8sU0FBUztBQUNoQixPQUFPLGNBQWM7QUFDckIsT0FBTyxrQkFBa0I7QUFDekIsT0FBTyxhQUFhO0FBQ3BCLE9BQU8sZUFBZTtBQUN0QixTQUFTLGVBQWU7QUFHeEIsSUFBTyxzQkFBUSxhQUFhO0FBQUEsRUFDMUIsU0FBUztBQUFBLElBQ1AsT0FBTztBQUFBLE1BQ0wseUJBQXlCLFFBQVEsb0JBQW9CO0FBQUEsTUFDckQseUJBQXlCLFFBQVEsb0JBQW9CO0FBQUEsTUFDckQsMEJBQTBCLFFBQVEscUJBQXFCO0FBQUEsSUFDekQ7QUFBQSxFQUNGO0FBQUEsRUFDQSxTQUFTO0FBQUEsSUFDUCxJQUFJO0FBQUEsSUFDSixTQUFTO0FBQUEsSUFDVCxVQUFVO0FBQUEsSUFDVixhQUFhO0FBQUEsSUFDYixRQUFRLEVBQUUsWUFBWSxNQUFNLFFBQVEsS0FBSyxDQUFDO0FBQUEsRUFDNUM7QUFBQSxFQUNBLE1BQU07QUFBQSxFQUNOLFFBQVE7QUFBQSxJQUNOLE9BQU87QUFBQSxNQUNMLFFBQVE7QUFBQSxRQUNOLFFBQVE7QUFBQSxRQUNSLGNBQWM7QUFBQSxRQUNkLFNBQVMsQ0FBQyxTQUFTLEtBQUssUUFBUSxVQUFVLEVBQUU7QUFBQSxNQUM5QztBQUFBLElBQ0Y7QUFBQSxJQUNBLE1BQU07QUFBQSxFQUNSO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
