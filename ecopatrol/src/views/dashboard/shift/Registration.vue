<template>
    <div class="container_employee">
        <div class="columns is-multiline">
            <div class="column is-12">
                <section class="section">
                    <div class="container_employee">
                        <div class="columns is-multiline">
                            <div class="column is-2">
                                <div class="box">
                                    <div class="has-text-centered">
                                        <h2 class="mt-4 mb-4">
                                            <span class="is-size-2">
                                                <strong>ԷՊԾ</strong>
                                            </span>
                                            <br/>
                                            <span class="is-size-4">
                                                <strong>էլեկտրոնային գրանցում</strong>
                                            </span>
                                             
                                        </h2>
                                    </div>
                                    <div class="has-text-centered">
                                        <Menu />                                     
                                    </div>
                                </div>
                            </div>
                            <div class="column is-10" v-if="$route.path != '/dashboard/precinct_shift/registration'">
                                <router-view />
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
    import Menu from '@/components/nav/Menu.vue'

    export default {
        name: 'Registration',
        components: { Menu }
    }
</script>