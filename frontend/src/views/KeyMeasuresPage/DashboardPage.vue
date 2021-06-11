<template>
  <div>
    <h1 class="text-h4 font-weight-black my-6">Mon tableau de bord</h1>

    <v-card v-if="isAuthenticated" elevation="0" class="text-left">
      <v-card-text>
        Les données que vous avez renseignées précédemment ont été sauvegardées. Vous pouvez les modifier en effectuant
        à nouveau
        <router-link :to="{ name: 'DiagnosticPage' }">l'auto-diagnostic "savoir où j'en suis"</router-link>
        . Votre tableau de bord sera mis à jour automatiquement.
      </v-card-text>
      <v-card-text>
        Vous pouvez choisir de valoriser les démarches entreprises dans votre établissement en décidant de rendre
        publique vos données. Les informations que vous avez renseignées dans l'auto-diagnostic seront donc visibles sur
        notre page
        <router-link :to="{ name: 'CanteensHome' }">nos cantines</router-link>
        . C'est une page que vous pouvez partager avec vos élu.e.s, convives, personnels...
      </v-card-text>
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <GiveFeedbackLink class="mt-2 mb-n4" />
        <v-btn color="primary" class="ml-8" large :to="{ name: 'CanteenInfo' }">
          Publier mes données
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>

    <v-card v-else elevation="0" class="text-left">
      <v-card-text>
        Vous accédez actuellement à la plateforme en tant qu'utilisateur.trice invité.e. Afin de conserver vos données
        et enregistrer votre tableau de bord, pouvoir le modifier, le partager... Vous pouvez vous connecter ou créér un
        compte. Les données précédemment remplies seront sauvegardées automatiquement
      </v-card-text>
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <GiveFeedbackLink class="mt-2 mb-n4" />
        <v-btn color="primary" class="ml-8" large href="/creer-mon-compte">
          Sauvegarder mes données
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>

    <CanteenDashboard :diagnostics="diagnostics" :showResources="true" />
  </div>
</template>

<script>
import CanteenDashboard from "@/components/CanteenDashboard"
import GiveFeedbackLink from "@/components/GiveFeedbackLink"

export default {
  components: {
    CanteenDashboard,
    GiveFeedbackLink,
  },
  props: ["diagnostics"],
  computed: {
    isAuthenticated() {
      return !!this.$store.state.loggedUser
    },
  },
}
</script>
