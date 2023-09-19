<template>
  <div>
    <DsfrSkipLinks :links="[{ text: 'Contenu', id: 'contenu' }]" />
    <DsfrHeader service-title="ma cantine" :quick-links="headerLinks">
      <DsfrNavigation
        :nav-items="[
          { text: 'Nos cantines', to: { name: 'CanteensHome' } },
          {
            title: 'Questions ?',
            links: [
              { text: 'FAQ', to: { name: 'FaqPage' } },
              { text: 'Contactez-nous', to: { name: 'ContactPage' } },
            ],
          },
        ]"
      />
    </DsfrHeader>
    <div id="contenu" class="fr-container">
      <router-view />
    </div>
    <DsfrFooter />
    <NotificationSnackbar />
  </div>
</template>

<script>
import NotificationSnackbar from "@/components/NotificationSnackbar"

export default {
  name: "App",
  components: { NotificationSnackbar },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    headerLinks() {
      return this.loggedUser
        ? [
            {
              // TODO: use modal for confirmation
              label: "Me déconnecter",
              href: this.authUrl("/se-deconnecter"),
            },
          ]
        : [
            { label: "S'identifier", href: this.authUrl("/s-identifier") },
            { label: "Créer mon compte", href: this.authUrl("/creer-mon-compte") },
          ]
    },
  },
  methods: {
    authUrl(path) {
      // header component will interpret a link
      // as a router-link unless it starts with http
      // https://github.com/dnum-mi/vue-dsfr/pull/54/files
      return `${location.origin}${path}`
    },
  },
}
</script>

<style lang="scss">
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // text-align: center;
}

// .constrained {
//   max-width: 1024px !important;
// }

// .v-menu__content {
//   text-align: left;
// }

// .cta-group {
//   background-color: #cacafb;
//   border-radius: 0px;
// }

// .theme--light.v-card > .v-card__text,
// .theme--light.v-card > .v-card__subtitle {
//   color: rgba(0, 0, 0, 0.87);
// }

.v-card.dsfr {
  border: solid 1px #e0e0e0;
  border-radius: 0px;
}

.v-card.dsfr:hover {
  background-color: #f6f6f6;
}
</style>
