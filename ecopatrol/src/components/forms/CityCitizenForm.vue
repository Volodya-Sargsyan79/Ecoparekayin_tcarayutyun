<template>
    <form class="box">
        <h3 class="title is-5 has-text-centered mb-4">
            Քաղաքացի
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
            <label class="label">Մարզ</label>
            <div class="control">
                <div class="select is-fullwidth">
                    <select v-model="form.region_id" @change="loadPrecincts">
                        <option value="">Ընտրել</option>
                        <option
                            v-for="region in $store.state.user.regionArmenia"
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
            <label class="label">Համայնք</label>
            <div class="control">
                <div class="select is-fullwidth">
                    <select v-model="form.precinct_id" @change="loadVillage">
                        <option value="">Ընտրել</option>
                        <option
                            v-for="precinct in $store.state.user.city"
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
            <label class="label">Գյուղական համայնք</label>
            <div class="control">
            <div class="select is-fullwidth">
                <select v-model="form.position_id">
                    <option value="">Ընտրել</option>
                    <option
                        v-for="position in $store.state.user.village"
                        :key="position.id"
                        :value="position.id"
                    >
                        {{ position.name }}
                    </option>
                </select>
            </div>
            </div>
        </div>

        <!-- Street, House, Apartment -->
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
    name: 'Form',

    data() {
        return {
            form: {
                unknown_person: false, // ✅ Boolean
                name: null,
                surname: null,
                phone: null,
                region_id: null,
                precinct_id: null,
                position_id: null,
                apartment: null,
                house: null,
                street: null
            }
        }
    },

    methods: {
        loadPrecincts() {
            if (!this.form.region_id) return;

            axios
                .get("/api/ekopatrol/cities/", {
                    params: { id: this.form.region_id },
                })
                .then((res) => {
                    // Store the response in precincts
                    this.$store.state.user.city = res.data;
                })
                .catch((err) => {
                    console.error(err);
                });
        },
        loadVillage() {
            if (!this.form.precinct_id) return 
            
            axios
                .get("/api/ekopatrol/villages/", { 
                    params: { id: this.form.precinct_id } 
                }) 
                .then(
                    res => { 
                        this.$store.state.user.village = res.data 
                }) 
                .catch(err => { console.error(err) }) 
            
        },
        saveCall() {
            const payload = {
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

            axios.post("/api/ekopatrol/addCitizenCaller/", payload)
                .then(() => 
                    this.$router.push('/dashboard/firealarm/firecaller')
                )
                .catch(err => console.error(err))
        }
    }
}
</script>