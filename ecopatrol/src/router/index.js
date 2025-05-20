import { createRouter, createWebHistory } from 'vue-router'
import Home  from '../views/Home.vue'
import SignUp from '@/views/SignUp.vue'
import LogIn from '@/views/LogIn.vue'
import MyAccount from '@/views/dashboard/MyAccount.vue'

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
  },
  ,
  {
    path: '/dashboard/my-account',
    name: 'MyAccount',
    component: MyAccount
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
