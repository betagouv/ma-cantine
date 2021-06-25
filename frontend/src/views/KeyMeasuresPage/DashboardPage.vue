<template>
  <div>
    <h1 class="text-h4 font-weight-black my-6">Mon tableau de bord</h1>

    <v-card elevation="0" class="text-left">
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
}
</script>
