<template>
    <div class="login">
        <div class="hero">
            <div class="hero-body has-text-centered">
                <h1 class="title">Log in</h1>
            </div>
        </div>
    
        <section class="section">
            <div class="container">
                <div class="columns">
                    <div class="column is-4 is-offset-4">
                        <form action="" v-on:submit.prevent="submitForm">
                            <div class="field">
                                <label for="">Username</label>
                                <div class="control">
                                    <input type="text" class="input" v-model="username"/>
                                </div>
                            </div>

                            <div class="field">
                                <label for="">Password</label>
                                <div class="control">
                                    <input type="password" class="input" v-model="password"/>
                                </div>
                            </div>

                            <div class="notification is-danger" v-if="errors.length">
                                <p v-for="error in errors" v-bind:key="erre">
                                    {{ error }}
                                </p>
                            </div>

                            <div class="field">
                                <div class="control">
                                    <button class="button" style="background: #163820; color: #ffffff;">Log in</button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'SignUp',
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    methods: {
        submitForm() {
            axios.defaults.headers.common['Authorization'] = ""

            localStorage.removeItem('token')
            
            this.errors = []
            
            if (this.username === ''){
                this.errors.push('The username is missing!')
            }
            if (this.password === ''){
                this.errors.push('The password is missing!')
            }

            if (!this.errors.length) {
                const formData = {
                    username: this.username,
                    password: this.password
                }

                axios
                    .post('/api/ekopatrol/token/login/', formData)
                    .then(response => {
                        const token = response.data.auth_token
                        
                        this.$store.commit('setToken', token)
                        
                        axios.defaults.headers.common['Authorization'] = "Token " + token
                        
                        localStorage.setItem('token', token)
                        
                        this.$router.push('/dashboard/my-account')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${errors.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again')
                            console.log(JSON.stringify(error))
                        }
                    }) 
            }
        }
    }
}
</script>
