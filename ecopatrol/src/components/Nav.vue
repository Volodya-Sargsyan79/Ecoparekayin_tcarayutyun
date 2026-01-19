<template>
  <nav  role="navigation" aria-label="main vanigation" style="min-height: 7rem; background: #163820;">
    <div class="container">
      <div style="display: flex; justify-content: space-between;">
        <div class="navbar-brand">
          <a class="navbar-item" href="/">
            <img src="https://eps.am/image/header-logo.png" alt style="max-height: 5rem;" class="img"/>
            <p style="color: #ffffff;">Հայաստանի Հանրապետության<br/>Շրջակա միջավայրի նախարարության<br/>ԷԿՈՊԱՐԵԿԱՅԻՆ ԾԱՌԱՅՈՒԹՅՈՒՆ</p>
          </a>
        </div>
        <div class="navbar-brand">
          <a class="navbar-item" href="/">
            <p style="color: #ffffff;">Հայաստանի Հանրապետության</p>
            <img src="https://ecopatrolservice.am/image/gerb-logo.png" alt style="max-height: 5rem;" class="img"/>
          </a>
          <div v-if=this.$store.state.user.isAuthenticated>
            <LogOut />
          </div>
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