<template>
  <nav  role="navigation" aria-label="main vanigation" style="min-height: 7rem; background: #163820;">
    <div class="container">
      <div style="display: flex; justify-content: space-between;">
        <div class="navbar-brand">
          <a class="navbar-item" href="/">
            <img src="https://eps.am/image/header-logo.png" alt style="max-height: 5rem;" class="img"/>
            <p style="color: #ffffff;">Eco-patrol Service of the <br/> Ministry of Environment</p>
          </a>
        </div>

        <div v-if=this.$store.state.user.isAuthenticated>
          <LogOut />
        </div>
      </div>

      <div id="navbar-item" class="navbar-menu">
        <div class="navbar-start" style="color: #ffffff;">
          <a class="navbar-item" href="/dashboard">Home</a>
          <a class="navbar-item" href="https://eps.am/">About</a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import LogOut from './LogOut.vue';

export default {
    name: 'Nav',
    components: {
            LogOut
    },
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    }
}
</script>