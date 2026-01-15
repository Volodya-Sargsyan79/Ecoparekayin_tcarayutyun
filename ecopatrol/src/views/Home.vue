<template>
  <div class="home mt-5">
    <div class="hero is-medium">
      <div class="has-text-centered pt-5">
        <h1 class="title">Welcome to Eco-patrol</h1>
        <h2 class="subtitle">An online place for searching what you want</h2>
      </div>
    </div>
  </div>
  
  <section class="section">
    <div class="container">
      <div class="columns is-multiline">
        <div class="column is-4">
          <div class="box has-text-centered">
            <span class="icon is-size-2 is-size-info">
              <i class="far fa-clock"></i>
            </span>
            <h2 class="is-size-4 mt-4 mb-4">
              Էկոպարեկային ծառայության աշխատակիցներ
            </h2>
            <p>Ներկա պահին գործող</p>
          </div>
        </div>

        <div class="column is-4">
          <div class="box has-text-centered">
            <span class="icon is-size-2 is-size-info">
              <i class="far fa-comments"></i>
            </span>
            <h2 class="is-size-4 mt-4 mb-4">
              Էկոպարեկային ծառայության դիմորտներ
            </h2>
            <p>Դիմել են կամ դեռ ընթացքի մեջ է</p>
          </div>
        </div>

        <div class="column is-4">
          <div class="box has-text-centered" href="/log-in">
            <span class="icon is-size-2 is-size-info">
              <i class="far fa-home"></i>
            </span>
            <h2 class="is-size-4 mt-4 mb-4">
              Էկոպարեկային ծառայության նախքին աշխատակիցներ
            </h2>
            <p>Հեռացված կամ դիմումին համաձայն ազատված</p>
          </div>
        </div>
        
        <div class="column is-12 has-text-centered">
          <a href="/log-in" class="button is-size-3 mt-6 mb-6" style="background: #163820; color:#ffffff;">
            Մուտք գքրծել համակարգ
          </a>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Home'
}
</script>
