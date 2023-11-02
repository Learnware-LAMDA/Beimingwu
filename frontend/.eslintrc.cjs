module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:vue/vue3-essential",
    "plugin:@typescript-eslint/recommended",
    "plugin:vuetify/base",
  ],
  overrides: [],
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: "@typescript-eslint/parser",
    ecmaVersion: 2020,
    sourceType: "module",
    project: "./tsconfig.eslint.json",
    tsconfigRootDir: __dirname,
    extraFileExtensions: [".vue"],
  },
  ignorePatterns: ["node_modules", "dist", "public", ".eslintrc.cjs", "encrypt.ts"],
  plugins: ["@typescript-eslint", "vue"],
  rules: {
    "vue/multi-word-component-names": "off",
    "@typescript-eslint/explicit-function-return-type": "error",
  },
};
