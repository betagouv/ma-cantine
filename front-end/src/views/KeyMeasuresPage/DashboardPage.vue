<template>
  <div>
    <h1>Mon tableau de bord</h1>

    <div v-if="$jwt.token" class="action-information">
      <p>
        Les données que vous avez renseignées précédemment ont été sauvegardées.
        Vous pouvez les modifier en effectuant à nouveau
        <router-link :to="{ name: 'DiagnosticPage' }">l'auto-diagnostic "savoir où j'en suis"</router-link>.
        Votre tableau de bord sera mis à jour automatiquement.
      </p>
      <p>
        Vous pouvez choisir de valoriser les démarches entreprises dans votre établissement
        en décidant de rendre publique vos données. Les informations que vous avez
        renseignées dans l'auto-diagnostic seront donc visible sur notre page
        <router-link :to="{ name: 'CanteensHome' }">nos cantines</router-link>.
        C'est une page que vous pouvez partager avec vos élu.e.s, convives, personnels...
      </p>

      <router-link class="call-to-action" :to="{ name: 'CanteenInfo' }">Publier mes données</router-link>
    </div>

    <div v-else class="action-information">
      <p>
        Vous accédez actuellement à la plateforme en tant qu'utilisateur.trice invité.e.
        Afin de conserver vos données et enregistrer votre tableau de bord, pouvoir le modifier, le partager...
        Vous pouvez vous connecter ou créér un compte. Les données précédemment remplies seront sauvegardées automatiquement
      </p>

      <router-link class="call-to-action" :to="{ name: 'SignUpPage' }">Sauvegarder mes données</router-link>
    </div>

    <CanteenDashboard :diagnostics="diagnostics" :showResources="true"/>
  </div>
</template>

<script>
  import CanteenDashboard from '@/components/CanteenDashboard';

  export default {
    components: {
      CanteenDashboard
    },
    props: ['diagnostics'],
  };
</script>

<style scoped lang="scss">
  h1 {
    font-weight: bold;
    font-size: 48px;
    color: $green;
  }

  .action-information {
    border: 1px solid $green;
    border-radius: 10px;
    padding: 15px;
  }

  .call-to-action {
    font-size: 1.2em;
    margin: auto;
    border: none;
    background: $orange;
    border-radius: 1em;
    padding: 0.5em;
    color: $white;
    font-weight: bold;
    cursor: pointer;
    text-decoration: none;
    display: block;
    width: max-content;
  }

  .fa-check-square {
    color: $green;
  }
</style>
