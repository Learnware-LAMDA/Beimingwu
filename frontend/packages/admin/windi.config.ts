import { defineConfig } from 'windicss/helpers'

export default defineConfig({
  extract: {
    include: ['{src,../main/src}/**/*.{vue,html,jsx,tsx}'],
    exclude: ['node_modules', '.git'],
  },
})