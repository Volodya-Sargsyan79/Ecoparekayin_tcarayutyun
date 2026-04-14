<template>
    <div class="box">
        <h3 class="title is-5 has-text-centered mb-4">
           Հերթափոխերի վերաբերյալ տեղեկատվություն
        </h3>
                <!-- Date Filter -->
        <div class="columns is-vcentered mb-4">
            <div class="column is-narrow">
                <div class="field">
                    <label class="label is-small">Սկիզբ</label>
                    <div class="control">
                        <input class="input" type="date" v-model="dateFrom" />
                    </div>
                </div>
            </div>
            <div class="column is-narrow">
                <div class="field">
                    <label class="label is-small">Ավարտ</label>
                    <div class="control">
                        <input class="input" type="date" v-model="dateTo" />
                    </div>
                </div>
            </div>
            <div class="column is-narrow">
                <div class="flield">
                    <label class="label is-small">Տեղամաս</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                        <select v-model="precinct_id" @change="loadRoute">
                            <option value="">Ընտրել</option>
                            <option
                                v-for="precinct in $store.state.user.precincts"
                                :key="precinct.id"
                                :value="precinct.id"
                            >
                                {{ precinct.precinct }}
                            </option>
                        </select>
                    </div>
                    </div>
                </div>
            </div>
            <div class="column is-narrow">
                <div class="field">
                    <label class="label is-small">&nbsp;</label>
                    <div class="buttons">
                        <button class="button is-info" @click="search">Որոնել</button>
                        <button class="button is-light" @click="clear">Մաքրել</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="columns">
            <div class="column">
                <div class="field">
                    <InvoiceTable 
                        :header="header"
                        :invoice="invoice"
                        routeName="search-shift-detail"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import InvoiceTable from "../tables/InvoiceTable.vue";
    export default {
        name: "ShitListForm",
        data() {
            return {
                dateFrom: '',
                dateTo: '',
                precinct_id: '',
            }
        },
        components: {
            InvoiceTable
        },
        computed: {
            header() {
                return [
                    "#", 
                    "Սկիզբ",
                    "Ավարտ",
                    "Տեղամաս",
                    "Պետհամարանիշ",
                    "Կողային համար",
                    "Երթուղու համար",
                    "Երթուղու կմ",
                    "Քարտեզ"
                ]
            },
            invoice() {
                const routes = this.$store.state.user.stationshif || []

                return routes.map((item, index) => ({
                    id: item.id,
                    start_shift: item.start_shift,
                    end_shift: item.end_shift,
                    precinct: item.precinct,
                    car_number: item.car_number,
                    board_number: item.board_number,
                    route_number: item.route_number,
                    route_length: item.route_length,
                    image: item.thumbnail
                }))
            }
        },
        methods: {

            async search() {
                try {
                    const res = await axios.get('/api/ekopatrol/filterstationshift/', {
                        params: {
                            id: this.precinct_id || undefined,  // կամ քո param-ը
                            date_from: this.dateFrom || undefined,
                            date_to: this.dateTo || undefined,
                        }
                    })
                    this.$store.state.user.stationshif = res.data
                } catch (err) {
                    console.error(err)
                }
            },
            clear() {
                this.dateFrom = ''
                this.dateTo = ''
            }
        }
    };
</script>
