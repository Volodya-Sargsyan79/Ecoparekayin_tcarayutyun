<template>
    <div class="container_employee">
        <div class="columns is-multiline">
            <div class="column is-12">
                <section class="section">
                    <div class="container_employee">
                        <div class="columns is-multiline">
                            <div class="column is-2">
                                <div class="box">
                                    <div v-if="$store.state.user.employee.length > 0">
                                        <Menu />
                                    </div>

                                    <div v-else class="has-text-centered">
                                        <p>Տվյալներ չեն գտնվել կամ բեռնվում են...</p>
                                    </div>
                                </div>
                            </div>

                            <div class="column is-10">
                                <div class="box">
                                    <div class="has-text-centered column is-12">                                                
                                        <div class="has-text-centered">
                                            <h2 class="is-size-4 mt-4 mb-4">
                                                ՀՀ ՇՄՆ էկոպարեկային ծառայության աշխատակից
                                            </h2>
                                        </div>
                                        <TablePerson />
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
                first_name: "",
                last_name: "",
                passport: "",
                id_card: "",
                hvhh: "",
                errors: [],
                employee: []
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
</style>