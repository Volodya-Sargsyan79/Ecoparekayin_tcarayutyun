<template>
    <div class="box">
        <h3 class="title is-5 has-text-centered mb-4">Հերթապոխերի վերաբերյալ տեղեկատվություն</h3>
        <div class="columns">
            <div class="column">
                <div class="field">
                    <InvoiceTable 
                        :header="header"
                        :invoice="invoice"
                        routeName="shift-detail"
                    />
                </div>
            </div>
        </div>
    </div>
    <div class="box" v-if="this.$store.state.user.stationshif && this.$store.state.user.stationshif.length > 0">
        <h3 class="title is-5 has-text-centered mb-4">{{this.$store.state.user.stationshif[0].precinct}}ի Հերթապոխերի վերաբերյալ զեկուցագիր</h3>
        <div class="columns" >
            <div class="column">
                <div class="box mb-3" v-for="(value, index) in this.$store.state.user.filelist" :key="index">
                    <a v-if="value.pdf_file" :href="`http://192.168.88.111:8000/media/${value.pdf_file}`"  target="_blank" class="button is-link is-small">📄 Բացել PDF</a>
                </div>
            </div>
        </div>
        <div class="columns" v-if="Array.isArray(this.$store.state.user.filelist) && this.$store.state.user.filelist.length === 0">
            <div class="field">
                <label class="label">PDF ֆայլ</label>
                <div class="control">
                    <input type="file" accept=".pdf" @change="form.PDF = $event.target.files[0]"/>
                </div>
            </div>
            <button v-if="form.PDF" type="submit" class="button is-primary is-medium" @click.prevent="saveCall">Պահպանել</button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import InvoiceTable from "../tables/InvoiceTable.vue";
    import { formatDate } from "@/utils/dateFormatter";

    export default {
        name: "ShitListForm",
        data() {
            return {
                shift_pdf: null,
                form: {
                    PDF: null
                }
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
                    start_shift: formatDate(item.start_shift),
                    end_shift: formatDate(item.end_shift),
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
            getShiftDayInfo() {
                const stationshift = this.$store.state.user.stationshif
                if (!stationshift || stationshift.length === 0) {
                    this.shift_pdf = []
                    return
                }
                const precinctId = stationshift[0].precinct_id
                axios
                    .get('/api/ecopatrol/getshiftdayinfo/', {
                        params: {
                            id: precinctId
                        }
                    })
                    .then((res) => {
                        this.$store.state.user.filelist = res.data
                    })
                    .catch((err) => {
                        console.error('PDF-ների ստացման սխալ՝', err)
                        this.shift_pdf = []
                    })
            },
            saveCall() {
                if (!this.form.PDF) {
                    alert('Խնդրում ենք ընտրել PDF ֆայլ։')
                    return
                }
                const stationshift = this.$store.state.user.stationshif
                if (!stationshift || stationshift.length === 0) {
                    alert('Հերթափոխի տվյալները բացակայում են։')
                    return
                }
                const formData = new FormData()
                formData.append(
                    'precinct',
                    stationshift[0].precinct_id
                )
                formData.append('PDF', this.form.PDF)
                axios
                    .post('/api/ecopatrol/addshiftdayinfo/', formData)
                    .then(() => {
                        // Նորից բեռնում ենք PDF-ների ցանկը
                        return this.getShiftDayInfo()
                    })
                    .then(() => {
                        alert('Ֆայլը հաջողությամբ ներբեռնվել է։')

                        // Մաքրում ենք ընտրված ֆայլը
                        this.form.PDF = null

                        if (this.$refs.pdfInput) {
                            this.$refs.pdfInput.value = ''
                        }
                    })
                    .catch((err) => {
                        alert(
                            err.response?.data?.error ||
                            'Տեղի է ունեցել սխալ։'
                        )
                        console.error(err)
                    })
            }
        }
    };
</script>
