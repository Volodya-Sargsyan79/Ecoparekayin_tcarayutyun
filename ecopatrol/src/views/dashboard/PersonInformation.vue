<template>
    <div class="container_employee">
        <div class="columns is-multiline">
            <div class="column is-12">
                <section class="section">
                    <div class="container_employee">
                        <div class="columns is-multiline">
                            <div class="column is-2">
                                <div class="box">
                                    <div v-if="$store.state.user.person.length > 0">
                                        <Menu />
                                    </div>

                                    <div v-else class="has-text-centered">
                                        <p>Տվյալներ չեն գտնվել կամ բեռնվում են...</p>
                                    </div>
                                </div>
                            </div>

                            <div class="column is-10" v-if="$store.state.user.person.length > 0">
                                <div class="box" v-for="(item, index) in this.$store.state.user.person" :key="index">
                                    <div class="has-text-centered column is-12">                                                
                                        <div class="has-text-centered">
                                            <h2 class="is-size-4 mt-4 mb-4 name_title" @click="person(item.id)">
                                               {{ item.first_name }} {{ item.last_name }}ի անձնական տվյալները 
                                            </h2>
                                        </div>
                                        <TablePerson :item="item"/>
                                    </div>
                                </div>
                            </div>
                            <div class="column is-10" v-else-if="$store.state.user.workList.length > 0">
                                <div class="box" v-for="(item, index) in this.$store.state.user.workList" :key="index">
                                    <div class="has-text-centered column is-12">                                                
                                        <div class="has-text-centered">
                                            <h2 class="is-size-4 mt-4 mb-4 name_title" @click="person(item.id)">
                                               {{ item.first_name }} {{ item.last_name }}ի անձնական տվյալները 
                                            </h2>
                                        </div>
                                        <TablePerson :item="item"/>
                                    </div>
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
    import Menu from '@/components/Menu.vue';
    import TablePerson from '@/components/TablePerson.vue';
    export default {
        name: 'Employee',
        components: {
            Menu,
            TablePerson
        },
        data() {
            return {
                errors: [],
            }
        },
        methods: {
            person(id) {
            
                this.errors = []

                this.$store.commit('setIsLoading', true)

                axios
                    .get('/api/ekopatrol/person/', {
                        params: {
                            id: id,
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

                this.$store.commit('setIsLoading', false)
            
            }
        }
    }
</script>

<style lang="scss">

    .container_employee {
        width: 100%;
    }
    .employee_img {
        width: 200px;
    }

    .name_title {
        cursor: pointer;
    }
</style>