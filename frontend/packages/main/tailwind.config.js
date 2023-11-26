/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
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
    extend: {},
  },
  plugins: [],
  important: true,
};
