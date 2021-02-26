<template>
  <div id="presentation">
    <div class="presentation-content">
      <h1>Diagnostiquer ma cantine sur les mesures de la loi EGAlim</h1>
      <p>
        La loi EGAlim vise à apporter une alimentation saine, de qualité et plus durable dans nos assiettes.
      </p>
      <router-link :to="{ name: 'DiagnosticPage' }" class="presentation-diagnostic">
        Savoir où j'en suis des mesures EGAlim
      </router-link>
    </div>
    <img src="@/assets/toque.svg" class="presentation-right-image">
  </div>
</template>

<style scoped lang="scss">
  #presentation {
    display: flex;
    justify-content: space-around;
    padding: 20px;
  }

  .presentation-content {
    text-align: left;
    max-width: 600px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    font-size: 20px;
    color: $dark-grey;
  }

  h1 {
    line-height: 52px;
    color: $orange;
  }

  p {
    margin: 0;
  }

  .presentation-diagnostic {
    text-align: center;
    width: 350px;
    height: 50px;
    line-height: 50px;
    color: $white;
    background-color: $orange;
    border-radius: 50px;
    font-weight: bold;
    text-decoration: none;
  }

  .presentation-right-image {
    width: 450px;
    height: 400px;
  }

  @media (max-width: 1000px) {
    .presentation-content {
      p {
        margin: 15px 0;
      }
    }

    .presentation-diagnostic {
      margin: 30px auto 0 auto;
    }
  }

  @media (max-width: 900px) {
    .presentation-right-image {
      display: none;
    }
  }

  @media (max-width: 480px) {
    .presentation-content {
      text-align: center;
    }
  }
</style>
