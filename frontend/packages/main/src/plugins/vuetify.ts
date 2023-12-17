import "@mdi/font/css/materialdesignicons.css"; // Ensure you are using css-loader
import { createVuetify } from "vuetify";
import tailwindConfig from "../../tailwind.config";

const lightColors = Object.fromEntries(
  Object.entries(tailwindConfig.theme.extend.colors).map(([key, value]) => [key, value.light]),
);
const darkColors = Object.fromEntries(
  Object.entries(tailwindConfig.theme.extend.colors).map(([key, value]) => [key, value.dark]),
);

const light = {
  dark: false,
  colors: lightColors,
};

const dark = {
  dark: true,
  colors: darkColors,
};

export default createVuetify({
  theme: {
    defaultTheme: "light",
    themes: {
      light,
      dark,
    },
  },
});
