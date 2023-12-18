import { createApp } from "vue";
import router from "./router";
import App from "./App.vue";
import vuetify from "@main/plugins/vuetify";
import "@main/plugins/dayjs";
import store from "@main/store";
import i18n from "@main/i18n";
import "@main/style.scss";
import "driver.js/dist/driver.css";

createApp(App).use(vuetify).use(router).use(store).use(i18n).mount("#app");
