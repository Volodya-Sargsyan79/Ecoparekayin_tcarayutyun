<template>
    <div class="container">
        <div class="columns is-multiline">
            <div class="column is-12">
                <section class="section">
                    <div class="container">
                        <div class="columns is-multiline">
                            <div class="column is-4">
                                <div class="box">
                                    <div class="has-text-centered">
                                         <h2 class="is-size-4 mt-4 mb-4">
                                            ՀՀ ՇՄՆ էկոպարեկային ծառայության աշխատակից
                                        </h2>
                                    </div>

                                    <form action="" v-on:submit.prevent="employeeSearch">
                                        <div class="field">
                                            <label for="">Անուն</label>
                                            <div class="control">
                                                <input type="text" class="input" v-model="employee.first_name"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">Ազգանուն</label>
                                            <div class="control">
                                                <input type="text" class="input" v-model="employee.last_name"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">Անձնագիր</label>
                                            <div class="control">
                                                <input type="text" class="input" v-model="employee.passport"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">Նույնականացման քարտ</label>
                                            <div class="control">
                                                <input type="password" class="input" v-model="employee.id_card"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">ՀՎՀՀ</label>
                                            <div class="control">
                                                <input type="password" class="input" v-model="employee.hvhh"/>
                                            </div>
                                        </div>

                                        <div class="notification is-danger" v-if="errors.length">
                                            <p v-for="error in errors" v-bind:key="erre">
                                                {{ error }}
                                            </p>
                                        </div>

                                        <div class="field">
                                            <div class="control">
                                                <button class="button" style="background: #163820; color: #ffffff;">Փնտրել</button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>

                            <div class="column is-4">
                                <div class="box">
                                    <div class="has-text-centered">
                                         <h2 class="is-size-4 mt-4 mb-4">
                                            Հայաստանի Հանրապետության քաղաքացի
                                        </h2>
                                    </div>

                                    <form action="" v-on:submit.prevent="person">
                                        <div class="field">
                                            <label for="">Անուն</label>
                                            <div class="control">
                                                <input type="text" class="input" v-model="person.first_name"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">Ազգանուն</label>
                                            <div class="control">
                                                <input type="text" class="input" v-model="person.last_name"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">Անձնագիր</label>
                                            <div class="control">
                                                <input type="text" class="input" v-model="person.passport"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">Նույնականացման քարտ</label>
                                            <div class="control">
                                                <input type="password" class="input" v-model="person.id_card"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">ՀՎՀՀ</label>
                                            <div class="control">
                                                <input type="password" class="input" v-model="person.hvhh"/>
                                            </div>
                                        </div>

                                        <div class="notification is-danger" v-if="errors.length">
                                            <p v-for="error in errors" v-bind:key="erre">
                                                {{ error }}
                                            </p>
                                        </div>

                                        <div class="field">
                                            <div class="control">
                                                <button class="button" style="background: #163820; color: #ffffff;">Փնտրել</button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>

                            <div class="column is-4">
                                <div class="box">
                                    <div class="has-text-centered">
                                         <h2 class="is-size-4 mt-4 mb-4">
                                            Խախտումների վերաբերյալ տեղեկություններ
                                        </h2>
                                    </div>

                                    <form action="" v-on:submit.prevent="submitForm">
                                        <div class="field">
                                            <label for="">Անուն</label>
                                            <div class="control">
                                                <input type="text" class="input" v-model="first_name"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">Ազգանուն</label>
                                            <div class="control">
                                                <input type="text" class="input" v-model="last_name"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">Անձնագիր</label>
                                            <div class="control">
                                                <input type="text" class="input" v-model="passport"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">Նույնականացման քարդ</label>
                                            <div class="control">
                                                <input type="password" class="input" v-model="id_card"/>
                                            </div>
                                        </div>

                                        <div class="field">
                                            <label for="">ՀՎՀՀ</label>
                                            <div class="control">
                                                <input type="password" class="input" v-model="hvhh"/>
                                            </div>
                                        </div>

                                        <div class="notification is-danger" v-if="errors.length">
                                            <p v-for="error in errors" v-bind:key="erre">
                                                {{ error }}
                                            </p>
                                        </div>

                                        <div class="field">
                                            <div class="control">
                                                <button class="button" style="background: #163820; color: #ffffff;">Փնտրել</button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div> 
</template>

<script>
    import axios from 'axios';
    export default {
        name: 'Dashboard',
        components: {
            
        },
        data() {
            return {
                employee: {
                    first_name: "",
                    last_name: "",
                    passport: "",
                    id_card: "",
                    hvhh: "",
                },
                person: {
                    first_name: "",
                    last_name: "",
                    passport: "",
                    id_card: "",
                    hvhh: "",
                },
                errors: []
            }
        },
        methods: {
            employeeSearch() {
                this.errors = []

                this.$store.commit('setIsLoading', true)

                axios
                    .get('/api/ekopatrol/employee/', {
                        params: {
                            first_name: this.employee.first_name,
                            last_name: this.employee.last_name,
                            passport: this.employee.passport,
                            id_card: this.employee.id_card,
                            hvhh: this.employee.hvhh
                        }
                    })
                    .then(response => {
                        this.$store.state.user.employee = response.data
                        this.$router.push('/dashboard/employee')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again')
                            console.log(JSON.stringify(error))
                        }
                    }) 

                this.$store.commit('setIsLoading', false)
            
            },
            person() {
                this.errors = []

                this.$store.commit('setIsLoading', true)

                axios
                    .get('/api/ekopatrol/employee/', {
                        params: {
                            first_name: this.person.first_name,
                            last_name: this.person.last_name,
                            passport: this.person.passport,
                            id_card: this.person.id_card,
                            hvhh: this.person.hvhh
                        }
                    })
                    .then(response => {
                        this.$store.state.user.person = response.data
                        this.$router.push('/dashboard/employee')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }
                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again')
                            console.log(JSON.stringify(error))
                        }
                    }) 

                this.$store.commit('setIsLoading', false)
            
            }
        }
    }
</script>