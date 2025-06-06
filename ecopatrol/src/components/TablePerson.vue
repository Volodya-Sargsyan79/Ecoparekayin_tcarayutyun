<template>
    <section class="section">
        <div 
            class="container_employee" 
            v-if="$store.state.user.person.length > 0 
                || $store.state.user.workList.length > 0">                                                   
            <div class="columns is-multiline">                                                        
                <div class="column is-4" v-if="item.img">
                    <img class="employee_img"  :src="'http://localhost:8000/media/' + item.img"/>
                </div>
                <div class="column is-8">
                    <table class="table">
                        <tbody >
                            <tr v-if="item.pal_name">
                                <td colspan="3">{{ item.pal_name }}</td>
                            </tr>
                             <tr v-if="item.plase_name">
                                <td colspan="3">{{ item.plase_name }}</td>
                            </tr>
                            <tr v-if="item.position_start" class="has-text-left">
                                <td>Պաշտոն</td>
                                <td>-</td>
                                <td>{{ item.position_start }}</td>
                            </tr>
                             <tr v-if="item.data_of_start" class="has-text-left">
                                <td>Պաշտոնի սկիզբ</td>
                                 <td>-</td>
                                <td>{{ item.data_of_start }}</td>
                            </tr>
                            <tr v-if="item.end_of_start" class="has-text-left">
                                <td>Պաշտոնի ավարտ</td>
                                 <td>-</td>
                                <td>{{ item.end_of_start }}</td>
                            </tr>
                            <tr v-if="item.degree" class="has-text-left">
                                <td>Կոչում</td>
                                 <td>-</td>
                                <td>{{ item.degree }}</td>
                            </tr>
                            <tr v-if="item.birthday" class="has-text-left">
                                <td>Ծննդյան ամսաթիվ</td>
                                 <td>-</td>
                                <td>{{ item.birthday }}</td>
                            </tr>
                            <tr v-if="item.passport" class="has-text-left">
                                <td>Անձնագիր</td>
                                 <td>-</td>
                                <td>{{ item.passport }}</td>
                            </tr>
                            <tr v-if="item.id_card" class="has-text-left">
                                <td>Նույնականացման քարտ</td>
                                 <td>-</td>
                                <td>{{ item.id_card }}</td>
                            </tr>
                            <tr v-if="item.hvhh" class="has-text-left">
                                <td>Հվհհ</td>
                                 <td>-</td>
                                <td>{{ item.hvhh }}</td>
                            </tr>
                            <tr v-if="item.email" class="has-text-left">
                                <td>Email</td>
                                 <td>-</td>
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