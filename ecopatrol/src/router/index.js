import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import Home  from '../views/Home.vue'
import LogIn from '@/views/LogIn.vue'
import Dashboard from '@/views/dashboard/Dashboard.vue'
import RegionInfo from '@/views/dashboard/RegionInfo.vue'
import Register from '@/views/dashboard/ShitRegister.vue'
import CreateMonthlyDuty from '@/views/dashboard/CreateMonthlyDuty.vue'
import ShitDuty from '@/views/dashboard/ShitDuty.vue'
import CreateDuty from '@/views/dashboard/CreateDuty.vue'

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
    path: '/dashboard/regioninfo',
    name: 'RegionInfo',
    component: RegionInfo,
    meta: { requireLogin: true },
    children: [
      {
        path: 'employeelist',
         component: () => import('@/components/forms/EmployeeList.vue')
      },
      {
        path: 'routelist',
        component: () => import('@/components/forms/RouteList.vue')
      },
      {
        path: 'shitlist',
        component: () => import('@/components/forms/ShitListForm.vue')
      },
      {
        path: "route/:id",
        name: "route-detail",
        component: () => import('@/components/detail/RouteDetail.vue')
      },
      {
        path: "person/:id",
        name: "person-detail",
        component: () => import('@/components/detail/PersonDetail.vue')
      },
      {
        path: "shift/:id",
        name: "shift-detail",
        component: () => import('@/components/detail/ShiftDetail.vue')
      },
    ]
  },
  {
    path: '/dashboard/createmonthlyduty',
    name: 'CreateMonthlyDuty',
    component: CreateMonthlyDuty,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/createmonthlyduty/shitduty',
    name: 'ShitDuty',
    component: ShitDuty,
    meta: {
      requireLogin: true
    },
    children: [
      {
        path: 'shitlist',
        component: () => import('@/components/forms/ShitListForm.vue')
      }
    ]
  },
  {
    path: '/dashboard/createmonthlyduty/createduty',
    name: 'CreateDuty',
    component: CreateDuty,
    meta: {
      requireLogin: true
    },
    children: [
      {
        path: 'shitlist',
        component: () => import('@/components/forms/ShitListForm.vue')
      },
       {
        path: 'createshit',
        component: () => import('@/components/forms/CreateShit.vue')
      }
    ]
  },
  {
    path: '/dashboard/register',
    component: Register,
    meta: { requireLogin: true },
    children: [
      {
        path: 'epsemployee',
        component: () => import('@/components/forms/EpsEmployeeForm.vue')
      },
      {
        path: 'regionshift',
        component: () => import('@/components/forms/RegionShift.vue')
      },
      {
        path: 'regionroute',
        component: () => import('@/components/forms/RegionRouteForm.vue')
      },
      {
        path: 'employeelist',
        component: () => import('@/components/forms/EmployeeList.vue')
      },
      {
        path: 'shitlist',
        component: () => import('@/components/forms/ShitListForm.vue')
      },
      {
        path: 'routelist',
        component: () => import('@/components/forms/RouteList.vue')
      }
    ]
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
