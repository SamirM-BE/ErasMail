import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";


import "./../node_modules/bulma/css/bulma.css"
import "./../node_modules/@fortawesome/fontawesome-free/css/all.css"

const toastOptions = {
    position: "top-left",
    timeout: 5000,
    icon: "fas fa-trophy",
    closeOnClick: false,
    onClick: () => router.push({name: 'user'})
}

createApp(App).use(store).use(router).use(Toast, toastOptions).mount('#app')
