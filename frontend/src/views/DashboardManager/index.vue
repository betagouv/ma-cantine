<template>
  <div class="text-left">
    <p class="my-4 text-h5 font-weight-bold">Bienvenue {{ loggedUser.firstName }}</p>

    <p class="mt-8 mb-2 text-h6 font-weight-bold">
      Ma progression
    </p>
    <p class="body-2">
      Vous trouverez ci-dessous une vue d'ensemble de votre progression sur les cinq volets de la loi EGAlim.
    </p>

    <div>
      <EgalimProgression v-if="hasProgression" />
      <EmptyProgression v-else />
    </div>

    <p class="mt-10 mb-2 text-h6 font-weight-bold">
      Mon établissement
    </p>
    <p class="body-2">
      Accédez ci-dessous aux différents outils de gestion de votre établissement sur la plateforme « ma cantine ».
    </p>

    <p class="mt-10 mb-2 text-h6 font-weight-bold">
      Mes ressources personalisées
    </p>
    <p class="body-2">
      Découvrez ci-dessous des articles et des outils pratiques, ainsi que des suggestions de partenaires et des
      cantines inspirantes sur votre territoire qui correspondent à vos enjeux.
    </p>
  </div>
</template>

<script>
import EmptyProgression from "./EmptyProgression.vue"
import EgalimProgression from "./EgalimProgression.vue"

export default {
  name: "DashboardManager",
  components: { EmptyProgression, EgalimProgression },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
    hasProgression() {
      return true
    },
  },
}
</script>
