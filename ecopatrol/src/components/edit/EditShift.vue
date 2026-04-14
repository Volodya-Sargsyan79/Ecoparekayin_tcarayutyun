<template>
    <form class="box">
        <h3 class="title is-5 has-text-centered mb-4">
            Ավելացնել զեկուցագիր կամ տեղեկություն
        </h3>

        <div class="columns">
             <!-- Text input -->
            <div class="column is-6">
                <div class="field">
                    <label class="label">Տեքստ</label>
                    <div class="control">
                        <textarea
                            class="textarea"
                            placeholder="Գրեք ձեր տեքստը այստեղ..."
                            v-model="form.text" 
                        ></textarea>
                    </div>
                </div>
            </div>

            <!-- PDF upload -->
            <div class="column is-6">
                <div class="field">
                    <label class="label">PDF ֆայլ</label>
                    <div class="control">
                        <input 
                            type="file" 
                            accept=".pdf"
                            @change="form.PDF = $event.target.files[0]"
                        />
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
    name: 'EditShift',

    data() {
        return {
            form: {
                PDF: null,
                text: null,
            }
        }
    },

    methods: {
        saveCall() {
            
           const formData = new FormData()
    
            formData.append('shift', this.$route.params.id)
            
            if (this.form.text) {
                formData.append('text', this.form.text)
            }
            
            if (this.form.PDF) {
                formData.append('PDF', this.form.PDF)
            }

            axios.post("/api/ekopatrol/addinformationforshift/", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then((res) => {
                this.$store.state.user.stationshif = res.data
                alert("Գրանցումը հաջողությամբ կատարվել է:")
                this.$router.push(`/dashboard/precinct_shift/information/shift/${this.$route.params.id}`)
            })
            .catch(err => {
                alert("Հերթափոխն արդեն գրանցված է:")
                console.error(err)
            })
        }
    }
}
</script>