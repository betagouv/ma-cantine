<template>
  <div>
    <DsfrSkipLinks :links="[{ text: 'Contenu', to: '#contenu' }]" />
    <DsfrHeader
      service-title="ma cantine"
      :quick-links="[
        { label: 'S\'identifier', to: '/s-identifier' },
        { label: 'Créer mon compte', to: '/creer-mon-compte' },
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
}
</script>
