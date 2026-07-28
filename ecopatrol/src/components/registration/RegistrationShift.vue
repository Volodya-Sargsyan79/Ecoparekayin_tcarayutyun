<template>
    <form class="box">
        <h3 class="title is-5 has-text-centered mb-4">Հերթափոխի գրանցում
        </h3>
        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="label">Հերթափոխի սկիզբ</label>
                    <div class="field is-grouped is-align-items-center">
                        <div class="control is-expanded">
                            <input class="input" type="date" v-model="form.start_shift_date">
                        </div>
                        <div class="control" style="max-width: 110px;">
                            <input
                                class="input"
                                type="number"
                                min="0"
                                max="23"
                                step="1"
                                inputmode="numeric"
                                v-model="form.start_shift_hour"
                                placeholder="Ժամ"
                                @blur="normalizeTimeField('start')"
                            >
                        </div>
                        <div class="control" style="max-width: 110px;">
                            <input
                                class="input"
                                type="number"
                                min="0"
                                max="59"
                                step="1"
                                inputmode="numeric"
                                v-model="form.start_shift_minute"
                                placeholder="րոպ"
                                @blur="normalizeTimeField('start')"
                            >
                        </div>
                    </div>
                </div>
                <p v-if="!form.start_shift_date || !form.start_shift_hour || !form.start_shift_minute" class="help is-danger">Պարտադիր է ընտրել սկիզբի ամսաթիվը և ժամանակը</p>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Հերթափոխի ավարտ</label>
                    <div class="field is-grouped is-align-items-center">
                        <div class="control is-expanded">
                            <input class="input" type="date" v-model="form.end_shift_date">
                        </div>
                        <div class="control" style="max-width: 110px;">
                            <input
                                class="input"
                                type="number"
                                min="0"
                                max="23"
                                step="1"
                                inputmode="numeric"
                                v-model="form.end_shift_hour"
                                placeholder="Ժամ"
                                @blur="normalizeTimeField('end')"
                            >
                        </div>
                        <div class="control" style="max-width: 110px;">
                            <input
                                class="input"
                                type="number"
                                min="0"
                                max="59"
                                step="1"
                                inputmode="numeric"
                                v-model="form.end_shift_minute"
                                placeholder="րոպ"
                                @blur="normalizeTimeField('end')"
                            >
                        </div>
                    </div>
                </div>
                <p v-if="!form.end_shift_date || !form.end_shift_hour || !form.end_shift_minute" class="help is-danger">Պարտադիր է ընտրել ավարտի ամսաթիվը և ժամանակը</p>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Մարզային վարչություն</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.region_id" @change="loadRegion">
                                <option value="">Ընտրել</option>
                                <option v-for="region in $store.state.user.regions" :key="region.id" :value="region.id">{{ region.region }}</option>
                            </select>
                        </div>
                    </div>
                    <p v-if="!form.region_id" class="help is-danger">Պարտադիր է ընտրել Մարզային վարչություն</p>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Տեղամաս</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.precinct_id" @change="loadRoute">
                                <option value="">Ընտրել</option>
                                <option v-for="precinct in $store.state.user.precincts" :key="precinct.id" :value="precinct.id">{{ precinct.precinct }}</option>
                            </select>
                        </div>
                    </div>
                    <p v-if="!form.precinct_id" class="help is-danger">Պարտադիր է ընտրել տեղամասը</p>
                </div>
            </div>
        </div>
        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="label">ԷՊ ծառայող 1</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.employee_01_id">
                                <option value="">Ընտրել</option>
                                <option v-for="employee in $store.state.user.employee" :key="employee.id" :value="employee.id">
                                    {{ employee.number }} {{ employee.name }} {{ employee.surname }} 
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                <p v-if="!form.employee_01_id" class="help is-danger">Պարտադիր է ընտրել տեղամասը</p>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">ԷՊ ծառայող 2</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.employee_02_id">
                                <option value="">Ընտրել</option>
                                <option v-for="employee in $store.state.user.employee" :key="employee.id" :value="employee.id">
                                    {{ employee.number }} {{ employee.name }} {{ employee.surname }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                <p v-if="!form.employee_02_id" class="help is-danger">Պարտադիր է ընտրել տեղամասը</p>
            </div>
             <div class="column">
                <div class="field">
                    <label class="label">ԷՊ ծառայող 3</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.employee_03_id">
                                <option value="">Ընտրել</option>
                                <option v-for="employee in $store.state.user.employee" :key="employee.id" :value="employee.id">
                                    {{ employee.number }} {{ employee.name }} {{ employee.surname }}
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
                                <option v-for="employee in $store.state.user.employee" :key="employee.id" :value="employee.id">
                                    {{ employee.number }} {{ employee.name }} {{ employee.surname }}
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
                                <option v-for="car in $store.state.user.car" :key="car.id" :value="car.id">
                                    {{ car.board_number }} {{ car.car_number }} 
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                <p v-if="!form.car_id" class="help is-danger">Պարտադիր է ընտրել տեղամասը</p>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Երթուղի</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                           <select v-model="form.route_id">
                                <option value="">Ընտրել</option>
                                <option v-for="route in $store.state.user.route" :key="route.id" :value="route.id">
                                    {{ route.route_number }} երթուղի {{ route.route_length }}կմ {{ route.registration_day }} ստեղծման ամսաթիվ
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                <p v-if="!form.route_id" class="help is-danger">Պարտադիր է ընտրել տեղամասը</p>
            </div>
        </div>
        <div class="field mt-5 has-text-centered">
            <button type="submit" class="button is-primary is-medium" @click.prevent="saveCall">Պահպանել</button>
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
                    start_shift_date: null,
                    start_shift_hour: null,
                    start_shift_minute: null,
                    end_shift_date: null,
                    end_shift_hour: null,
                    end_shift_minute: null,
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
                    .get("/api/ecopatrol/precinct/", {
                        params: { id: this.form.region_id },
                    })
                    .then(response => {
                        const groups = this.$store.state.user.groups || []
                        const user = this.$store.state.user
                        if (
                            groups.includes('Ադմիններ') ||
                            groups.includes('Օպերատորներ')
                        ) {
                            this.$store.state.user.precincts = response.data
                        } else {
                            // Հերթապահ և տեղամասի պետ՝ միայն իրենց տեղամասը
                            this.$store.state.user.precincts = response.data.filter(
                                precinct =>
                                    Number(precinct.id) === Number(user.precinct_id)
                            )
                        }
                    })
                axios
                    .get("/api/ecopatrol/getlastcar/", {
                        params: { id: this.form.region_id },
                    })
                    .then((res) => {
                        this.$store.state.user.car = res.data;
                    })
                    .catch((err) => {
                        console.error(err);
                    });
            },
            loadRoute() {
                if (!this.form.precinct_id) return;
                axios
                    .get("/api/ecopatrol/getlastroute/", {
                        params: { id: this.form.precinct_id },
                    })
                    .then((res) => {
                        this.$store.state.user.route = res.data;
                    })
                    .catch((err) => {
                        console.error(err);
                    });
                axios
                    .get("/api/ecopatrol/getlastemployee/",{
                        params: { id: this.form.precinct_id },
                    })
                    .then(res => {
                        this.$store.state.user.employee = res.data
                    })
                    .catch(err => { console.error(err) })
            },
            normalizeTimeField(part) {
                const hourKey = `${part}_shift_hour`
                const minuteKey = `${part}_shift_minute`

                const normalize = (value, max) => {
                    if (value === null || value === undefined || value === '') return null
                    const digits = String(value).replace(/\D/g, '')
                    if (!digits) return null
                    const num = Number(digits)
                    const clamped = Math.min(Math.max(num, 0), max)
                    return String(clamped).padStart(2, '0')
                }

                this.form[hourKey] = normalize(this.form[hourKey], 23)
                this.form[minuteKey] = normalize(this.form[minuteKey], 59)
            },
            saveCall() {
                const payload = { ...this.form }
                payload.start_shift = `${this.form.start_shift_date}T${String(this.form.start_shift_hour).padStart(2, '0')}:${String(this.form.start_shift_minute).padStart(2, '0')}`
                payload.end_shift = `${this.form.end_shift_date}T${String(this.form.end_shift_hour).padStart(2, '0')}:${String(this.form.end_shift_minute).padStart(2, '0')}`
                delete payload.start_shift_date
                delete payload.start_shift_hour
                delete payload.start_shift_minute
                delete payload.end_shift_date
                delete payload.end_shift_hour
                delete payload.end_shift_minute

                axios.post("/api/ecopatrol/addstationshift/", payload)
                    .then(() => 
                        axios
                            .get('/api/ecopatrol/getstationshiftlist/', {
                                params: { id: this.form.precinct_id }
                            }) 
                            .then((res) => {
                                this.$store.state.user.stationshif = res.data
                                alert("Գրանցումը հաջողությամբ կատարվել է:")
                                this.$router.push('/dashboard/precinct_shift/registration')
                            })
                            .catch(err => {
                                alert("Անհրաժեշտ է լրացնել բոլոր դաշտերը:")
                                console.error(err) 
                            }) 
                    )
                    .catch(err => {
                        alert("Հերթափոխն արդեն գրանցված է:")
                        console.error(err)
                    })
            }
        }
    }
</script>