<template>
    <form class="box">
        <h3 class="title is-5 has-text-centered mb-4">
            ԷՊԾ աշխատակից
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
                            {{ region.name }}
                        </option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Precinct -->
        <div class="field">
            <label class="label">Տեղամաս</label>
            <div class="control">
                <div class="select is-fullwidth">
                    <select v-model="form.precinct_id" @change="loadSesion">
                        <option value="">Ընտրել</option>
                        <option
                            v-for="precinct in $store.state.user.precincts"
                            :key="precinct.id"
                            :value="precinct.id"
                        >
                            {{ precinct.name }}
                        </option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Position -->
        <div class="field">
            <label class="label">Պաշտոն</label>
            <div class="control">
            <div class="select is-fullwidth">
                <select v-model="form.position_id">
                    <option value="">Ընտրել</option>
                    <option
                        v-for="position in $store.state.user.position"
                        :key="position.id"
                        :value="position.id"
                    >
                        {{ position.position_held }}
                    </option>
                </select>
            </div>
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
   name: 'EpsEmployeeForm',

    data() {
        return {
            form: {
                name: "",
                surname: "",
                phone: "",
                region_id: null,
                precinct_id: null,
                position_id: null,
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
        },
        loadSesion() {
            if (!this.form.precinct_id) return 
            
            axios
                .get("/api/ekopatrol/position/", { 
                    params: { id: this.form.precinct_id } 
                }) 
                .then(
                    res => { 
                        this.$store.state.user.position = res.data 
                }) 
                .catch(err => { console.error(err) }) 
            
        },
        saveCall() {
            const payload = {
                    ...this.form,
                    precinct_id: this.form.precinct_id || null,
                }

            axios.post("/api/ekopatrol/addEmployeeCaller/", payload)
                .then(() =>
                    this.$router.push('/dashboard/firealarm/firecaller')
                )
                .catch(err => console.error(err))
        }
    }
}
</script>