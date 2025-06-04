<template>
    <div class="menu">
        <div class="has-text-centered">
            <h2 class="is-size-4 mt-4 mb-4">
                Տեղեկատվություն<br/>{{ this.$store.state.user.person[0].first_name }} {{ this.$store.state.user.person[0].last_name }}ի<br/>վերաբերյալ
            </h2>
        </div>
        <MenuItem 
            v-for="(item, index) in menuTree"
            :key="index"
            :label="item.label"
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
                                func: this.personRelatives,
                            },
                            {
                                label: 'Բարեկամներ',
                                func: this.personPals,
                            },
                            {
                                label: 'Ընկերներ',
                                func: this.personFriends,
                            },
                            {
                                label: 'Կապեր',
                                func: this.personRelation,
                            },
                        ]
                    },
                    {
                        label: 'Ուսում',
                    },
                    {
                        label: 'Ծառայություն',
                    },
                    {
                        label: 'Աշխատանք',
                        func: this.workList,
                    },
                    {
                        label: 'Տուժեր և խրախուսանքներ',
                         children: [
                            {
                                label: 'Տուժեր',
                            },
                            {
                                label: 'Խրախուսանքներ',
                                func: this.personPals,
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
                        label: 'Սեփականություն',
                        children: [
                            {
                                label: 'Անշարժ գույք',
                            },
                            {
                                label: 'Մեքենա',
                            }
                        ]
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
            personRelatives() {
                 axios
                    .get('/api/ekopatrol/person/relatives/', {
                        params: {
                            id: this.$store.state.user.person[0].id
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
            personPals() {
                 axios
                    .get('/api/ekopatrol/person/pals/', {
                        params: {
                            id: this.$store.state.user.person[0].id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.pals = response.data
                        console.log(this.$store.state.user.pals)
                        // this.$router.push(/dashboard/person_information')
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
            personFriends() {
                 axios
                    .get('/api/ekopatrol/person/friends/', {
                        params: {
                            id: this.$store.state.user.person[0].id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.friends = response.data
                        console.log(this.$store.state.user.friends)
                        // this.$router.push('/dashboard/person_information')
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
            personRelation() {
                axios
                    .get('/api/ekopatrol/person/relation/', {
                        params: {
                            id: this.$store.state.user.person[0].id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.relation = response.data
                        console.log(this.$store.state.user.relation)
                        // this.$router.push(/dashboard/person_information')
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
            workList() {
                axios
                    .get('/api/ekopatrol/person/work_list/', {
                        params: {
                            id: this.$store.state.user.person[0].id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.workList = response.data
                         this.$store.state.user.person = ""
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