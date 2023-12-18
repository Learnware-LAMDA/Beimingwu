import type { Config } from "tailwindcss";
import tailwindConfig from "../main/tailwind.config";

export default {
  ...tailwindConfig,
  content: [...tailwindConfig.content, "../main/src/**/*.{vue,js,ts,jsx,tsx}"],
} satisfies Config;
