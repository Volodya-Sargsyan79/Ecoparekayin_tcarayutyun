<template>
    <div class="box">
    <h2>Ունիվերսալ հերթափոխների գրաֆիկ (12/24 12/48)</h2>

    <div>
      <label>Աշխատողների թիվ:</label>
      <input v-model.number="numEmployees" type="number" min="2" />
    </div>

    <div>
      <label>Մեքենաների թիվ:</label>
      <input v-model.number="numVehicles" type="number" min="1" />
    </div>

    <div>
      <label>Սկիզբ ժամ:</label>
      <input v-model.number="startHour" type="number" min="0" max="23" />
    </div>

    <button type="button" @click="getSchedule">Ստանալ գրաֆիկը</button>

    <div v-if="error" style="color:red; margin-top:10px">{{ error }}</div>
    <ul v-if="schedule.length" style="margin-top:10px">
      <li v-for="(shift, index) in schedule" :key="index">{{ shift }}</li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";

export default {
    setup() {
        const numEmployees = ref(8); 
        const numVehicles = ref(1); 
        const startHour = ref(9);
        const schedule = ref([]);
        const error = ref("");

        const getSchedule = async () => {
        schedule.value = [];
        error.value = "";

        try {

            const employees = [];
            for (let i = 1; i <= numEmployees.value; i++) {
            employees.push(`Ա${i}`);
            }

            const vehicles = [];
            for (let i = 1; i <= numVehicles.value; i++) {
            vehicles.push(`${1000+i}`);
            }

            const params = new URLSearchParams();
            params.append("year", 2026);
            params.append("month", 3);
            params.append("start_hour", startHour.value);
            params.append("days", 31);
            employees.forEach(e => params.append("employees", e));
            vehicles.forEach(v => params.append("vehicles", v));

            const response = await axios.get(`/api/ekopatrol_duty/schedule/?${params.toString()}`);
            schedule.value = response.data;

        } catch (err) {
            console.error(err);
            error.value = "Անհաջող փորձ, ստուգեք API կամ ցանցը";
        }
        };

        return { numEmployees, numVehicles, startHour, schedule, error, getSchedule };
    }
}
</script>

<style scoped>
    h2 { margin-bottom: 10px; }
    input { margin: 4px 0 10px 0; padding: 4px; width: 80px; }
    button { padding: 6px 12px; cursor: pointer; margin-top: 10px; }
    ul { list-style-type: none; padding-left: 0; }
    li { margin-bottom: 4px; }
</style>