<template>
    <div class="box">
        <h3 class="title is-5 has-text-centered mb-4">
            Երթուղիների վերաբերյալ տեղեկատվություն
        </h3>

        <div class="columns">
            <div class="column">
                <div class="field">
                    <InvoiceTable 
                        :header="header"
                        :invoice="invoice"
                        routeName="route-detail"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import InvoiceTable from "../tables/InvoiceTable.vue";
export default {
    name: "RouteList",
    components: {
        InvoiceTable
    },
   computed: {
        header() {
            return [
                "#", 
                "Երթուղու համարը",
                "Երթուղու երկարություն",
                "Ստեղծման ամսաթիվ",
                "Քարտեզ"
            ]
        },
        invoice() {
            const routes = this.$store.state.user.route || []

            return routes.map((item, index) => ({
                id: item.id,
                name: item.route_number,
                route: item.route_length,
                create: item.registration_day,
                image: item.thumbnail,
                kmz: item.kmz_file
            }))
        }
    }
}
</script>
