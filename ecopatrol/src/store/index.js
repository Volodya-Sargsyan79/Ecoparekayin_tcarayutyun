import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      token: '',
      relatives: "",
      regions: "",
      precincts: "",
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
    }
  },
  actions: {
  },
  modules: {
  }
})
