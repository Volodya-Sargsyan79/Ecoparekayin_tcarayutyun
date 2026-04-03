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
                    <p v-if="!form.name" class="help is-danger">
                        Պարտադիր է մուտքագրել անունը
                    </p>
                </div>
            </div>

            <div class="column">
                <div class="field">
                    <label class="label">Ազգանուն</label>
                    <div class="control">
                        <input class="input" v-model="form.surname" placeholder="Ազգանուն">
                    </div>
                    <p v-if="!form.surname" class="help is-danger">
                        Պարտադիր է մուտքագրել ազգանունը
                    </p>
                </div>
            </div>

            <div class="column">
                <div class="field">
                    <label class="label">Հեռախոս</label>
                    <div class="control">
                        <input class="input" v-model="form.phone" placeholder="(099)000000">
                    </div>
                    <p v-if="!form.phone" class="help is-danger">
                        Պարտադիր է մուտքագրել հեռախոսահամարը
                    </p>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Տեսախցիկ</label>
                    <div class="control">
                        <input class="input" type="number" v-model="form.camera" placeholder="Տեսախցիկի համարը">
                    </div>
                    <p v-if="!form.camera" class="help is-danger">
                        Պարտադիր է մուտքագրել տեսախցիկի համարը
                    </p>
                    <p v-if="errors.camera" class="help is-danger">{{ errors.camera }}</p>
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
                            {{ region.region }}
                        </option>
                    </select>
                </div>
            </div>
            <p v-if="!form.region_id" class="help is-danger">
                Պարտադիր է ընտրել Մարզային վարչություն
            </p>
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
                            {{ precinct.precinct }}
                        </option>
                    </select>
                </div>
            </div>
             <p v-if="!form.precinct_id" class="help is-danger">
                Պարտադիր է ընտրել տեղամասը
            </p>
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
             <p v-if="!form.position_id" class="help is-danger">
                Պարտադիր է ընտրել պաշտոնը
            </p>
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
   name: 'EpsEmployeeForm',

    data() {
        return {
            form: {
                name: "",
                surname: "",
                phone: "",
                camera: "",
                region_id: null,
                precinct_id: null,
                position_id: null,
            },
            errors: {
                camera: "" 
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
        saveEmployee() {
            const payload = {
                ...this.form,
                camera: this.form.camera ? parseInt(this.form.camera) : null,
                precinct_id: this.form.precinct_id || null,
            }

            axios.post("/api/ekopatrol/addEmployee/", payload)
                .then(() => {
                    axios
                        .get("/api/ekopatrol/getlastemployee/", {
                            params: { id: this.form.precinct_id }
                        })
                        .then(res => {
                            this.$store.state.user.employee = res.data
                            alert("Գրանցումը հաջողությամբ կատարվել է:") 
                            this.$router.push('/dashboard/precinct_shift/registration')
                        })
                        .catch(err => { console.error(err) })
                })
                .catch(err => {
                    this.errors.phone = "";

                    if (err.response && err.response.data) {
                        const data = err.response.data;
                        if (data.error) {
                            this.errors.camera = "Այս տեսախցիկը արդեն ավելացված է";
                        }
                    }

                    console.error(err)
                })
        }
    }
}
</script>