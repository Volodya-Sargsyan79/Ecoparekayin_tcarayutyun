<template>
    <div class="menu">
        <div class="has-text-centered">
            <h2 class="is-size-4 mt-4 mb-4">
                <br/>{{ $store.state.user.person.first_name }} {{ $store.state.user.person.last_name }}<br/>
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
                        label: 'Անշարժ գույք',
                        children: [
                            {
                                label: 'Հաշվառման հասցե',
                                func: this.registrationAddress,
                            },
                            {
                                label: 'Բնակության հասցե',
                                func: this.residentialAddress,
                            },
                            {
                                label: 'property',
                            }
                        ]
                    },
                    {
                        label: 'Մեքենա',
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
            personRelatives(title) {
                 axios
                    .get('/api/ekopatrol/person/relatives/', {
                        params: {
                            id: this.$store.state.user.person.id,
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