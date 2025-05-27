<template>
  <nav class="navbar" role="navigation" aria-label="main vanigation" style="min-height: 7rem; background: #163820;">
    <div class="navbar-brand">
      <a class="navbar-item" href="/">
        <img src="https://eps.am/image/header-logo.png" alt style="max-height: 5rem;" class="img"/>
        <p style="color: #ffffff;">Eco-patrol Service of the <br/> Ministry of Environment</p>
      </a>
    </div>

    <div id="navbar-item" class="navbar-menu">
      <div class="navbar-start">
        <a class="navbar-item" href="/sign-up">Home</a>
        <a class="navbar-item" href="https://eps.am/">About</a>
      </div>
    </div>
    <div v-if=this.$store.state.user.isAuthenticated>
      <LogOut />
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