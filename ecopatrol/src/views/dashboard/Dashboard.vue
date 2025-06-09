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
                                            Հայաստանի Հանրապետության քաղաքացի
                                        </h2>
                                    </div>

                                    <form action="" v-on:submit.prevent="personSearch">
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
            async personSearch() {
                this.errors = []

                try {
                    // 1. Search for person
                    const personRes = await axios.get('/api/ekopatrol/person/', {
                        params: {
                            first_name: this.person.first_name,
                            last_name: this.person.last_name,
                            passport: this.person.passport,
                            id_card: this.person.id_card,
                            hvhh: this.person.hvhh
                        }
                    });
    
                    if (personRes.data.length > 1) {
                        this.$store.state.user.person = personRes.data;

                        this.$router.push('/dashboard/person_information');
                    } else {
                        this.$store.state.user.person = personRes.data[0];

                        const personId = this.$store.state.user.person?.id;
                        
                        if (!personId) throw new Error("Person ID not found");

                        // 2. Get phone info
                        const phoneRes = await axios.get('/api/ekopatrol/person/phone/', {
                            params: { person_id: personId }
                        });
                        this.$store.state.user.phone = phoneRes.data;

                        // 3. Get address info
                        const addressRes = await axios.get('/api/ekopatrol/person/address/', {
                            params: { person_id: personId }
                        });
                        this.$store.state.user.address = addressRes.data;

                        // 4. Navigate
                        this.$router.push('/dashboard/person_information');
                    }

                } catch (error) {
                    if (error.response && error.response.data) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`);
                        }
                        console.log(JSON.stringify(error.response.data));
                    } else {
                        this.errors.push('Something went wrong. Please try again');
                        console.log(error.message || error);
                    }
                } finally {
                    this.$store.commit('setIsLoading', false);
                }             

                this.$store.commit('setIsLoading', false)
            
            }
        }
    }
</script>