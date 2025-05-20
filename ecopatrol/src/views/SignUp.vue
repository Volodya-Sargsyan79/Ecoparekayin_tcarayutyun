<template>
    <div class="signup">
        <div class="hero">
            <div class="hero-body has-text-centered">
                <h1 class="title">Sign up</h1>
            </div>
        </div>
    
        <section class="section">
            <div class="container">
                <div class="columns">
                    <div class="column is-4 is-offset-4">
                        <form action="" v-on:submit.prevent="submitForm">
                            <div class="field">
                                <label for="">First name</label>
                                <div class="control">
                                    <input type="text" class="input" v-model="firstName"/>
                                </div>
                            </div>

                            <div class="field">
                                <label for="">Last name</label>
                                <div class="control">
                                    <input type="text" class="input" v-model="lastName"/>
                                </div>
                            </div>

                            <div class="field">
                                <label for="">Email</label>
                                <div class="control">
                                    <input type="email" class="input" v-model="email"/>
                                </div>
                            </div>

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

                            <div class="field">
                                <label for="">Repeat password</label>
                                <div class="control">
                                    <input type="password" class="input" v-model="repassword"/>
                                </div>
                            </div>

                            <div class="field">
                                <label for="">Access</label>
                                <div class="control is-flex">
                                    <div class="control mr-5">
                                        <label for="">DHS </label>
                                        <input type="radio" class="radio" name="Access" v-model="dhs"/> 
                                    </div >
                                    <div class="control mr-5">
                                        <label for="">ES I </label>
                                        <input type="radio" class="radio" name="Access" v-model="esi"/>
                                    </div>
                                    <div class="control">
                                        <label for="">Frames </label>
                                        <input type="radio" class="radio" name="Access" v-model="frames"/>
                                    </div>
                                </div>
                            </div>

                            <div class="notification is-danger" v-if="errors.length">
                                <p v-for="error in errors" v-bind:key="erre">
                                    {{ error }}
                                </p>
                            </div>

                            <div class="field">
                                <div class="control">
                                    <button class="button" style="background: #163820; color: #ffffff;">Sign up</button>
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
            firstName: '',
            lastName: '',
            username: '',
            email: '',
            password: '',
            repassword: '',
            dhs: '',
            esi: '',
            frames: '',
            errors: []
        }
    },
    methods: {
        submitForm() {

            this.errors = []
            
            if (this.firstName === '') {
                this.errors.push('The name is missing!')
            }
            if (this.lastName === ''){
                this.errors.push('The surname is missing!')
            }
            if (this.email === ''){
                this.errors.push('The email is missing!')
            }
            if (this.username === ''){
                this.errors.push('The username is missing!')
            }
            if (this.password === ''){
                this.errors.push('The password is missing!')
            }
            if (this.password !== this.repassword){
                this.errors.push('The password is not matching!')
            }

            if (!this.errors.length) {
                const formData = {
                    firstName: this.firstName,
                    lastName: this.lastName,
                    username: this.username,
                    email: this.email,
                    password: this.password
                }

                axios
                    .post('/api/ekopatrol/users/', formData)
                    .then(response => {
                        this.$router.push('/log-in')
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
