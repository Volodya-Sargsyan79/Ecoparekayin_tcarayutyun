import { createRouter, createWebHistory } from 'vue-router'
import Home  from '../views/Home.vue'
import SignUp from '@/views/SignUp.vue'
import LogIn from '@/views/LogIn.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
