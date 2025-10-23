<template>
    <div class="menu">
        <div class="has-text-centered">
            <h2 class="is-size-4 mt-4 mb-4" @click="person(this.$store.state.user.persons.id)" style="cursor: pointer;">
                <br/>{{ $store.state.user.persons.first_name }} {{ $store.state.user.persons.last_name }}<br/>
            </h2>
        </div>
        <MenuItem 
            v-for="(item, index) in menuTree"
            :key="index"
            :label="item.label"
            :title="item.title"
            :func="item.func"
            :depth="0"
            :data="item.children"
        />
    </div>
</template>

<script>
    import axios from 'axios';
    import MenuItem from './MenuItem.vue';
    export default {
        name: 'recursive-menu',
        data() {
            return {
                menuTree: [
                    {
                        label: 'Կապեր',
                        children: [
                            {
                                label: 'Հարազատներ',
                                title: "Հ",
                                func: this.personRelatives,
                            },
                            {
                                label: 'Բարեկամներ',
                                title: "Բ",
                                func: this.personRelatives,
                            },
                            {
                                label: 'Ընկերներ',
                                title: "Ը",
                                func: this.personRelatives,
                            },
                            {
                                label: 'Կապեր',
                                title: "Կ",
                                func: this.personRelatives,
                            },
                        ]
                    },
                    {
                        label: 'Ուսում',
                        func: this.personStudy,
                    },
                    {
                        label: 'Ծառայություն',
                        func: this.personSoldier,
                    },
                    {
                        label: 'Աշխատանք',
                        func: this.personWork,
                    },
                    {
                        label: 'Տուժեր և խրախուսանքներ',
                         children: [
                            {
                                label: 'Տուժեր',
                            },
                            {
                                label: 'Խրախուսանքներ',
                            },
                        ]
                    },
                    {
                        label: 'Խախտումներ',
                         children: [
                            {
                                label: 'Վարչական տուժ',
                            },
                            {
                                label: 'Դատվածություն',
                            },
                        ]
                    },
                    {
                        label: 'Անշարժ գույք',
                        func: this.personProperty,
                    },
                    {
                        label: 'Մեքենա',
                        func: this.personCar,
                    },
                    {
                        label: 'Փաստաթղթեր',
                    },
                    {
                        label: 'Այլ տեղեկատվություն',
                    },
                ]
            }
            
        },
        components: {
            MenuItem
        },
        methods: {
             async person(id) {
            
                this.errors = []

                this.$store.commit('setIsLoading', true)

                try {
                    // 1. Search for person
                    const personRes = await axios.get('/api/ekopatrol/person/', {
                        params: {
                            id: id
                        }
                    });
    
                    this.$store.state.user.person = personRes.data[0];
                     this.$store.state.user.persons = personRes.data[0];

                    const personId = this.$store.state.user.person?.id;
                    
                    if (!personId) throw new Error("Person ID not found");

                    // 2. Get phone info
                    const phoneRes = await axios.get('/api/ekopatrol/person/phone/', {
                        params: { id: personId }
                    });
                    this.$store.state.user.phone = phoneRes.data;

                    // 3. Get address info
                    const addressRes = await axios.get('/api/ekopatrol/person/address/', {
                        params: { id: personId }
                    });
                    this.$store.state.user.address = addressRes.data;

                    // 4. Navigate
                    this.$router.push('/dashboard/person_information');

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
            
            },
            personRelatives(title) {
                
                 axios
                    .get('/api/ekopatrol/person/relatives/', {
                        params: {
                            id: this.$store.state.user.persons.id,
                            registration: title
                        }
                    })
                    .then(response => {
                        this.$store.state.user.person = response.data
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
            },
            personStudy() {
                axios
                    .get('/api/ekopatrol/person/study/', {
                        params: {
                            id: this.$store.state.user.persons.id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.person = response.data
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
            },
            personSoldier() {
                axios
                    .get('/api/ekopatrol/person/soldier/', {
                        params: {
                            id: this.$store.state.user.persons.id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.person = response.data
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
            },
            personWork() {
                axios
                    .get('/api/ekopatrol/person/work/', {
                        params: {
                            id: this.$store.state.user.persons.id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.person = response.data
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
            },
            personProperty() {

                axios
                    .get('/api/ekopatrol/person/address/', {
                        params: {
                            id: this.$store.state.user.persons.id
                        }
                    })
                    .then(response => {
                        
                        this.$store.state.user.person = response.data.filter(item => item.registration === "Սեփականություն")

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
            },
            personCar() {

                axios
                    .get('/api/ekopatrol/person/car/', {
                        params: {
                            id: this.$store.state.user.persons.id
                        }
                    })
                    .then(response => {
                        
                        this.$store.state.user.person = response.data

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
            }
        }
    }
</script>

<style lang="scss" scoped>
    .menu {
        width: 100%;
        transition: all .3s ease;
        overflow: auto;
    }
</style>