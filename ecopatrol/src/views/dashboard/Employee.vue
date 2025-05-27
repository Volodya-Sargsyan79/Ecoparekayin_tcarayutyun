<template>
    <div class="container_employee">
        <div class="columns is-multiline">
            <div class="column is-12">
                <section class="section">
                    <div class="container_employee">
                        <div class="columns is-multiline">
                            <div class="column is-3">
                                <div class="box">
                                    <div class="has-text-centered">
                                         <h2 class="is-size-4 mt-4 mb-4">
                                            Տեղեկատվություն<br/>{{ this.$store.state.user.employee[0][1] }} {{ this.$store.state.user.employee[0][2] }}ի<br/>վերաբերյալ
                                        </h2>
                                    </div>
                                    <div>
                                        <Menu />
                                    </div>
                                </div>
                            </div>

                            <div class="column is-9">
                                <div class="box">
                                    <div class="has-text-centered column is-12">                                                
                                        <div class="has-text-centered">
                                            <h2 class="is-size-4 mt-4 mb-4">
                                                ՀՀ ՇՄՆ էկոպարեկային ծառայության աշխատակից
                                            </h2>
                                        </div>
                                        <section class="section">
                                            <div class="container_employee">                                                    

                                                 <div class="columns is-multiline">                                                        
                                                    <div class="column is-4">
                                                        <img class="employee_img"  :src="'http://localhost:8000/media/' + this.$store.state.user.employee[0][8]"/>
                                                    </div>
                                                    <div class="column is-8">

                                                        <table class="table">
                                                            <tbody>
                                                                <tr>
                                                                    <td>Անուն - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][1] }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Ազգանուն - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][2] }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Ծննդյան ամսաթիվ - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][3] }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Անձնագիր - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][4] }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Նույնականացման քարտ - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][5] }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Հվհհ - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][6] }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Email - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][2] }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Աշխատանք - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][10] }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Պաշտոն - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][11] }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Ընդունման ամսաթիվ - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][12] }}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td>Ազատման ամսաթիվ - </td>
                                                                    <td>{{ this.$store.state.user.employee[0][13] }}</td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                </div>
                                            </div>
                                        </section>
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
    export default {
        name: 'Employee',
        components: {
            Menu
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