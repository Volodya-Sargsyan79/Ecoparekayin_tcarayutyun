<template>
    <form class="box">
        <h3 class="title is-5 has-text-centered mb-4">
            {{ this.$store.state.user.caller }}
        </h3>

        <!-- Name & Surname $ Phone-->
        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="label">Անուն</label>
                    <div class="control">
                        <input class="input" v-model="form.name" placeholder="Անուն">
                    </div>
                </div>
            </div>

            <div class="column">
                <div class="field">
                    <label class="label">Ազգանուն</label>
                    <div class="control">
                        <input class="input" v-model="form.surname" placeholder="Ազգանուն">
                    </div>
                </div>
            </div>

            <div class="column">
                <div class="field">
                    <label class="label">Հեռախոս</label>
                    <div class="control">
                        <input class="input" v-model="form.phone" placeholder="(+374)">
                    </div>
                </div>
            </div>
        </div>

        <!-- Region -->
        <div class="field">
            <label class="label">{{ $store.state.user.caller === "ԷՊԾ աշղատակից" ? "Մարզային վարչություն" : "Մարզ" }}</label>
            <div class="control">
                <div class="select is-fullwidth">
                    <select v-model="form.region_id" @change="loadPrecincts">
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
        </div>

        <!-- Precinct -->
        <div class="field">
            <label class="label">{{ $store.state.user.caller === "ԷՊԾ աշղատակից" ? "Տեղամաս" : "Քաղաք" }}</label>
            <div class="control">
                <div class="select is-fullwidth">
                    <select v-model="form.precinct_id" @change="loadVillage">
                        <option value="">Ընտրել</option>
                        <option
                            v-for="precinct in $store.state.user.precincts"
                            :key="precinct.id"
                            :value="precinct.id"
                        >
                            {{ $store.state.user.caller === "ԷՊԾ աշղատակից" ? precinct.section : precinct.city }}
                        </option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Position -->
        <div class="field">
            <label class="label">{{ $store.state.user.caller === "ԷՊԾ աշղատակից" ? "Պաշտոն" : "Գյուղ" }}</label>
            <div class="control">
            <div class="select is-fullwidth">
                <select v-model="form.position_id">
                    <option value="">Ընտրել</option>
                    <option
                        v-for="position in $store.state.user.position"
                        :key="position.id"
                        :value="position.id"
                    >
                        {{ $store.state.user.caller === "ԷՊԾ աշղատակից" ?  position.position_held : position.village }}
                    </option>
                </select>
            </div>
            </div>
        </div>

        <!-- Street, House, Apartment -->
        <div v-if="$store.state.user.caller !== 'ԷՊԾ աշղատակից'">
            <div class="columns">
                <div class="column">
                    <div class="field">
                        <label class="label">Փողոց</label>
                        <div class="control">
                            <input class="input" v-model="form.street" placeholder="Փողոց">
                        </div>
                    </div>
                </div>

                <div class="column">
                    <div class="field">
                        <label class="label">Շենք/Տուն</label>
                        <div class="control">
                            <input class="input" v-model="form.house" placeholder="Շենք/Տուն">
                        </div>
                    </div>
                </div>

                <div class="column">
                    <div class="field">
                        <label class="label">Բնակարան</label>
                        <div class="control">
                            <input class="input" v-model="form.apartment" placeholder="Բնակարան">
                        </div>
                    </div>
                </div>
            </div>

            <div class="columns">
                <div class="column">
                    <div class="field">
                        <label class="checkbox">
                            <input type="checkbox" v-model="form.unknown_person" />
                            Չի ցանկացել ներկայանալ
                        </label>
                    </div>
                </div>
            </div>
        </div>
        <!-- Submit -->
        <div class="field mt-5 has-text-centered">
            <button
            type="submit"
            class="button is-primary is-medium"
            @click.prevent="saveEmployee"
            >
            Պահպանել
            </button>
        </div>
    </form>                     
</template>

<script>
import axios from 'axios'

export default {
    name: 'Form',

    data() {
        return {
            form: {
                unknown_person: false, // ✅ Boolean
                name: "",
                surname: "",
                phone: "",
                region_id: null,
                precinct_id: null,
                position_id: null,
                apartment: "",
                house: "",
                street: ""
            }
        }
    },

    methods: {
        loadPrecincts() {
            if (!this.form.region_id) return;

            // Determine which URL to call
            const url =
            this.$store.state.user.caller === "ԷՊԾ աշղատակից"
                ? "/api/ekopatrol/precinct/"
                : "/api/ekopatrol/cities/";

            axios
                .get(url, {
                    params: { id: this.form.region_id },
                })
                .then((res) => {
                    // Store the response in precincts
                    this.$store.state.user.precincts = res.data;
                })
                .catch((err) => {
                    console.error(err);
                });
        },
        loadVillage() {
            if (!this.form.precinct_id) return 
            
            const url =
            this.$store.state.user.caller === "ԷՊԾ աշղատակից"
                ? "/api/ekopatrol/position/"
                : "/api/ekopatrol/villages/";
            axios
                .get(url, { 
                    params: { id: this.form.precinct_id } 
                }) 
                .then(
                    res => { 
                        this.$store.state.user.position = res.data 
                }) 
                .catch(err => { console.error(err) }) 
            
        },
        saveEmployee() {
            const payload = this.$store.state.user.caller === "ԷՊԾ աշղատակից"
            ?   {
                    ...this.form,
                    precinct_id: this.form.precinct_id || null,
                }
            :   {
                    ...this.form,
                    name: this.form.name || null,
                    surname: this.form.surname || null,
                    phone: this.form.phone || null,
                    region_id: this.form.region_id || null,
                    city_id: this.form.precinct_id || null,
                    village_id: this.form.position_id || null,
                    street: this.form.street || null,
                    house: this.form.house || null,
                    apartment: this.form.apartment || null,
                    unknown_person: this.form.unknown_person || false,
                }
            const url = 
            this.$store.state.user.caller === "ԷՊԾ աշղատակից"
            ? '/api/ekopatrol/addEmployeeCaller/'
            : '/api/ekopatrol/addCitizenCaller/'

            axios.post(url, payload)
                .then(() => alert('Պահպանված է'))
                .catch(err => console.error(err))
        }
    }
}
</script>