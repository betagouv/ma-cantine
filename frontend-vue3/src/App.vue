<template>
  <div>
    <DsfrSkipLinks :links="[{ text: 'Test', to: '#test' }]" />
    <DsfrHeader
      service-title="ma cantine"
      :quick-links="[
        { label: 'S\'identifier', to: '/s-identifier' },
        { label: 'Créer mon compte', to: '/creer-mon-compmte' },
      ]"
    >
      <DsfrNavigation
        :nav-items="[
          { text: 'Test', to: '/test' },
          { title: 'Test menu', links: [{ text: 'Test', to: '/test' }] },
        ]"
      />
    </DsfrHeader>
    <div class="fr-container">
      <h1>Test DSFR</h1>
      <DsfrAlert title="Testing" />
      <router-link :to="{ path: 'test' }">Testing</router-link>
    </div>
    <DsfrFooter />
  </div>
</template>

<script>
export default {
  name: "App",
}
</script>
