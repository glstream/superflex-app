import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
// import 'ant-design-vue/dist/reset.css'
import 'primevue/resources/themes/aura-light-green/theme.css'
import PrimeVue from 'primevue/config'

import 'primevue/resources/themes/aura-light-green/theme.css'
import 'primevue/resources/primevue.min.css' /* Deprecated */
import './style.css'
import './flags.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Antd)
app.use(PrimeVue)

app.mount('#app')
