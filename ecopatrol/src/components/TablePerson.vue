<template>
    <section class="section">
        <div 
            class="container_employee" 
            v-if="$store.state.user.person.length > 0 
                || $store.state.user.workList.length > 0">
                {{ console.log($store.state.user.workList, 111111111) }}                                                    
            <div class="columns is-multiline">                                                        
                <div class="column is-4" v-if="item.img">
                    <img class="employee_img"  :src="'http://localhost:8000/media/' + item.img"/>
                </div>
                <div class="column is-8">
                    <table class="table">
                        <tbody >
                            <tr v-if="item.name">
                                <td colspan="2">{{ item.name }}</td>
                            </tr>
                            <tr v-if="item.name">
                                <td>Պաշտոն - </td>
                                <td>{{ item.position_start }}</td>
                            </tr>
                            <tr v-if="item.first_name">
                                <td>Անուն - </td>
                                <td>{{ item.first_name }}</td>
                            </tr>
                            <tr v-if="item.last_name">
                                <td>Ազգանուն - </td>
                                <td>{{ item.last_name }}</td>
                            </tr>
                            <tr v-if="item.birthday">
                                <td>Ծննդյան ամսաթիվ - </td>
                                <td>{{ item.birthday }}</td>
                            </tr>
                            <tr v-if="item.passport">
                                <td>Անձնագիր - </td>
                                <td>{{ item.passport }}</td>
                            </tr>
                            <tr v-if="item.id_card">
                                <td>Նույնականացման քարտ - </td>
                                <td>{{ item.id_card }}</td>
                            </tr>
                            <tr v-if="item.hvhh">
                                <td>Հվհհ - </td>
                                <td>{{ item.hvhh }}</td>
                            </tr>
                            <tr v-if="item.email">
                                <td>Email - </td>
                                <td>{{ item.email }}</td>
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
        },
        props: {
            item: {
                type: Object
            },
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