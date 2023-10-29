import { defineConfig } from "windicss/helpers";

export default defineConfig({
  extract: {
    include: ["{src,../admin/src}/**/*.{vue,html,jsx,tsx}"],
    exclude: ["node_modules", ".git"],
  },
});
