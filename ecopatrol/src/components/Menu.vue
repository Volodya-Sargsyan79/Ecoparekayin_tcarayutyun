<template>
    <div class="menu">
        <div class="has-text-centered">
            <h2 class="is-size-4 mt-4 mb-4">
                Տեղեկատվություն<br/>{{ this.$store.state.user.employee[0].first_name }} {{ this.$store.state.user.employee[0].last_name }}ի<br/>վերաբերյալ
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
                                func: this.employeeRelatives,
                            },
                            {
                                label: 'Բարեկամներ',
                                func: this.employeePals,
                            },
                            {
                                label: 'Ընկերներ',
                                func: this.employeeFriends,
                            },
                            {
                                label: 'Կապեր',
                                func: this.employeeRelation,
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
                        label: 'Տուժեր և խրախուսանքներ',
                         children: [
                            {
                                label: 'Տուժեր',
                            },
                            {
                                label: 'Խրախուսանքներ',
                                func: this.employeePals,
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
                    }
                ]
            }
            
        },
        components: {
            MenuItem
        },
        methods: {
            employeeRelatives() {
                 axios
                    .get('/api/ekopatrol/employee/relatives/', {
                        params: {
                            id: this.$store.state.user.employee[0].id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.relatives = response.data
                        console.log(this.$store.state.user.relatives)
                        // this.$router.push('/dashboard/employee')
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
            employeePals() {
                 axios
                    .get('/api/ekopatrol/employee/pals/', {
                        params: {
                            id: this.$store.state.user.employee[0].id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.pals = response.data
                        console.log(this.$store.state.user.pals)
                        // this.$router.push('/dashboard/employee')
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
            employeeFriends() {
                 axios
                    .get('/api/ekopatrol/employee/friends/', {
                        params: {
                            id: this.$store.state.user.employee[0].id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.friends = response.data
                        console.log(this.$store.state.user.friends)
                        // this.$router.push('/dashboard/employee')
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
            employeeRelation() {
                 axios
                    .get('/api/ekopatrol/employee/relation/', {
                        params: {
                            id: this.$store.state.user.employee[0].id
                        }
                    })
                    .then(response => {
                        this.$store.state.user.relation = response.data
                        console.log(this.$store.state.user.relation)
                        // this.$router.push('/dashboard/employee')
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