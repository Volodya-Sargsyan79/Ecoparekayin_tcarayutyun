<template>
  <div class="home mt-5">
    <div class="hero is-medium">
      <div class="has-text-centered pt-5">
        <h1 class="title">
          Իրավախաղտումների գրանցում <br />
          և տեղեկատվության իրավախաղտումների վերաբերյալ
        </h1>
      </div>
    </div>
  </div>
  <section class="section">
    <div class="container">
      <div class="columns is-multiline">
        <router-link to="/dashboard/precinct_shift/registration" class="column is-6">
          <div class="box has-text-centered clickable">
            <span class="icon is-size-2">
              <i class="far fa-clock"></i>
            </span>
            <h2 class="title is-4 mt-4 mb-4">Գրանցամատյան</h2>
            <p class="title is-6">հայտնաբերված խաղտումների վերաբերյալ</p>
          </div>
        </router-link>
         <router-link to="/dashboard/precinct_shift/information" class="column is-6">
          <div class="box has-text-centered clickable">
            <span class="icon is-size-2">
              <i class="far fa-comments"></i>
            </span>
            <h2 class="title is-4 mt-4 mb-4">Տեղեկատվություն</h2>
            <p class="title is-6">խաղտումների վերաբերյալ</p>
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