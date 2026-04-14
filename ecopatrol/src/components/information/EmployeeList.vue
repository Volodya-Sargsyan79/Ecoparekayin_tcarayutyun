<template>
    <div class="box">
        <h3 class="title is-5 has-text-centered mb-4">
            Անձնակազմի վերաբերյալ տեղեկատվություն
        </h3>

        <div class="columns">
            <div class="column">
                <div class="field">
                    <InvoiceTable 
                        :header="header"
                        :invoice="invoice"
                        routeName="person-detail"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import InvoiceTable from "../tables/InvoiceTable.vue";
export default {
    name: "EmployeeList",
    components: {
        InvoiceTable
    },
     computed: {
        header() {
            return [
                "#",
                "Տեսախցիկ",
                "Անուն",
                "Ազգանուն", 
                "Հեռախոս"
            ]
        },
        invoice() {
            const routes = this.$store.state.user.employee || []

            return routes.map((item, index) => ({
                id: item.id,
                camera: item.camera,
                name: item.name,
                surname: item.surname,
                phone: item.phone,
            }))
        }
    }
};
</script>
