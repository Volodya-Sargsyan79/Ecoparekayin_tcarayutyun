// import { createApp } from 'vue'
// import App from './App.vue'
// import router from './router'
// import store from './store'

// import axios from 'axios'

// import { createVuetify } from 'vuetify'
// import 'vuetify/styles'

// const vuetify = createVuetify()

// axios.defaults.baseURL = 'http://127.0.0.1:8000'
// axios.defaults.withCredentials = true;

// createApp(App).use(store).use(router, axios).use(vuetify).mount('#app')

// 1. Imports at the top
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import axios from 'axios'

// Vuetify imports
import { createVuetify } from 'vuetify'
import 'vuetify/styles'

// 2. Axios configuration
axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true

// 3. Create Vuetify instance
const vuetify = createVuetify()

// 4. Create app
const app = createApp(App)

// 5. Use plugins
app.use(store)
app.use(router)
app.use(vuetify)

// 6. Mount app
app.mount('#app')