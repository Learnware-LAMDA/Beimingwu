import type { Config } from "tailwindcss";
import colors from "tailwindcss/colors";

export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  corePlugins: {
    preflight: false,
  },
  safeList: [
    "fill-blue-600",
    "fill-green-800",
    "fill-red-800",
    "stroke-blue-600",
    "stroke-green-800",
    "stroke-red-800",
    "bg-organge-600",
  ],
  theme: {
    extend: {
      colors: {
        background: {
          DEFAULT: colors.gray[50],
          light: colors.gray[50],
          dark: colors.neutral[900],
        },
        surface: {
          DEFAULT: colors.white,
          light: colors.white,
          dark: colors.neutral[800],
        },
        primary: {
          DEFAULT: colors.sky[600],
          light: colors.sky[600],
          dark: colors.sky[800],
        },
        "on-primary": {
          DEFAULT: colors.white,
          light: colors.white,
          dark: colors.gray[200],
        },
        secondary: {
          DEFAULT: colors.amber[500],
          light: colors.amber[500],
          dark: colors.amber[700],
        },
        inactive: {
          DEFAULT: colors.gray[400],
          light: colors.gray[400],
          dark: colors.gray[700],
        },
        active: {
          DEFAULT: colors.gray[100],
          light: colors.gray[100],
          dark: colors.gray[800],
        },
        error: {
          DEFAULT: "#B00020",
          light: "#B00020",
          dark: "#900010",
        },
        info: {
          DEFAULT: "#2196F3",
          light: "#2196F3",
          dark: "#2196F3",
        },
        success: {
          DEFAULT: "#4CAF50",
          light: "#4CAF50",
          dark: "#4CAF50",
        },
        warning: {
          DEFAULT: "#FB8C00",
          light: "#FB8C00",
          dark: "#FB8C00",
        },
      },
    },
  },
  darkMode: "class",
  plugins: [],
} satisfies Config;
