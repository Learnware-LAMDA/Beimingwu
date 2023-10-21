import { createApp } from "vue";
import router from "./router";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import store from "@main/store";
import i18n from "@main/i18n";

// windicss
import "virtual:windi.css";

createApp(App).use(vuetify).use(router).use(store).use(i18n).mount("#app");
