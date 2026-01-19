<template>
  <div class="home mt-5">
    <div class="hero is-medium">
      <div class="has-text-centered pt-5">
        <h1 class="title">
          Բարի գալուստ <br />
          Էկոպարեկային ծառայության <br />
          1-07 <br />
          ահազանգերի գրանցման համակարգ
        </h1>
      </div>
    </div>
  </div>

  <section class="section">
    <div class="container">
      <div class="columns is-multiline">

        <!-- BUTTON 1 -->
        <router-link to="/dashboard/firealarm" class="column is-4">
          <div class="box has-text-centered">
            <span class="icon is-size-2">
              <i class="far fa-clock"></i>
            </span>
            <h2 class="is-size-4 mt-4 mb-4">1-07</h2>
            <p>Հրդեհների վերաբերյալ հայտարարություններ</p>
          </div>
        </router-link>

        <!-- BUTTON 2 -->
        <router-link to="/EPSAlarm" class="column is-4">
          <div class="box has-text-centered">
            <span class="icon is-size-2">
              <i class="far fa-comments"></i>
            </span>
            <h2 class="is-size-4 mt-4 mb-4">1-07</h2>
            <p>Էկոպարեկային ծառայության խախտումների վերաբերյալ հայտարարություններ</p>
          </div>
        </router-link>

        <!-- BUTTON 3 -->
        <router-link to="/CrimeAlert" class="column is-4">
          <div class="box has-text-centered">
            <span class="icon is-size-2">
              <i class="far fa-home"></i>
            </span>
            <h2 class="is-size-4 mt-4 mb-4">1-07</h2>
            <p>Հանցագործությունների վերաբերյալ հայտարարություններ</p>
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