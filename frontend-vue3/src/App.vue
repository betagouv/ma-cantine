<template>
  <div>
    <DsfrSkipLinks :links="[{ text: 'Contenu', id: 'contenu' }]" />
    <DsfrHeader
      service-title="ma cantine"
      :quick-links="[
        { label: 'S\'identifier', href: authUrl('/s-identifier') },
        { label: 'Créer mon compte', href: authUrl('/creer-mon-compte') },
      ]"
    >
      <DsfrNavigation
        :nav-items="[
          { text: 'Test', to: '/test' },
          { title: 'Test menu', links: [{ text: 'Test', to: '/test' }] },
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
