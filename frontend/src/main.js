import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './Routes.vue'
import axios from 'axios'

const app = createApp(App)
app.config.globalProperties.$axios = axios
app.provide('axios', axios)

app.use(router)
app.mount('#app')
