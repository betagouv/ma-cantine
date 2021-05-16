<template>
  <nav id="navbar">
    <router-link :to="{ name: 'LandingPage' }" id="goto-landing">
      <img src="@/assets/Marianne.png" class="gov-logo" alt="Ministère de l'Agriculture et de l'Alimentation">
      <img src="@/assets/beta-gouv-logo.png" id="beta-logo" class="gov-logo" alt="Beta gouv">
      <div id="brand">
        <img id="logo" src="@/assets/logo_transparent.png" alt="Ma cantine">
        <p id="slogan">Pour une alimentation saine, de qualité et plus durable dans nos assiettes grâce à EGAlim</p>
        <p id="beta-message">
          <router-link :to="{ name: 'KeyMeasuresHome', hash: '#publish-form' }" id="tester-link">
            <i class="fas fa-tools"></i> Site en expérimentation, devenir testeur !
          </router-link>
        </p>
      </div>
    </router-link>

    <router-link :to="{ name: 'DiagnosticPage' }" class="navbar-item">Savoir où j'en suis</router-link>
    <router-link :to="{ name: 'KeyMeasuresHome' }" class="navbar-item">Les 5 mesures phares</router-link>
    <router-link :to="{ name: 'CanteenInfo' }" v-if="jwt" class="navbar-item">Publier mes données</router-link>
    <router-link :to="{ name: 'CanteensHome' }" class="navbar-item">Nos cantines</router-link>

    <div class="navbar-icons">
      <router-link :to="{ name: 'BlogsHome' }" class="navbar-icon">
        <i class="fas fa-newspaper" title="Blog"></i>
      </router-link>
      <a href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/" target="_blank" class="navbar-icon">
        <i class="fas fa-book" title="Ressources"></i>
      </a>
      <router-link :to="{ name: 'AccountSummaryPage' }" class="navbar-icon">
        <i class="fas fa-user" title="Mon compte"></i>
      </router-link>
    </div>
  </nav>
</template>

<script>
  export default {
    name: 'TheNavbar',
    data() {
      return {
        jwt: localStorage.getItem('jwt'),
      };
    },
  }
</script>

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
    align-items: center;
  }

  .gov-logo {
    height: 75px;
  }

  #beta-logo {
    margin-left: 1em;
  }

  #brand {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-left: 50px;
    text-align: left;
    max-width: 300px;
    text-decoration: none;
  }

  #logo {
    width: 13em;
  }

  #slogan {
    font-size: 11px;
    font-weight: 600;
    line-height: 15px;
    color: $light-black;
    margin: 0;
  }

  #beta-message {
    margin: 0;
    margin-top: 0.5em;
    font-size: 12px;
  }

  #tester-link {
    color: $dark-orange;
  }

  .navbar-item {
    margin: auto 0;
    border-radius: 25px;
    padding: 15px;
    font-size: 17px;
    font-weight: bold;
    line-height: 20px;
    color: $grey;
  }

  .navbar-item:hover {
    color: $white;
    background-color: $orange;
  }

  .navbar-icons {
    margin: auto 0;
    display: flex;
    width: 130px;
    justify-content: space-between;
    font-size: 25px;
  }

  .navbar-icon {
    color: $grey;
  }

  .navbar-icon:hover {
    color: $orange;
  }

  @media (max-width: 1200px) {
    .gov-logo {
      display: none;
    }

    #brand {
      margin-left: 0;
    }
  }

  @media (max-width: 750px) {
    #navbar {
      flex-direction: column;
      position: relative;
    }

    .navbar-item {
      text-align: left;
      margin-top: 30px;
      padding: 3px;
    }

    .navbar-icons {
      margin-top: 20px;
    }
  }
</style>
