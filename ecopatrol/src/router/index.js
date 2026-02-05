import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import Home  from '../views/Home.vue'
import LogIn from '@/views/LogIn.vue'
import Dashboard from '@/views/dashboard/Dashboard.vue'
import MyAccount from '@/views/dashboard/MyAccount.vue'
import PersonInformation from '@/views/dashboard/PersonInformation.vue'
import FireAlarm from '@/views/dashboard/FireAlarm.vue'
import EPSAlarm from '@/views/dashboard/EPSAlarm.vue'
import CrimeAlert from '@/views/dashboard/CrimeAlert.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/person_information',
    name: 'PersonInformation',
    component: PersonInformation,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/my-account',
    name: 'MyAccount',
    component: MyAccount,
    meta: {
      requireLogin: true
    }
  },
  // {
  //   path: '/dashboard/firealarm',
  //   name: 'FireAlarm',
  //   component: FireAlarm,
  //   meta: {
  //     requireLogin: true
  //   }
  // },
  {
    path: '/dashboard/firealarm',
    component: FireAlarm,
    meta: { requireLogin: true },
    children: [
      {
        path: 'epsemployee',
        component: () => import('@/components/forms/EpsEmployeeForm.vue')
      },
      {
        path: 'citizen',
        component: () => import('@/components/forms/CityCitizenForm.vue')
      },
      {
        path: 'firecaller',
        component: () => import('@/components/forms/FireAlarmForm.vue')
      },
    ]
  },
  {
    path: '/dashboard/epsalarm',
    name: 'EPSAlarm',
    component: EPSAlarm,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/crimealert',
    name: 'CrimeAlert',
    component: CrimeAlert,
    meta: {
      requireLogin: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requireLogin)  && !store.state.user.isAuthenticated) {
    next('/log-in')
  } else {
    next()
  }
})

export default router
