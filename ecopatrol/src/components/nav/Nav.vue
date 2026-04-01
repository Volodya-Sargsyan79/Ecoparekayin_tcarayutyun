<template>
  <nav  role="navigation" aria-label="main vanigation" style="min-height: 7rem; background: #163820;">
    <div class="container">
      <div style="display: flex; justify-content: space-between;">
        <div class="navbar-brand">
          <router-link to="/dashboard" class="navbar-item">
            <img src="https://eps.am/image/header-logo.png" alt style="max-height: 5rem;" class="img"/>
            <p style="color: #ffffff;">Հայաստանի Հանրապետության<br/>Շրջակա միջավայրի նախարարության<br/>ԷԿՈՊԱՐԵԿԱՅԻՆ ԾԱՌԱՅՈՒԹՅՈՒՆ</p>
          </router-link>
        </div>
        <div class="navbar-brand">
          <router-link to="/dashboard" class="navbar-item">
            <p style="color: #ffffff;">Հայաստանի Հանրապետություն</p>
            <img src="https://ecopatrolservice.am/image/gerb-logo.png" alt style="max-height: 5rem;" class="img"/>
          </router-link>
          <div v-if=this.$store.state.user.isAuthenticated>
            <LogOut />
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import LogOut from './../LogOut.vue';

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