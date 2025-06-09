<template>
    <div class="container_employee">
        <div class="columns is-multiline">
            <div class="column is-12">
                <section class="section">
                    <div class="container_employee">
                        <div class="columns is-multiline">
                            <div class="column is-2">
                                <div class="box">
                                    <div v-if="typeof $store.state.user.person === 'object'">
                                        <Menu />
                                    </div>

                                    <div v-else class="has-text-centered">
                                        <p>Տվյալներ չեն գտնվել կամ բեռնվում են...</p>
                                    </div>
                                </div>
                            </div>

                            <div class="column is-10" v-if="$store.state.user.person.length > 1">
                                <div class="box" v-for="(item, index) in $store.state.user.person" :key="index">
                                    <div class="has-text-centered column is-12">                                                
                                        <div class="has-text-centered">
                                            <h2 class="is-size-4 mt-4 mb-4 name_title" @click="person(item.id)">
                                               {{ item.first_name }} {{ item.last_name }}ի անձնական տվյալները 
                                            </h2>
                                        </div>
                                        <TablePerson :item="item" />
                                    </div>
                                </div>
                            </div>
                            <div class="column is-10" v-else>
                                <div class="box">
                                    <div class="has-text-centered column is-12">                                                
                                        <div class="has-text-centered">
                                            <h2 class="is-size-4 mt-4 mb-4 name_title" >
                                               {{ $store.state.user.person.first_name }} {{ $store.state.user.person.last_name }}ի անձնական տվյալները 
                                            </h2>
                                        </div>
                                        <TablePerson :item="$store.state.user.person" />
                                        <TablePerson  
                                            v-for="(item, index) in this.$store.state.user.phone" 
                                            :key="index" 
                                            :item="{ mobile: item.phone }" 
                                        />
                                        <TablePerson  
                                            v-if="this.$store.state.user.address" v-for="(item, index) in filteredAddresses"  
                                            :key="index" 
                                            :item="item" 
                                        />
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
        computed: {
            filteredAddresses() {
                return this.$store.state.user.address.filter(item =>
                    item.registration === "Հաշվառման հասցե" || item.registration === "Բնակության հասցե"
                );
            }
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