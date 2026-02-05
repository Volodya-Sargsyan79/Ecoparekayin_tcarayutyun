<template>
    <form class="box" @submit.prevent="submitForm">
        <h3 class="title is-5 has-text-centered mb-4">
            Հրդեհի ավարտ
        </h3>

        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="label">Հրդեհի մարման ժամանակը</label>
                    <div class="control">
                        <input class="input" type="datetime-local" v-model="form.end_of_fire">
                    </div>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">ԷՊԾ աշխատակիցների մասնակցության քանաք</label>
                    <div class="control">
                        <input class="input" type="text" v-model="form.eps">
                    </div>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">ԱԻՆ աշխատակիցների մասնակցության քանաք</label>
                    <div class="control">
                        <input class="input" type="text" v-model="form.ain">
                    </div>
                </div>
            </div>
        </div>
        <div class="columns">
            <div class="column">
                <div class="field">
                    <label class="label">Այրված անտառային տարածք հա</label>
                    <div class="control">
                        <input class="input" type="text" v-model="form.forest_place_burnt">
                    </div>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Այրված դաշտային տարածք հա</label>
                    <div class="control">
                        <input class="input" type="text" v-model="form.field_place_burnt">
                    </div>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Այրված ծառների քանակ</label>
                    <div class="control">
                        <input class="input" type="text" v-model="form.burnt_trees">
                    </div>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Այրված կենդանիների քանակ</label>
                    <div class="control">
                        <input class="input" type="text" v-model="form.burnt_animals">
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
      callerType: "",
      employees: [],
      citizens: [],
      regions: [],

      form: {     
        end_of_fire: null,
        eps: "",
        ain: "",
        forest_place_burnt: "",
        field_place_burnt: "",
        burnt_trees: "",
        burnt_animals: "",
   
      },
    };
  },

  watch: {

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
    loadVillageAndRever() {
        
    },
  },
};
</script>