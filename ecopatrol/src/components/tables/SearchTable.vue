<template>
    <table class="table is-fullwidth">
        <thead>
            <tr>
                <th v-for="(value, index) in header" :key="index" style="text-align: center; vertical-align: middle; ">
                    <span v-html="value"></span>
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(row, rowIndex) in invoice" :key="rowIndex">
                <td v-if="invoice.length > 1" style="text-align: center;">{{ rowIndex + 1 }}</td>

                <td v-for="(cell, cellIndex) in row" :key="cellIndex" style="text-align: center; vertical-align: middle; ">
                    <template v-if="isPerson && cellIndex === 3 && cell">
                        {{ cell }}
                        <button @click="callNumber(cell)">📞</button>
                    </template>

                    <template v-else>
                        {{ cell }}
                    </template>
                </td>
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
        isPerson: {   // 👈 ավելացրու սա
            type: Boolean,
            default: false
        }
    },
    methods: {
        callNumber(number) {
           if (!number) return
  window.location.href = `sip:${number}`
        }
    }
};
</script>