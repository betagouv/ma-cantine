<template>
  <div id="presentation">
    <div class="presentation-content">
      <h1>Approvisionner ma cantine en denrées de qualité</h1>
      <p>
        La loi EGAlim vise à apporter une alimentation saine, de qualité et plus durable dans nos assiettes.
      </p>
      <p>
        Vous êtes en charge de l'approvisionnement d'une restauration collective ?
      </p>
      <a :href="`${publicPath}Diagnostic approvisionnement (ma-cantine-alpha) v0.1.ods`" download class="presentation-diagnostic">
        Télécharger notre calculateur
      </a>
    </div>
    <img src="@/assets/toque.svg" class="presentation-right-image">
  </div>
</template>

<script>
  export default {
    data() {
      return {
        publicPath: process.env.BASE_URL,
      };
    },
  }
</script>

<style scoped>
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
    color: rgba(0, 0, 0, 0.60);
  }

  h1 {
    font-weight: bold;
    font-size: 37px;
    line-height: 52px;
    color: #EB5B25;
  }

  p {
    margin: 0;
  }

  .presentation-diagnostic {
    text-align: center;
    max-width: 400px;
    height: 50px;
    line-height: 50px;
    color: white;
    background-color: #EB5B25;
    border-radius: 50px;
    font-weight: bold;
    text-decoration: none;
  }

  .presentation-right-image {
    width: 450px;
    height: 400px;
  }
</style>
