import { createApp } from "vue";
import router from "./router";
import App from "./App.vue";
import "./style.scss";
import "driver.js/dist/driver.css";
import vuetify from "./plugins/vuetify";
import "./plugins/dayjs";
import store from "./store";
import i18n from "./i18n";

createApp(App).use(vuetify).use(router).use(store).use(i18n).mount("#app");
