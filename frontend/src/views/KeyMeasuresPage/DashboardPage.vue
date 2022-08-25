<template>
  <div>
    <BreadcrumbsNav />
    <h1 class="text-h4 font-weight-black my-6">Mon tableau de bord</h1>

    <v-card elevation="0" class="text-left">
      <v-card-text>
        Vous accédez actuellement à la plateforme en tant qu'utilisateur.trice invité.e. Vous pouvez créer un compte et
        enregistrer votre cantine pour profiter de toutes nos fonctionnalités.
      </v-card-text>
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <GiveFeedbackLink class="mt-2 mb-n4" />
        <v-btn color="primary" class="ml-8" large href="/creer-mon-compte">
          Créer mon compte
        </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>

    <CanteenDashboard :diagnostics="diagnostics" :showResources="true" :canteen="canteen" />
  </div>
</template>

<script>
import CanteenDashboard from "@/components/CanteenDashboard"
import GiveFeedbackLink from "@/components/GiveFeedbackLink"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  components: {
    CanteenDashboard,
    GiveFeedbackLink,
    BreadcrumbsNav,
  },
  props: ["diagnostics", "canteen"],
}
</script>
