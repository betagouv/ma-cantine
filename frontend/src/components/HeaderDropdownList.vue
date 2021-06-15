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
          breakpoint: null,
          authenticationState: true,
          to: { name: "AccountSummaryPage" },
          href: null,
        },
        {
          text: "S'identifier",
          icon: "mdi-key",
          breakpoint: "smAndDown",
          authenticationState: false,
          to: null,
          href: "/s-identifier",
        },
        {
          text: "Créer un compte",
          icon: "mdi-account",
          breakpoint: "smAndDown",
          authenticationState: false,
          to: null,
          href: "/creer-mon-compte",
        },
        {
          text: "Devenir testeur",
          icon: "mdi-hammer-wrench",
          breakpoint: "xs",
          authenticationState: false,
          to: { name: "TesterParticipation" },
          href: null,
        },
        {
          text: "Publier",
          icon: "mdi-publish",
          breakpoint: null,
          authenticationState: true,
          to: { name: "CanteenInfo" },
          href: null,
        },
        {
          text: "Autodiagnostic",
          icon: "mdi-chart-pie",
          breakpoint: null,
          authenticationState: null,
          to: { name: "DiagnosticPage" },
          href: null,
        },
        {
          type: "divider",
          breakpoint: null,
          authenticationState: null,
        },
        {
          text: "Nos cantines",
          icon: "mdi-silverware-fork-knife",
          breakpoint: null,
          authenticationState: null,
          to: { name: "CanteensHome" },
          href: null,
        },
        {
          text: "Blog",
          icon: "mdi-newspaper-variant-outline",
          breakpoint: null,
          authenticationState: null,
          to: { name: "BlogsHome" },
          href: null,
        },
        {
          text: "Documentation",
          icon: "mdi-file-document-outline",
          breakpoint: null,
          authenticationState: null,
          to: null,
          href: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
          target: "_blank",
        },
        {
          text: "Générer mon affiche",
          icon: "mdi-text-box-check",
          breakpoint: null,
          authenticationState: null,
          to: { name: "GeneratePosterPage" },
          href: null,
        },
        {
          type: "divider",
          breakpoint: null,
          authenticationState: null,
        },
        {
          text: "Donner son avis",
          icon: "mdi-check",
          breakpoint: null,
          authenticationState: null,
          to: null,
          href:
            "https://voxusagers.numerique.gouv.fr/Demarches/2934?&view-mode=formulaire-avis&nd_mode=en-ligne-enti%C3%A8rement&nd_source=button&key=2c212af2116e6bf85d63fee0645f8a10",
          target: "_blank",
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
