import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import "./../node_modules/bulma/css/bulma.css"
import "./../node_modules/@fortawesome/fontawesome-free/css/all.css"

createApp(App).use(store).use(router).mount('#app')
