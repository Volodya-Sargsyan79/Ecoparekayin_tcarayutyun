<template>
    <div class="box">
        <h3 class="title is-5 has-text-centered mb-4">
            Հերթապոխերի վերաբերյալ տեղեկատվություն
        </h3>

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
</template>

<script>
import InvoiceTable from "../tables/InvoiceTable.vue";
export default {
    name: "ShitListForm",
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
        }
};
</script>
