import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      token: '',
      id: null,
      username: '',
      is_admin: false,
      groups: [],
      region_id: null,
      precinct_id: null,
      relatives: "",
      regions: "",
      precincts: "",
      position: "",
      stationshif: null,
      employee: null,
      car: null,
      route: null,
      persons: null,
      creater: null,
      call_list: null,
      filelist: null,
      isLoading: false,
      isAuthenticated: false
    }
  },
  getters: {
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {

          state.user.token = localStorage.getItem('token')
          state.user.isAuthenticated = true

          state.user.groups =
              JSON.parse(localStorage.getItem('groups') || '[]')

          state.user.region_id =
              Number(localStorage.getItem('region_id'))

          state.user.precinct_id =
              Number(localStorage.getItem('precinct_id'))

      } else {

          state.user.token = ''
          state.user.isAuthenticated = false
          state.user.groups = []

      }
    },
    setIsLoading(state, status) {
      state.user.isLoading = status
    },
    setToken(state, token) {
      state.user.token = token
      state.user.isAuthenticated = true
    },
    removeToken(state) {
      state.user.token = ''
      state.user.isAuthenticated = false
      state.user.groups = []

      localStorage.removeItem('token')
      localStorage.removeItem('groups')
      localStorage.removeItem('region_id')
      localStorage.removeItem('precinct_id')
    },
    SET_FIRELIST(state, payload) {
      state.user.firelist = payload
    },
    setUser(state, user) {
        state.user.id = user.id
        state.user.username = user.username
        state.user.is_admin = user.is_admin
        state.user.groups = user.groups || []
        state.user.region_id = user.region_id
        state.user.precinct_id = user.precinct_id

        localStorage.setItem('groups', JSON.stringify(state.user.groups))
        localStorage.setItem('region_id', user.region_id)
        localStorage.setItem('precinct_id', user.precinct_id)
    },
    setCallList(state, callList) {
      state.user.call_list = callList
    },
  },
  actions: {
  },
  modules: {
  }
})
