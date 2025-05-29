<template>
    <section class="section">
        <div class="container_employee" v-if="$store.state.user.employee.length > 0 ">                                                    
            <div class="columns is-multiline">                                                        
                <div class="column is-4">
                    <img class="employee_img"  :src="'http://localhost:8000/media/' + this.$store.state.user.employee[0].img"/>
                </div>
                <div class="column is-8">
                    <table class="table">
                        <tbody>
                            <tr>
                                <td>Անուն - </td>
                                <td>{{ this.$store.state.user.employee[0].first_name }}</td>
                            </tr>
                            <tr>
                                <td>Ազգանուն - </td>
                                <td>{{ this.$store.state.user.employee[0].last_name }}</td>
                            </tr>
                            <tr>
                                <td>Ծննդյան ամսաթիվ - </td>
                                <td>{{ this.$store.state.user.employee[0].birthday }}</td>
                            </tr>
                            <tr>
                                <td>Անձնագիր - </td>
                                <td>{{ this.$store.state.user.employee[0].passport }}</td>
                            </tr>
                            <tr>
                                <td>Նույնականացման քարտ - </td>
                                <td>{{ this.$store.state.user.employee[0].id_card }}</td>
                            </tr>
                            <tr>
                                <td>Հվհհ - </td>
                                <td>{{ this.$store.state.user.employee[0].hvhh }}</td>
                            </tr>
                            <tr>
                                <td>Email - </td>
                                <td>{{ this.$store.state.user.employee[0].email }}</td>
                            </tr>
                            <tr>
                                <td>Աշխատանք - </td>
                                <td>{{ this.$store.state.user.employee[0].name }}</td>
                            </tr>
                            <tr>
                                <td>Պաշտոն - </td>
                                <td>{{ this.$store.state.user.employee[0].position_start }}</td>
                            </tr>
                            <tr>
                                <td>Ընդունման ամսաթիվ - </td>
                                <td>{{ this.$store.state.user.employee[0].data_of_start }}</td>
                            </tr>
                            <tr>
                                <td>Ազատման ամսաթիվ - </td>
                                <td>{{ this.$store.state.user.employee[0].end_of_start }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div v-else class="has-text-centered">
            <p>Տվյալներ չեն գտնվել կամ բեռնվում են...</p>
        </div>
    </section>                         
</template>

<script>
    import axios from 'axios';
    export default {
        name: 'TablePerson',
        components: {
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