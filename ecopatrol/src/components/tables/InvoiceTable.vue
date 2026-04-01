<template>
    <table class="table is-fullwidth">
        <thead>
            <tr>
                <th v-for="(value, index) in header" :key="index">
                    {{ value }}
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(item, rowIndex) in invoice" :key="rowIndex" @click="handleClick(item)" style="cursor: pointer;">
                <td>{{ rowIndex + 1 }}</td>

                <template v-for="(value, key) in item" :key="key">
                    <td v-if="key !== 'id'">
                        <img 
                            v-if="key === 'image'" 
                            :src="`http://localhost:8000/media/${value}`" 
                            width="100"
                        />
                        <span v-else>
                            {{ value }}
                        </span>
                    </td>
                </template>
            </tr>
        </tbody>
    </table>
</template>

<script>

export default {
    name: "InvoiceTable",
    props: {
        header: {
            type: [String, Object, Array],
            required: true
        },
        invoice: {
            type: Array,
            required: true
        },
        routeName: {
            type: String,
            required: true
        }
    },
    methods: {
        handleClick(item) {
            this.$router.push({
            name: this.routeName,
            params: { id: item.id }
            })
        }
    }
};
</script>