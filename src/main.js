import { createApp } from 'vue'
import './style.css'
import router from './router'
import App from './App.vue'
import vuetify from './plugins/vuetify'

// windicss
import 'virtual:windi.css'

createApp(App)
    .use(vuetify)
    .use(router)
    .mount('#app')
