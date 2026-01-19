<template>
    <div class="container_employee">
        <div class="columns is-multiline">
            <div class="column is-12">
                <section class="section">
                    <div class="container_employee">
                        <div class="columns is-multiline">
                            <div class="column is-2">
                                <div class="box">
                                    <div v-if="this.$store.state.user.persons" class="has-text-centered">
                                        <Menu />                                     
                                    </div>

                                    <div v-else >
                                        <p>Տվյալներ չեն գտնվել...</p>
                                    </div>
                                </div>
                            </div>

                            <div class="column is-10" v-if="this.$store.state.user.person.length > 0">
                                <div class="box" v-for="(item, index) in this.$store.state.user.person" :key="index">
                                    <div class="has-text-centered column is-12">                                                
                                        <div class="has-text-centered" v-if="item.first_name">
                                            <h2 class="is-size-4 mt-4 mb-4 name_title" @click="person(item.id)">
                                               {{ item.first_name }} {{ item.last_name }}ի անձնական տվյալները 
                                            </h2>
                                        </div>
                                        <div class="has-text-centered" v-else>
                                            <h2 class="is-size-4 mt-4 mb-4 name_title">
                                              {{ this.$store.state.user.persons.first_name }} {{ this.$store.state.user.persons.last_name }}ի անձնական տվյալները
                                            </h2>
                                        </div>
                                        <TablePerson :item="item" />
                                    </div>
                                </div>
                            </div>
                            <div 
                                class="column is-10"  
                                v-else-if="this.$store.state.user.person &&
                                Object.keys(this.$store.state.user.person).length !== 0 &&
                                this.$store.state.user.person.constructor === Object"
                            >
                                <div class="box">
                                    <div class="has-text-centered column is-12">                                                
                                        <div class="has-text-centered">
                                            <h2 class="is-size-4 mt-4 mb-4 name_title" >
                                               {{ this.$store.state.user.persons.first_name }} {{ this.$store.state.user.persons.last_name }}ի անձնական տվյալները 
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
                            <div class="column is-10" v-else>
                                <div class="box">
                                    <div class="has-text-centered column is-12">                                                
                                        <div class="has-text-centered">
                                            <h2 class="is-size-4 mt-4 mb-4 name_title" >
                                               Տվյալներ չեն գտնվել... 
                                            </h2>
                                        </div>
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
export default {
  name: 'FireAlarm'
}
</script>
