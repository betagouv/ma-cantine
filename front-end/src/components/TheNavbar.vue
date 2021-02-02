<template>
  <div id="navbar">
    <router-link :to="{ name: 'LandingPage' }" id="goto-landing">
      <img src="@/assets/Marianne.png" id="Marianne">
      <div id="brand">
        <div id="logo"><span id="ma-cantine">ma-cantine</span>.beta.gouv.fr</div>
        <div id="slogan">Pour une alimentation saine, de qualité et plus durable dans nos assiettes grâce à EGAlim</div>
      </div>
    </router-link>
    <router-link :to="{ name: 'KeyMeasuresPage' }" class="navbar-item">Mesures phares</router-link>
    <a class="navbar-item about" href="https://beta.gouv.fr/startups/ma-cantine-egalim.html" target="_blank">
      À propos <i class="fas fa-external-link-alt"></i>
    </a>
    <a class="navbar-item" href="https://jennifer-stephan.gitbook.io/ma-cantine-egalim/" target="_blank">
      Ressources <i class="fas fa-external-link-alt"></i>
    </a>
  </div>
</template>

<script>
export default {
  name: 'TheNavbar',
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  a {
    text-decoration: none;
  }

  #navbar {
    top: 0;
    z-index: 1000;
    position: fixed;
    width: 96%;
    padding: 10px 2%;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid $dark-white;
    background-color: $white;
  }

  #goto-landing {
    display: flex;
  }

  #Marianne {
    height: 75px;
  }

  #brand {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    margin-left: 50px;
    text-align: left;
    max-width: 300px;
    text-decoration: none;
  }

  #logo {
    white-space: nowrap;
    font-style: italic;
    font-weight: 200;
    font-size: 25px;
    line-height: 29px;
    color: rgba(64, 64, 64, 0.85);
  }

  #ma-cantine {
    font-weight: bold;
    color: $orange;
  }

  #slogan {
    font-size: 11px;
    font-weight: 600;
    line-height: 15px;
    color: rgba(0,0,0,0.83);
  }

  .navbar-item {
    margin: auto 0;
    border-radius: 25px;
    padding: 15px;
    font-size: 17px;
    font-weight: bold;
    line-height: 20px;
    color: rgba(64, 64, 64, 0.85);
  }

  .navbar-item:hover {
    color: $white;
    background-color: $orange;
  }

  @media (max-width: 800px) {
    #Marianne, .about {
      display: none;
    }

    #brand {
      margin-left: 0;
    }
  }

  @media (max-width: 480px) {
    #navbar {
      flex-direction: column;
      position: relative;
    }

    .navbar-item {
      text-align: left;
      margin-top: 30px;
      padding: 3px;
    }
  }
</style>
