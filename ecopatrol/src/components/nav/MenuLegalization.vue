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
                        label: 'Ապօրինի ծառահատում',
                        title: "Ծ",
                        func: () => this.illegalԼogging()
                    },
                    {
                        label: 'Ապօրինի որս',
                        title: "Ո",
                        func: () => this.poaching()
                    },
                    {
                        label: 'Ապօրինի ձկնորսություն',
                        title: "Ե",
                        func: () => this.illegalFishing()
                    },
                ]
            }
        },
        components: {
            MenuItem
        },
        methods: {
            illegalԼogging() {
                axios
                    .get('/api/legalization/regions/')
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
                this.$router.push('/dashboard/legalization/registration_legalization/illegal_logging')
            },
            poaching() {
                axios
                    .get('/api/legalization/regions/')
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
                this.$router.push('/dashboard/legalization/registration_legalization/poaching')
            },
            illegalFishing() {
                axios
                    .get('/api/legalization/regions/')
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
                this.$router.push('/dashboard/legalization/registration_legalization/illegal_fishing')
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