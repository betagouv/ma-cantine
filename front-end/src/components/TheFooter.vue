<template>
  <div id="footer">
    <div id="logos">
      <img src="@/assets/Marianne.png" alt="Ministère de l'Agriculture et de l'Alimentation">
      <img src="@/assets/beta-gouv-logo.png" alt="Beta gouv">
    </div>
    <div id="footer-columns">
      <div class="footer-column">
        <div class="footer-column-title">Ma Cantine</div>
        <a href="https://beta.gouv.fr/startups/ma-cantine-egalim.html" target="_blank">
          Qui sommes nous ? <i class="fas fa-external-link-alt"></i>
        </a>
        <router-link :to="{ name: 'BlogsPage' }">
          Blog
        </router-link>
        <a href="https://beta.gouv.fr/approche/" target="_blank">
          Les start-ups d'état <i class="fas fa-external-link-alt"></i>
        </a>
        <a href="mailto:contact@egalim.beta.gouv.fr">Contactez-nous !</a>
        <router-link :to="{ name: 'LegalNotices' }">Mentions légales</router-link>
      </div>
      <div class="footer-column">
        <div class="footer-column-title">Aidez-nous à améliorer cet outils</div>
        <a href="https://github.com/betagouv/ma-cantine" target="_blank">
          Contribuer sur Github <i class="fas fa-external-link-alt"></i>
        </a>
        <a href="https://github.com/betagouv/ma-cantine/issues" target="_blank">
          Envoyer une suggestion <i class="fas fa-external-link-alt"></i>
        </a>
      </div>
      <div class="footer-column">
        <div class="footer-column-title">En collaboration avec</div>
        <a href="https://agriculture.gouv.fr/thematique-generale/alimentation" target="_blank">
          DGAL (Ministère de l'agriculture) <i class="fas fa-external-link-alt"></i>
        </a>
        <a href="https://beta.gouv.fr/" target="_blank">
          beta.gouv.fr <i class="fas fa-external-link-alt"></i>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TheFooter',
}
</script>

<style scoped lang="scss">
  #footer {
    display: flex;
    padding: 50px;
  }

  #logos {
    width: 240px;
    min-height: 300px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    img {
      // without this, safari stretches the height of beta logo
      width: 240px;
    }
  }

  #footer-columns {
    width: 100%;
    display: flex;
    justify-content: space-around;
    margin-left: 30px;
  }

  .footer-column {
    display: flex;
    flex-direction: column;
    font-size: 14px;
    color: $dark-grey;
    text-align: left;
  }

  .footer-column-title {
    font-weight: bold;
    line-height: 24px;
    margin-bottom: 20px;
  }

  .footer-column a {
    text-decoration: none;
    line-height: 30px;
    color: $dark-grey;
  }

  .footer-column a:hover {
    text-decoration: underline;
  }

  @media (max-width: 1000px) {
    #footer-columns {
      flex-wrap: wrap;
      justify-content: left;
    }

    .footer-column {
      padding: 20px;
    }
  }

  @media (max-width: 700px) {
    #footer {
      flex-direction: column;
    }

    #footer-columns {
      margin-left: 0;
    }
  }
</style>
