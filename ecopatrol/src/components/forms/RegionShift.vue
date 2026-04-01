<template>
    <form class="box">
        <h3 class="title is-5 has-text-centered mb-4">
            Հերթափոխի գրանցում
        </h3>

        <!-- Name & Surname $ Phone-->
        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="label">Հերտափոխի սկիզբ</label>
                    <div class="control">
                        <input class="input" type="datetime-local" v-model="form.start_shift">
                    </div>
                </div>
                <p v-if="!form.start_shift" class="help is-danger">
                    Պարտադիր է ընտրել տեղամասը
                </p>
            </div>

            <div class="column">
                <div class="field">
                    <label class="label">Հերտափոխի ավարտ</label>
                    <div class="control">
                        <input class="input" type="datetime-local" v-model="form.end_shift">
                    </div>
                </div>
                <p v-if="!form.end_shift" class="help is-danger">
                    Պարտադիր է ընտրել տեղամասը
                </p>
            </div>

            <div class="column">
                <div class="field">
                    <label class="label">Մարզային վարչություն</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.region_id" @change="loadRegion">
                                <option value="">Ընտրել</option>
                                <option
                                    v-for="region in $store.state.user.regions"
                                    :key="region.id"
                                    :value="region.id"
                                >
                                    {{ region.region }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <p v-if="!form.region_id" class="help is-danger">
                        Պարտադիր է ընտրել Մարզային վարչություն
                    </p>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Տեղամաս</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.precinct_id" @change="loadRoute">
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
                    <p v-if="!form.precinct_id" class="help is-danger">
                        Պարտադիր է ընտրել տեղամասը
                    </p>
                </div>
            </div>
            <!-- Position -->
        </div>
        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="label">ԷՊ ծառայող 1</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.employee_01_id">
                                <option value="">Ընտրել</option>
                                <option
                                    v-for="employee in $store.state.user.employee"
                                    :key="employee.id"
                                    :value="employee.id"
                                >
                                    {{ employee.camera }} {{ employee.name }} {{ employee.surname }} 
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                <p v-if="!form.employee_01_id" class="help is-danger">
                    Պարտադիր է ընտրել տեղամասը
                </p>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">ԷՊ ծառայող 2</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.employee_02_id">
                                <option value="">Ընտրել</option>
                                <option
                                    v-for="employee in $store.state.user.employee"
                                    :key="employee.id"
                                    :value="employee.id"
                                >
                                    {{ employee.camera }} {{ employee.name }} {{ employee.surname }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                <p v-if="!form.employee_02_id" class="help is-danger">
                    Պարտադիր է ընտրել տեղամասը
                </p>
            </div>
             <div class="column">
                <div class="field">
                    <label class="label">ԷՊ ծառայող 3</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.employee_03_id">
                                <option value="">Ընտրել</option>
                                <option
                                    v-for="employee in $store.state.user.employee"
                                    :key="employee.id"
                                    :value="employee.id"
                                >
                                    {{ employee.camera }} {{ employee.name }} {{ employee.surname }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">ԷՊ ծառայող 4</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                           <select v-model="form.employee_04_id">
                                <option value="">Ընտրել</option>
                                <option
                                    v-for="employee in $store.state.user.employee"
                                    :key="employee.id"
                                    :value="employee.id"
                                >
                                    {{ employee.camera }} {{ employee.name }} {{ employee.surname }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        </div>        
        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="label">Մեքենա</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                           <select v-model="form.car_id">
                                <option value="">Ընտրել</option>
                                <option
                                    v-for="car in $store.state.user.car"
                                    :key="car.id"
                                    :value="car.id"
                                >
                                    {{ car.car_number }} {{ car.board_number }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                <p v-if="!form.car_id" class="help is-danger">
                    Պարտադիր է ընտրել տեղամասը
                </p>
            </div>

            <div class="column">
                <div class="field">
                    <label class="label">Երթուղի</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                           <select v-model="form.route_id">
                                <option value="">Ընտրել</option>
                                <option
                                    v-for="route in $store.state.user.route"
                                    :key="route.id"
                                    :value="route.id"
                                >
                                    {{ route.route_number }} երթուղի {{ route.route_length }}կմ
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                <p v-if="!form.route_id" class="help is-danger">
                    Պարտադիր է ընտրել տեղամասը
                </p>
            </div>
        </div>
        <!-- Submit -->
        <div class="field mt-5 has-text-centered">
            <button
                type="submit"
                class="button is-primary is-medium"
                @click.prevent="saveCall"
            >
            Պահպանել
            </button>
        </div>
    </form>                     
</template>

<script>
import axios from 'axios'

export default {
    name: 'RegionShift',

    data() {
        return {
            form: {
                start_shift: null,
                end_shift: null,
                region_id: null,
                precinct_id: null,
                employee_01_id: null,
                employee_02_id: null,
                employee_03_id: null,
                employee_04_id: null,
                car_id: null,
                route_id: null
            }
        }
    },

    methods: {
         loadRegion() {
            if (!this.form.region_id) return;

            axios
                .get("/api/ekopatrol/precinct/", {
                    params: { id: this.form.region_id },
                })
                .then((res) => {
                    // Store the response in precincts
                    this.$store.state.user.precincts = res.data;
                })
                .catch((err) => {
                    console.error(err);
                });
             axios
                .get("/api/ekopatrol/getlastcar/", {
                    params: { id: this.form.region_id },
                })
                .then((res) => {
                    // Store the response in precincts
                    this.$store.state.user.car = res.data;
                })
                .catch((err) => {
                    console.error(err);
                });
        },
        loadRoute() {
            if (!this.form.precinct_id) return;

            axios
                .get("/api/ekopatrol/getlastroute/", {
                    params: { id: this.form.precinct_id },
                })
                .then((res) => {
                    // Store the response in precincts
                    this.$store.state.user.route = res.data;
                })
                .catch((err) => {
                    console.error(err);
                });
            axios
                .get("/api/ekopatrol/getlastemployee/",{
                    params: { id: this.form.precinct_id },
                })
                .then(res => {
                    this.$store.state.user.employee = res.data
                })
                .catch(err => { console.error(err) })
        },
        saveCall() {
            axios.post("/api/ekopatrol/addstationshift/", this.form)
                .then(() => 
                     axios
                        .get('/api/ekopatrol/getstationshiftlist/', {
                            params: { id: this.form.precinct_id }
                        }) 
                        .then((res) => {
                            // Store the response in precincts
                            this.$store.state.user.stationshif = res.data;
                            this.$router.push('/dashboard/register/shitlist')
                        })
                        .catch(err => { console.error(err) }) 
                    
                   
                )
                .catch(err => console.error(err))
        }
    }
}
</script>