import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import LogIn from '@/views/LogIn.vue'
import Dashboard from '@/views/dashboard/Dashboard.vue'
import Registration from '@/views/dashboard/shift/Registration.vue'
import PrecinctShift from '@/views/dashboard/shift/PrecinctShift.vue'
import Information from '@/views/dashboard/shift/Information.vue'
import SearchInformation from '@/views/dashboard/shift/SearchInformation.vue'

const routes = [
  {
    path: '/',
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
        {
          path: "shift/edit/:id",
          name: "shift-edit",
          component: () => import('@/components/edit/EditShift.vue')
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
        {
          path: 'searchshift',
          component: () => import('@/components/search/SearchShift.vue')
        },
        {
          path: "shift/:id",
          name: "search-shift-detail",
          component: () => import('@/components/search/SearchShiftDetail.vue')
        },
      ]
    },
  ]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requireLogin)  && !store.state.user.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router


