<template>
    <div class="menu">
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
                        label: 'Ահազանգող',
                        children: [
                            {
                                label: 'ԷՊԾ աշխատակից',
                                title: "Է",
                                func: () => this.personEmployee()
                            },
                            {
                                label: 'Քաղաքացի',
                                title: "Ք",
                                func: () => this.personRelatives()
                            }
                        ]
                    },
                    {
                        label: 'Հրդեհ',
                        func: () => this.fireCall(),
                    },
                    {
                        label: 'ՕԿԿ ծառայող',
                        func: this.personSoldier,
                    }
                ]
            }
            
        },
        components: {
            MenuItem
        },
        methods: {
            personEmployee() {
                this.$router.push('/dashboard/firealarm/epsemployee')
                axios
                    .get('/api/ekopatrol/regions/')
                    .then(response => {
                        this.$store.state.user.regions = response.data
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
                axios
                    .get('/api/ekopatrol/position/')
                    .then(response => {
                        this.$store.state.user.position = response.data
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
            personRelatives() {
                this.$router.push('/dashboard/firealarm/citizen')
                axios
                    .get('/api/ekopatrol/regionArmenia/')
                    .then(response => {
                        this.$store.state.user.regionArmenia = response.data
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
            fireCall() {
                this.$router.push('/dashboard/firealarm/firecaller')
                // axios
                //     .get('/api/ekopatrol/getLastCaller/', {
                //         params: {
                //             name: this.$store.state.user.caller
                //         }
                //     })
                //     .then(response => {
                //         this.$store.state.user.person = response.data
                //     })
                //     .catch(error => {
                //         if (error.response) {
                //             for (const property in error.response.data) {
                //                 this.errors.push(`${property}: ${error.response.data[property]}`)
                //             }
                //             console.log(JSON.stringify(error.response.data))
                //         } else if (error.message) {
                //             this.errors.push('Something went wrong. Please try again')
                //             console.log(JSON.stringify(error))
                //         }
                //     }) 
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