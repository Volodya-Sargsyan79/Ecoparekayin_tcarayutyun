<template>
    <form class="box" @submit.prevent="submitForm">
        <h3 class="title is-5 has-text-centered mb-4">
            Հրդեհ
        </h3>

        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="label">Տարածքը</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.caller"  @change="callerType">
                                <option value="">Ընտրել</option>
                                <option value="Է">ԷՊԾ աշխատակից</option>
                                <option value="Ք">Քաղաքացի</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="column has-text-centered">
                <h3 class="label">Բռնկման ժամանակը</h3>
                <div class="field"> 
                    <div class="control">
                        <label class="title is-6">
                            <input type="radio" id="html" name="language" value="Yes" v-model="form.date_of_fire">
                            Այո 
                        </label>
                        <label class="title is-6">
                            <input type="radio" id="css" name="language" value="No" v-model="form.date_of_fire">
                            Ոչ
                        </label>
                    </div>
                </div> 
            </div>
            <div class="column" v-if="form.date_of_fire === 'Yes'">
                <h3 class="label">Ամիս/Օր/տարեթիվ ժամ</h3>
                <div class="field">
                    <div class="control">
                        <input class="input" type="datetime-local" v-model="form.start_of_fire">
                    </div>
                </div>
            </div>

            <div class="column">
                <label class="label"> Որտեղից են տեղեկացել</label>
                <div class="field">
                    <div class="control">
                        <input class="input"  v-model="form.from_where" placeholder="Մուքագրել անուն, ազգանուն, հեռախոս">
                    </div>
                </div>
            </div>

            <div class="column">
                <div class="field">
                    <label class="label">Տեղեկություն հրդեհի աղբյուրի վերաբերյալ</label>
                    <div class="control">
                        <input class="input"  v-model="form.the_source_of_the_fire" placeholder="Մուքագրել տվյալներ">
                    </div>
                </div>
            </div>
        </div>

        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="label">Տարածքը</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.registration" @change="loadRegions">
                                <option value="">Ընտրել</option>
                                <option value="Պ">Պետական պահպանվող տարածք</option>
                                <option value="Հ">Համայնքային տարածք</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <div class="column" v-if="form.registration !== ''">
                <div class="field">
                    <label class="label">{{ form.registration === "Պ" ? "Մարզային վարչություն" : "Մարզ"}}</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.region_id" @change="loadPrecincts">
                                <option value="">Ընտրել</option>
                                <option 
                                    v-for="region in $store.state.user.regionofall"
                                    :key="region.id"
                                    :value="region.id"
                                >
                                    {{ region.name }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="column"  v-if="form.region_id !== ''">
                <div class="field">
                    <label class="label">{{ form.registration === "Պ" ? "Պետական պահպանվող տարածք" : "Համայնքային տարածք"}}</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.loadPrecincts" @change="loadVillage">
                                <option value="">Ընտրել</option>
                                <option v-for="emp in $store.state.user.protectedAreas" 
                                    :key="emp.id" 
                                    :value="emp.id"
                                >
                                    {{ emp.name }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="column"  v-if="form.loadPrecincts !== ''">
                <div class="field">
                    <label class="label">{{ form.registration === "Պ" ? "Տարածքային" : "Գյուղական համայնքային տարածք"}}</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.community_id" @change="loadVillageAndRever">
                                <option value="">Ընտրել</option>
                                <option v-for="emp in $store.state.user.villageall" 
                                    :key="emp.id" 
                                    :value="emp.id"
                                >
                                    {{ emp.name }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Տարածքի կորդինատները</label>
                    <div class="control">
                        <div class="is-fullwidth">
                            <input class="input" type="text" v-model="form.cordinats">
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="columns">
            <div class="column has-text-centered">
                <h3 class="title is-5">Զանգ ԱԻՆ</h3>
                <div class="field"> 
                    <label class="title is-6">
                        <input type="radio" id="html" name="fav_language" value="Yes" v-model="form.yesCall">
                        Այո 
                    </label>
                    <label class="title is-6">
                        <input type="radio" id="css" name="fav_language" value="No" v-model="form.yesCall">
                        Ոչ
                    </label>
                </div>
            </div>
            <div class="column" v-if="form.yesCall === 'Yes'">
                <div class="field">
                    <label class="label">Անուն</label>
                    <div class="control">
                        <input class="input" type="text" v-model="form.name">
                    </div>
                </div>
            </div>
            <div class="column" v-if="form.yesCall === 'Yes'">
                <div class="field">
                    <label class="label">Ազգանուն</label>
                    <div class="control">
                        <input class="input" type="text" v-model="form.surname">
                    </div>
                </div>
            </div>
            <div class="column" v-if="form.yesCall === 'Yes'">
                <div class="field">
                    <label class="label">ԱԻՆ ահազամգման ժամանակը</label>
                    <div class="control">
                        <input class="input" type="datetime-local" v-model="form.call_of_date">
                    </div>
                </div>
            </div>
            <div class="column" v-if="form.yesCall === 'No'">
                <div class="field">
                    <label class="label">Ինչու չի ահազանգվել</label>
                    <div class="control">
                        <input class="input" type="text" v-model="form.why_not">
                    </div>
                </div>
            </div>
        </div>

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
import axios from "axios";

export default {
    name: "FireAlarmForm",

    data() {
        return {
            form: {
                employee: "",
                citizen: "",
                start_of_fire: "",
                date_of_fire: "",
                from_where: "",
                the_source_of_the_fire: "",
                registration: "",
                region: "",
                regionArmenia: "",
                protected_areas: "",
                community: "",
                village: "",
                cordinat: "",
                call_ain: "",
                name: "",
                surname: "",
                call_of_date: "",
                why_not: ""
            },
        };
    },
    methods: {
        callerType() { 
            const url =
                this.form.caller === 'Է'
                    ? '/api/ekopatrol/getLastEmployee/'
                    : '/api/ekopatrol/getLastCitizen/'
            axios
                .get(url)
                .then((res) => {
                    if (this.form.caller === 'Է') {
                        this.$store.state.user.employee = res.data
                        this.$store.state.user.citizen = null
                    } else {
                        this.$store.state.user.citizen = res.data
                        this.$store.state.user.employee = null
                    }
                })
                .catch((err) => {
                    console.error(err)
                })

        },
        loadRegions() {
            const rpg =
                this.form.registration === 'Պ'
                    ? '/api/ekopatrol/regions/'
                    : '/api/ekopatrol/regionArmenia/';
            axios
                .get(rpg)
                .then((res) => {
                    // Store the response in precincts
                    this.$store.state.user.regionofall = res.data;
                })
                .catch((err) => {
                    console.error(err);
            });
        },
        loadPrecincts() {
            if (!this.form.region_id) return;
            const rpg =
                this.form.registration === 'Պ'
                    ? '/api/ekopatrol/protectedAreasList/'
                    : '/api/ekopatrol/cities';
                axios
                .get(rpg, {
                    params: { id: this.form.region_id },
                })
                .then((res) => {
                    // Store the response in precincts
                    this.$store.state.user.protectedAreas = res.data;
                })
                .catch((err) => {
                    console.error(err);
                });
        },
        loadVillage() {
            const rpg =
                this.form.registration === 'Պ'
                    ? '/api/ekopatrol/reserveList/'
                    : "/api/ekopatrol/villages/";

            axios
                .get(rpg, { 
                    params: { id: this.form.loadPrecincts } 
                }) 
                .then(
                    res => { 
                        this.$store.state.user.villageall = res.data 
                }) 
                .catch(err => { console.error(err) }) 
            
        },
        saveCall() {
                console.log(this.$store.state.user.employee, this.$store.state.user.citizen, this.form, 11111111)

                // axios.post("/api/ekopatrol/addFireCall/", this.form)
                //     .then(() =>
                //         console.log(this.form, 1111111)
                //     )
                //     .catch(err => console.error(err))
        },
    },
};
</script>