<template>
    <div class="menu">
        <MenuItem
            v-for="(item, index) in visibleMenuTree"
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
                        label: 'ԷՊԾ աշխատակցի գրանցում',
                        title: "Է",
                        func: () => this.registrationEmployee()
                    },
                    {
                        label: 'Հերթափոխի գրանցում',
                        title: "Հ",
                        func: () => this.registrationShift()
                    },
                    {
                        label: 'Երթուղու գրանցում',
                        title: "Ե",
                        func: () => this.registrationRoute()
                    },
                ]
            }
        },
        components: {
            MenuItem
        },
        computed: {
            userGroups() {
                return this.$store.state.user.groups || []
            },
            isAdmin() {
                return this.userGroups.includes('Ադմիններ')
            },
            visibleMenuTree() {
                if (this.isAdmin) {
                    return this.menuTree
                }
                return this.menuTree.filter(
                    item => item.label === 'Հերթափոխի գրանցում'
                )
            }
        },
        methods: {
            registrationEmployee() {
                axios
                    .get('/api/ecopatrol/regions/')
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
                    .get('/api/ecopatrol/position/')
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
                    this.$router.push('/dashboard/precinct_shift/registration/employee')
            },
            registrationShift() {
                axios
                    .get('/api/ecopatrol/regions/')
                    .then(response => {
                        const groups = this.$store.state.user.groups || []
                        const user = this.$store.state.user
                        if (
                            groups.includes('Ադմիններ') ||
                            groups.includes('Օպերատորներ')
                        ) {
                            this.$store.state.user.regions = response.data
                        }
                        else {
                            this.$store.state.user.regions = response.data.filter(
                                region => Number(region.id) === Number(user.region_id)
                            )
                        }
                        this.$router.push('/dashboard/precinct_shift/registration/shift')
                    })
            },
            registrationRoute() {
                axios
                    .get('/api/ecopatrol/regions/')
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
                this.$router.push('/dashboard/precinct_shift/registration/route')
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