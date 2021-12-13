<template>
  <v-list rounded class="text-left">
    <v-list-item-group active-class="menu-item--active">
      <div v-for="(item, index) in items" :key="index">
        <v-divider v-if="item.type === 'divider' && shouldDisplay(item)" class="my-2"></v-divider>
        <v-list-item
          v-else-if="shouldDisplay(item)"
          :to="item.to"
          :href="item.href"
          :ripple="false"
          :target="item.target"
        >
          <v-list-item-title class="body-2">
            <v-icon small color="grey darken-2" class="mt-n1 mr-2">{{ item.icon }}</v-icon>
            {{ item.text }}
          </v-list-item-title>
        </v-list-item>
      </div>
    </v-list-item-group>
  </v-list>
</template>

<script>
export default {
  name: "HeaderDropdownList",
  data() {
    return {
      items: [
        {
          text: "Mon compte",
          icon: "mdi-account",
          authenticationState: true,
          to: { name: "AccountSummaryPage" },
        },
        {
          text: "Mes cantines",
          icon: "mdi-chart-bubble",
          authenticationState: true,
          to: { name: "ManagementPage" },
        },
        {
          text: "Mon outil de suivi",
          icon: "mdi-food-apple",
          authenticationState: true,
          to: { name: "InvoicesHome" },
        },
        {
          text: "S'identifier",
          icon: "mdi-key",
          breakpoint: "smAndDown",
          authenticationState: false,
          href: "/s-identifier",
        },
        {
          text: "Créer un compte",
          icon: "mdi-account",
          breakpoint: "smAndDown",
          authenticationState: false,
          href: "/creer-mon-compte",
        },
        {
          text: "Devenir testeur",
          icon: "mdi-hammer-wrench",
          breakpoint: "xs",
          authenticationState: false,
          to: { name: "TesterParticipation" },
        },
        {
          text: "Autodiagnostic",
          icon: "mdi-chart-pie",
          authenticationState: false,
          to: { name: "DiagnosticPage" },
        },
        {
          type: "divider",
        },
        {
          text: "Mesures phares",
          icon: "mdi-playlist-check",
          authenticationState: true,
          to: { name: "KeyMeasuresHome" },
        },
        {
          text: "Nos cantines",
          icon: "mdi-silverware-fork-knife",
          to: { name: "CanteensHome" },
        },
        {
          text: "Blog",
          icon: "mdi-newspaper-variant-outline",
          to: { name: "BlogsHome" },
        },
        {
          text: "Documentation",
          icon: "mdi-file-document-outline",
          href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
          target: "_blank",
        },
        {
          text: "Générer mon affiche",
          icon: "mdi-cloud-print-outline",
          to: { name: "GeneratePosterPage" },
        },
        {
          type: "divider",
        },
        {
          text: "Contactez-nous",
          icon: "mdi-help-circle-outline",
          to: { name: "ContactPage" },
        },
        {
          text: "Donner son avis",
          icon: "mdi-check",
          href:
            "https://voxusagers.numerique.gouv.fr/Demarches/2934?&view-mode=formulaire-avis&nd_mode=en-ligne-enti%C3%A8rement&nd_source=button&key=2c212af2116e6bf85d63fee0645f8a10",
          target: "_blank",
        },
        {
          type: "divider",
          authenticationState: true,
        },
        {
          text: "Me déconnecter",
          icon: "mdi-exit-to-app",
          href: "/se-deconnecter",
          authenticationState: true,
        },
      ],
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
  methods: {
    shouldDisplay(item) {
      if (item.authenticationState === true && !this.loggedUser) return false
      if (item.authenticationState === false && this.loggedUser) return false
      if (item.breakpoint && !this.$vuetify.breakpoint[item.breakpoint]) return false
      return true
    },
  },
}
</script>

<style scoped>
.v-list--rounded .v-list-item,
.v-list--rounded .v-list-item::before,
.v-list--rounded .v-list-item > .v-ripple__container {
  border-radius: 12px !important;
}
</style>
