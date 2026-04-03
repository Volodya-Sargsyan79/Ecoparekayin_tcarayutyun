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
        <router-link to="/dashboard/precinct_shift/registration" class="column is-4">
          <div class="box has-text-centered clickable">
            <span class="icon is-size-2">
              <i class="far fa-clock"></i>
            </span>
            <h2 class="title is-4 mt-4 mb-4">Գրանցամատյան էկոպարեկային ծառայության</h2>
            <p class="title is-6">հերթապաների, հերթափոխերի և երթուղիների գրանցման համակարգ</p>
          </div>
        </router-link>

        <!-- BUTTON 2 -->
         <router-link to="/dashboard/precinct_shift/information" class="column is-4">
          <div class="box has-text-centered clickable">
            <span class="icon is-size-2">
              <i class="far fa-comments"></i>
            </span>
            <h2 class="title is-4 mt-4 mb-4">Տեղեկատվություն էկոպարեկային ծառայության</h2>
            <p class="title is-6">հերթապահների, հերթափոխերի և երթուղիների վերաբերյալ</p>
          </div>
        </router-link>

        <!-- BUTTON 3 -->
        <router-link to="/dashboard/precinct_shift/search_information" class="column is-4">
          <div class="box has-text-centered clickable">
            <span class="icon is-size-2">
              <i class="far fa-comments"></i>
            </span>
            <h2 class="title is-4 mt-4 mb-4">Տեղեկատվություն որոնում էկոպարեկային ծառայության</h2>
            <p class="title is-6">հերթապահների, հերթափոխերի և երթուղիների վերաբերյալլ</p>
          </div>
        </router-link>

      </div>
    </div>
  </section>
</template>

<script>
  export default {
    name: 'Dashboard'
  }
</script>

<style lang="scss">

  .clickable {
    cursor: pointer;
  }

</style>