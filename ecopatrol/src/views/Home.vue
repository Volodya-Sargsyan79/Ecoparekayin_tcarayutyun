<template>
  <div class="home">
    <div class="hero is-medium">
      <div class="hero-body has-text-centered">
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
              Eco-patrol service employees
            </h2>
            <p>This is just some random placeholder text</p>
          </div>
        </div>

        <div class="column is-4">
          <div class="box has-text-centered">
            <span class="icon is-size-2 is-size-info">
              <i class="far fa-comments"></i>
            </span>
            <h2 class="is-size-4 mt-4 mb-4">
              People who made the bet
            </h2>
            <p>This is just some random placeholder text</p>
          </div>
        </div>

        <div class="column is-4">
          <div class="box has-text-centered">
            <span class="icon is-size-2 is-size-info">
              <i class="far fa-home"></i>
            </span>
            <h2 class="is-size-4 mt-4 mb-4">
              The machines that made the draw
            </h2>
            <p>This is just some random placeholder text</p>
          </div>
        </div>
        
        <div class="column is-12 has-text-centered">
          <a href="/log-in" class="button is-size-3 mt-6 mb-6" style="background: #163820; color:#ffffff;">
            Click to get starte
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
