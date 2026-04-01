<template>
  <div class="home mt-5">
    <div class="hero is-medium">
      <div class="has-text-centered pt-5">
        <h1 class="title">
          Տեղամասերի հերթափոխերի գրանցման <br />
          և առկա տեղեկատվության համակարգ
        </h1>
      </div>
    </div>
  </div>

  <section class="section">
    <div class="container">
      <div class="columns is-multiline">

        <!-- BUTTON 1 -->
        <router-link to="/dashboard/shitregister" class="column is-6">
          <div class="box has-text-centered clickable">
            <span class="icon is-size-2">
              <i class="far fa-clock"></i>
            </span>
            <h2 class="title is-4 mt-4 mb-4">Էկոպարեկային ծառայության տեղամասերի </h2>
            <p class="title is-5">շուրջօրյա հերթափոխերի գրանցման համակարգ</p>
          </div>
        </router-link>

        <!-- BUTTON 2 -->
        <div class="column is-6">
          <div class="box has-text-centered clickable" @click="shitԼist">
            <span class="icon is-size-2">
              <i class="far fa-comments"></i>
            </span>
            <h2 class="title is-4 mt-4 mb-4">Էկոպարեկային ծառայության տեղամասերի</h2>
            <p class="title is-5">ներկա հերթապահության գրաֆիկ</p>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Dashboard',
  methods: {
    shitԼist(){
      axios
        .get('/api/ekopatrol/getstationshiftlist/') 
        .then((res) => {
            // Store the response in precincts
            this.$store.state.user.stationshif = res.data;
            this.$router.push('/dashboard/firecallplase/shitinfo/shitlist') 
        })
        .catch(err => { console.error(err) }) 
    }
       
  }
}
</script>

<style lang="scss">

  .clickable {
    cursor: pointer;
  }

</style>