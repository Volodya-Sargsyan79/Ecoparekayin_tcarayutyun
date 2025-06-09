<template>
    <section>
        <div class="container_employee" v-if="item"> 
            <div class="columns is-multiline">                                                        
                <div class="column is-4">
                    <img v-if="item.img" class="employee_img"  :src="'http://localhost:8000/media/' + item.img"/>
                </div>
                <div class="column is-8">
                    <table class="table">
                        <thead>
                            <tr v-if="item.pal_name">
                                <th colspan="3" class="has-text-centered">{{ item.pal_name }}</th>
                            </tr>
                        </thead>
                        <tbody>                           
                            <template v-for="(value, key) in item">
                                <tr
                                    v-if="key !== 'id' && key !== 'img' && value !== '' && value !== null && value !== undefined"
                                    :key="key"
                                    class="has-text-left"
                                >
                                    <td>{{ formatKey(key) }}</td>
                                    <td>-</td>
                                    <td >{{ value }}</td>
                                </tr>
                            </template>
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
        },
        methods: {
            formatKey(key) {
                return key
                .replace(/_/g, ' ')          // Replace underscores with spaces
                .replace(/\b\w/g, l => l.toUpperCase()); // Capitalize first letter of each word
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