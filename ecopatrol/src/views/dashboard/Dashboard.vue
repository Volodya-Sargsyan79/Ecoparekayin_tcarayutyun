<template>
  <div class="home mt-5">
    <div class="hero is-medium">
      <div class="has-text-centered pt-5">
        <h1 class="title">
          Բարի գալուստ <br />
          Էկոպարեկային ծառայության <br />
          տեղեկատվական համակարգ
        </h1>
      </div>
    </div>
  </div>
  <section class="section">
    <div class="container">
      <div class="columns is-multiline">
        <router-link to="/dashboard/precinct_shift" class="column is-4">
          <div class="box has-text-centered">
            <span class="icon is-size-2">
              <i class="far fa-clock"></i>
            </span>
            <h2 class="title is-4 mt-4 mb-4">Տեղեկատվություն</h2>
            <p class="title is-5">հերթափոխերի վերաբերյալ</p>
          </div>
        </router-link>
        <div class=" column is-4">
          <div class="box has-text-centered clickable" @click="shitԼist">
            <span class="icon is-size-2">
              <i class="far fa-comments"></i>
            </span>
            <h2 class="title is-4 mt-4 mb-4">Տեղեկատվություն</h2>
            <p class="title is-5">իրավախախտումների վերաբերյալ</p>
          </div>
        </div>
        <router-link to="/CrimeAlert" class="column is-4">
          <div class="box has-text-centered">
            <span class="icon is-size-2">
              <i class="far fa-home"></i>
            </span>
            <h2 class="title is-4 mt-4 mb-4">1-07</h2>
            <p class="title is-5">ահազանգման համակարգ</p>
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