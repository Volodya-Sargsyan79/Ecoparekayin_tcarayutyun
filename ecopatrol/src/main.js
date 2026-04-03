import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import axios from 'axios'

// Vuetify imports
import { createVuetify } from 'vuetify'
import 'vuetify/styles'

// Axios configuration
// axios.defaults.baseURL = `http://${window.location.hostname}:8000`
axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true

// Create Vuetify instance
const vuetify = createVuetify()

// Create app
const app = createApp(App)

// Global properties
// app.config.globalProperties.$hostname = window.location.hostname

// Use plugins
app.use(store)
app.use(router)
app.use(vuetify)

// Mount app
app.mount('#app')