<template>
  <p class="mt-4 mb-0 body-1">
    <router-link :to="{ name: 'GeneratePosterPage' }">
      Générer votre affiche avec notre outil en ligne
    </router-link>
  </p>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return !!this.$store.state.loggedUser
    },
  },
}
</script>
