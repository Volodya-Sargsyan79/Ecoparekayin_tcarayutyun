<template>
    <form class="box">
        <h3 class="title is-5 has-text-centered mb-4">
           Երթուղու գրանցում
        </h3>

        <!-- Name & Surname $ Phone-->
        <div class="columns">

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
                    <label class="label">Երթուղու թիվը</label>
                    <div class="control">
                        <input class="input" v-model="form.route_number" placeholder="Անուն">
                    </div>
                    <p v-if="!form.route_number" class="help is-danger">
                        Պարտադիր է մուտքագրել անունը
                    </p>
                </div>
            </div>

            <div class="column">
                <div class="field">
                    <label class="label">Երթուղու երկարությունը</label>
                    <div class="control">
                        <input class="input" v-model="form.route_length" placeholder="Ազգանուն">
                    </div>
                    <p v-if="!form.route_length" class="help is-danger">
                        Պարտադիր է մուտքագրել ազգանունը
                    </p>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Երթուղու նկարը</label>
                    <div class="control">
                        <input 
                            type="file" 
                            class="input" 
                            @change="handleFileUpload"
                        >
                    </div>
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
    name: 'RegionRoudeForm',

    data() {
        return {
            form: {
                region_id: null,
                precinct_id: null,
                roudenumber: null,
                roudelength: null,
                roudephoto: null,
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
             axios
                .get("/api/ekopatrol/getlastcar/", {
                    params: { id: this.form.region_id },
                })
                .then((res) => {
                    this.$store.state.user.car = res.data;
                })
                .catch((err) => {
                    console.error(err);
                });
        },
        handleFileUpload(event) {
            this.form.image = event.target.files[0]
        },
        saveCall() {
            const formData = new FormData()

            formData.append('region_id', this.form.region_id)
            formData.append('precinct_id', this.form.precinct_id)
            formData.append('route_number', this.form.route_number)
            formData.append('route_length', this.form.route_length)

            if (this.form.image) {
                formData.append('image', this.form.image)
            }

            axios
                .post('/api/ekopatrol/addroute/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(res => {
                    axios
                        .get('/api/ekopatrol/getlastroute/', {
                            params: { id: this.form.precinct_id },
                        })
                        .then((res) => {
                            this.$store.state.user.route = res.data;
                            alert("Գրանցումը հաջողությամբ կատարվել է:")
                            this.$router.push('/dashboard/precinct_shift/registration')
                            
                        })
                        .catch(err => console.error(err))
                })
                .catch(err => console.error(err))
        }
    }
}
</script>