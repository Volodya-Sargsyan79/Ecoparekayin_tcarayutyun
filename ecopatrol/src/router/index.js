import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import Home  from '../views/Home.vue'
import LogIn from '@/views/LogIn.vue'
import Dashboard from '@/views/dashboard/Dashboard.vue'
import Registration from '@/views/dashboard/shift/Registration.vue'
import PrecinctShift from '@/views/dashboard/shift/PrecinctShift.vue'
import Information from '@/views/dashboard/shift/Information.vue'
import SearchInformation from '@/views/dashboard/shift/SearchInformation.vue'

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
    path: '/dashboard/precinct_shift',
    name: 'PrecinctShift',
    component: PrecinctShift,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/precinct_shift/registration',
    component: Registration,
    meta: { requireLogin: true },
    children: [
      {
        path: 'employee',
        component: () => import('@/components/registration/RegistrationEmployee.vue')
      },
      {
        path: 'shift',
        component: () => import('@/components/registration/RegistrationShift.vue')
      },
      {
        path: 'route',
        component: () => import('@/components/registration/RegistrationRoute.vue')
      }
    ]
  },
  {
      path: '/dashboard/precinct_shift/information',
      name: 'Information',
      component: Information,
      meta: {
        requireLogin: true
      },
      children: [
        {
          path: 'employeelist',
          component: () => import('@/components/information/EmployeeList.vue')
        },
        {
          path: 'routelist',
          component: () => import('@/components/information/RouteList.vue')
        },
        {
          path: 'shitlist',
          component: () => import('@/components/information/ShiftList.vue')
        },
        {
          path: "employee/:id",
          name: "person-detail",
          component: () => import('@/components/detail/PersonDetail.vue')
        },
        {
          path: "route/:id",
          name: "route-detail",
          component: () => import('@/components/detail/RouteDetail.vue')
        },
        {
          path: "shift/:id",
          name: "shift-detail",
          component: () => import('@/components/detail/ShiftDetail.vue')
        },
      ]
    },
    {
      path: '/dashboard/precinct_shift/search_information',
      name: 'SearchInformation',
      component: SearchInformation,
      meta: {
        requireLogin: true
      },
      children: [
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
