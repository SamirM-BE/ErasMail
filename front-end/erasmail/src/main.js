import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import en from './locales/en.json'
import fr from './locales/fr.json'


import { createI18n } from 'vue-i18n'

const messages = {
    en: en,
    fr: fr
}

const i18n = createI18n({
    locale: 'en',
    messages
})

createApp(App).use(store).use(router).use(i18n).mount('#app')
