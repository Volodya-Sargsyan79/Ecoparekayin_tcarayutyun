import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      token: '',
      id: null,
      is_admin: false,
      relatives: "",
      regions: "",
      precincts: "",
      region_id: null,
      position: "",
      stationshif: null,
      employee: null,
      car: null,
      route: null,
      persons: null,
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
      } else {
        state.user.token = ''
        state.user.isAuthenticated = false
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
    },
    SET_FIRELIST(state, payload) {
      state.user.firelist = payload
    },
    setUser(state, user) {
      state.user.id = user.id
      state.user.is_admin = user.is_admin
    },
  },
  actions: {
  },
  modules: {
  }
})
