import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'

axios.defaults.baseURL = `http://${window.location.hostname}:8000`
axios.defaults.withCredentials = true

const vuetify = createVuetify()
const app = createApp(App)

app.config.globalProperties.$hostname = window.location.hostname
app.use(store)
app.use(router)
app.use(vuetify)
app.mount('#app')