import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import LogIn from '@/views/LogIn.vue'
import Dashboard from '@/views/dashboard/Dashboard.vue'
import Registration from '@/views/dashboard/shift/Registration.vue'
import PrecinctShift from '@/views/dashboard/shift/PrecinctShift.vue'
import Information from '@/views/dashboard/shift/Information.vue'
import SearchInformation from '@/views/dashboard/shift/SearchInformation.vue'
import Legalization from '@/views/dashboard/offenses/Լegalization.vue'
import RegistrationLegalization from '@/views/dashboard/offenses/RegistrationLegalization.vue'

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
        path: 'shift',
        component: () =>
          import('@/components/registration/RegistrationShift.vue'),
        meta: {
          precinctHeadForbidden: true
        }
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
          component: () =>
            import('@/components/information/EmployeeList.vue'),
        },
        {
          path: 'routelist',
          component: () =>
            import('@/components/information/RouteList.vue'),
        },
        {
          path: 'shitlist',
          component: () =>
            import('@/components/information/ShiftList.vue')
        },
        {
          path: 'employee/:id',
          name: 'person-detail',
          component: () =>
            import('@/components/detail/PersonDetail.vue'),
          meta: {
            dutyOfficerForbidden: true
          }
        },
        {
          path: 'route/:id',
          name: 'route-detail',
          component: () =>
            import('@/components/detail/RouteDetail.vue'),
        },
        {
          path: 'shift/:id',
          name: 'shift-detail',
          component: () =>
            import('@/components/detail/ShiftDetail.vue')
        },
        {
          path: 'shift/edit/:id',
          name: 'shift-edit',
          component: () =>
            import('@/components/edit/EditShift.vue')
        }
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
          component: () => import('@/components/search/SearchShiftDetail.vue'),
          meta: {
            dutyOfficerForbidden: true
          }          
        },
      ]
    },
    {
      path: '/dashboard/legalization',
      name: 'Legalization',
      component: Legalization,
      meta: {
        requireLogin: true,
        dutyOfficerForbidden: true
      }
    },
    {
      path: '/dashboard/legalization/registration_legalization',
      component: RegistrationLegalization,
      meta: {
        requireLogin: true,
        dutyOfficerForbidden: true
      },
      children: [
        {
          path: 'illegal_logging',
          component: () => import('@/components/registration/RegistrationIllegalLogging.vue')
        },
        {
          path: 'poaching',
          component: () => import('@/components/registration/RegistrationPoaching.vue')
        },
        {
          path: 'illegal_fishing',
          component: () => import('@/components/registration/RegistrationIllegalFishing.vue')
        }
      ]
    },
  ]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const user = store.state.user

  if (
    to.matched.some(record => record.meta.requireLogin) &&
    !user.isAuthenticated
  ) {
    return next('/')
  }

  const groups = Array.isArray(user.groups)
    ? user.groups
    : []

  const isDutyOfficer =
    groups.includes('Հերթապահներ')

  const isPrecinctHead =
    groups.includes('Տեղամասի պետեր')

  const isForbiddenForDutyOfficer = to.matched.some(
    record => record.meta.dutyOfficerForbidden === true
  )

  const isForbiddenForPrecinctHead = to.matched.some(
    record => record.meta.precinctHeadForbidden === true
  )

  if (isDutyOfficer && isForbiddenForDutyOfficer) {
    return next('/dashboard/precinct_shift')
  }

  if (isPrecinctHead && isForbiddenForPrecinctHead) {
    return next('/dashboard/precinct_shift')
  }

  return next()
})

export default router


