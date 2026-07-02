<template>
    <form class="box">
        <h3 class="title is-5 has-text-centered mb-6">Ապօրինի ծառահատում գրանցում</h3>
        <div class="columns box">
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
                            <select v-model="form.precinct_id">
                                <option value="">Ընտրել</option>
                                <option v-for="precinct in $store.state.user.precincts" :key="precinct.id" :value="precinct.id">{{ precinct.precinct }}</option>
                            </select>
                        </div>
                    </div>
                    <p v-if="!form.precinct_id" class="help is-danger">Պարտադիր է ընտրել տեղամասը</p>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">Պաշտոն</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.position_id" @change="loadRoute">
                                <option value="">Ընտրել</option>
                                <option v-for="position in $store.state.user.position" :key="position.id" :value="position.id">{{ position.position_held }}</option>
                            </select>
                        </div>
                    </div>
                    <p v-if="!form.position_id" class="help is-danger">Պարտադիր է ընտրել պաշտոնը</p>
                </div>
            </div>
            <div class="column">
                <div class="field">
                    <label class="label">ԷՊ ծառայող</label>
                    <div class="control">
                        <div class="select is-fullwidth">
                            <select v-model="form.employee_01_id">
                                <option value="">Ընտրել</option>
                                <option v-for="employee in $store.state.user.employee" :key="employee.id" :value="employee.id">
                                    {{ employee.name }} {{ employee.surname }} {{ employee.phone }} 
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
                <p v-if="!form.employee_01_id" class="help is-danger">Պարտադիր է ընտրել տեղամասը</p>
            </div>
        </div>
        <div class="columns box mt-2">
            <div class="column is-1">
                <div class="field">
                    <div class="control">
                        <input type="number" v-model="form.սtumps" class="input" placeholder="Մուտքագրել կոճղերի քանակը" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Կոճղերի քանակ</label>
                </div>
            </div>
            <div class="column is-1">
                <div class="field">
                    <div class="control">
                        <input type="number" v-model="form.trees" class="input" placeholder="Մուտքագրել ծառերի քանակը" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Կտրված ծառերի քանակ</label>
                </div>
            </div>
            <div class="column is-1">
                <div class="field">
                    <div class="control">
                        <input type="number" v-model="form.wood" class="input" placeholder="Մուտքագրել փայտի մ3 քանակը" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Փայտի քանակ</label>
                </div>
            </div>
            <div class="column is-2">
                <div class="field">
                    <div class="control">
                        <input type="text" v-model="form.person" class="input" placeholder="Անուն, ազգանուն" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Իրավախաղտի անուն, ազգանուն</label>
                </div>
            </div>
            <div class="column is-3">
                <div class="field">
                    <div class="control">
                        <input type="text" v-model="form.address" class="input" placeholder="Հասցե" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Իրավախաղտի բնակության վայր</label>
                </div>
            </div>
            <div class="column is-1">
                <div class="field">
                    <div class="control">
                        <input type="text" v-model="form.passport" class="input" placeholder="Փաստաթուցթ" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Անձը հաստատող փաստաթուղթ</label>
                </div>
            </div>
            <div class="column is-1">
                <div class="field">
                    <div class="control">
                        <input type="text" v-model="form.phone" class="input " placeholder="Հեռ․" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Հեռախոս</label>
                </div>
            </div>
            <div class="column is-2">
                <div class="field">
                    <div class="file-upload">
                        <input
                            type="file"
                            id="woodImage"
                            accept="image/*"
                            multiple
                            @change="onFileChangeForWood"
                        />

                        <label for="woodImage">
                            📷 Նկար բեռնել
                        </label>
                    </div>

                    <label class="label has-text-centered" style="font-size:10px;">
                        Փոխադրամիջոցի նկարներ
                    </label>
                </div>
            </div>
        </div>
        <div v-if="form.imageWoodPreviews?.length" class="mt-4 mb-5">
            <h3 class="title is-5 has-text-centered mb-3">Նկարներ</h3>
            <div class="columns box mt-2">
                <div class="column">
                    <div class="field">
                        <div class="preview-images">
                            <img
                                v-for="(image, index) in form.imageWoodPreviews"
                                :key="index"
                                :src="image"
                                class="preview-image"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="columns box mt-2">
            <div class="column is-4">
                <div class="field">
                    <div class="control">
                        <input type="text" v-model="form.please" class="input" placeholder="Հասցե" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Հայտնաբերված իրավախղտման վայր</label>
                </div>
            </div>
            <div class="column is-1">
                <div class="field">
                    <div class="control">
                        <input type="text" v-model="form.car" class="input" placeholder="Անվանում" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Փոխադրամիջոց</label>
                </div>
            </div>
            <div class="column is-1">
                <div class="field">
                    <div class="control">
                        <input type="text" v-model="form.number" class="input" placeholder="Պետհամարանիշ" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Պետհամարանիշ</label>
                </div>
            </div>
            <div class="column is-2">
                <div class="field">
                    <div class="file-upload">
                        <input
                            type="file"
                            id="deviceImage"
                            accept="image/*"
                            multiple
                            @change="onFileChange"
                        />

                        <label for="deviceImage">
                            📷 Նկար բեռնել
                        </label>
                    </div>

                    <label class="label has-text-centered" style="font-size:10px;">
                        Փոխադրամիջոցի նկարներ
                    </label>
                </div>
            </div>
            <div class="column is-2">
                <div class="field">
                    <div class="control">
                        <input type="text" v-model="form.druzhba" class="input" placeholder="Անվանում" style="font-size: 12px; height: 38px;">
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Փայտ կտրելու միջոց</label>
                </div>
            </div>
            <div class="column is-2">
                <div class="field">
                    <div class="file-upload">
                        <input
                            type="file"
                            id="plateImage"
                            accept="image/*"
                            multiple
                            @change="onFileChangeForDruzhba"
                        />

                        <label for="plateImage">
                            📷 Նկար բեռնել
                        </label>
                    </div>
                    <label class="label has-text-centered"  style="font-size: 10px;">Սարքի նկարներ</label>
                </div>
            </div>
        </div>
        <div v-if="form.imagePreviews?.length" class="mt-4">
            <h3 class="title is-5 has-text-centered mb-3">Փոխադրամիջոցի նկարներ</h3>
            <div class="columns box mt-2">
                <div class="column">
                    <div class="field">
                        <div class="preview-images">
                            <img
                                v-for="(image, index) in form.imagePreviews"
                                :key="index"
                                :src="image"
                                class="preview-image"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="form.imagePreviewsDruzhba?.length" class="mt-5">
            <h3 class="title is-5 has-text-centered mb-3">Սարքի նկարներ</h3>
            <div class="columns box mt-2">
                <div class="column">
                    <div class="field">
                        <div class="preview-images">
                            <img
                                v-for="(image, index) in form.imagePreviewsDruzhba"
                                :key="index"
                                :src="image"
                                class="preview-image"
                            />
                        </div>
                    </div>
                </div>
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
        name: 'RegistrationIllegalLogging',
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
                    route_id: null,          
                    selectedImages: [],
                    imagePreviews: [],
                    imageWoodPreviews: [],
                    selectedImagesWood: [],
                    selectedImagesDruzhba: [],
                    imagePreviewsDruzhba: []
                },
      
            }
        },
        methods: {
            loadRegion() {
                if (!this.form.region_id) return;
                axios
                    .get("/api/legalization/precincts/", {
                        params: { id: this.form.region_id },
                    })
                    .then((res) => {
                        this.$store.state.user.precincts = res.data;
                    })
                    .catch((err) => {
                        console.error(err);
                    });
            },
            loadRoute() {
                if (!this.form.position_id) return;
                axios
                    .get("/api/legalization/getemployee/",{
                        params: { precinct_id: this.form.precinct_id, position_id: this.form.position_id },
                    })
                    .then(res => {
                        this.$store.state.user.employee = res.data
                    })
                    .catch(err => { console.error(err) })
            },
            onFileChangeForWood(event) {
                const files = Array.from(event.target.files);
                this.form.selectedImagesWood = files;
                files.forEach(file => {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.form.imageWoodPreviews.push(e.target.result);
                    };
                    reader.readAsDataURL(file);
                });
                event.target.value = null;
            },
            onFileChange(event) {
                const files = Array.from(event.target.files);
                this.form.selectedImages = files;
                files.forEach(file => {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.form.imagePreviews.push(e.target.result);
                    };
                    reader.readAsDataURL(file);
                });
                event.target.value = null;
            },
            onFileChangeForDruzhba(event) {
                const files = Array.from(event.target.files);
                this.form.selectedImagesDruzhba = files;
                files.forEach(file => {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        this.form.imagePreviewsDruzhba.push(e.target.result);
                    };
                    reader.readAsDataURL(file);
                });
                event.target.value = null;
            },
            saveCall() {
                axios.post("/api/ecopatrol/addstationshift/", this.form)
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
<style scoped>
    .file-upload input[type="file"] {
        display: none;
    }

    .file-upload label {
        display: inline-flex;
        align-items: center;
        justify-content: center;

        height: 38px;
        width: 100%;
        padding: 0 12px;

        background: #fff;

        color: black;

        font-size: 12px;
        border-radius: 6px;
        border: 1px solid #dbdbdb;

        cursor: pointer;
        transition: 0.2s;
    }

    .file-upload label:hover {
        background: #ededed;
    }

    .preview-images{
        display:flex;
        flex-wrap:wrap;
        gap:10px;
        margin-top:10px;
    }

    .preview-image{
        width:100px;
        height:100px;
        object-fit:cover;
        border:1px solid #ddd;
        border-radius:5px;
    }
</style>