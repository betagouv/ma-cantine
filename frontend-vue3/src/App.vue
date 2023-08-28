<template>
  <div>
    <DsfrSkipLinks :links="[{ text: 'Contenu', id: 'contenu' }]" />
    <DsfrHeader service-title="ma cantine" :quick-links="headerLinks">
      <DsfrNavigation
        :nav-items="[
          { text: 'Test', to: '/test' },
          { title: 'Questions ?', links: [{ text: 'FAQ', to: '/faq' }] },
        ]"
      />
    </DsfrHeader>
    <div id="contenu" class="fr-container">
      <router-view />
    </div>
    <DsfrFooter />
  </div>
</template>

<script>
export default {
  name: "App",
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
