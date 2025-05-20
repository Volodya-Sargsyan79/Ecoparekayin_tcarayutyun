<template>
    <div class="about">
        <div class="hero is-info">
            <div class="hero-body has-text-centered">
                <h1 class="title">My Account</h1>
            </div>
        </div>
        <section class="section">
            <button @click="logout()" class="button" style="background: #163820; color: #ffffff;">
                Log out
            </button>
        </section>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    methods: {
        logout() {
            axios
                .post('/api/ekopatrol/token/logout/')
                .then(response => {
                    console.log('Logged out')
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
                
            axios.defaults.headers.common['Authorization'] = ""
                        
            localStorage.removeItem('token')

            this.$store.commit('removeToken')

            this.$router.push('/')
        }
    }
}
</script>