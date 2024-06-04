<template>
  <v-container class="fr-text text-left">
    <v-row>
      <v-col>
        <h1 class="fr-h1">Trouver une cantine</h1>
        <p>
          Ci-dessous, cherchez un établissement pour découvrir ses initiatives pour une alimentation saine, de qualité,
          et plus durable.
        </p>
        <p>
          Vous cherchez plutôt des données à l’échelle d’une région ou département ?
          <br />
          <router-link :to="{ name: 'PublicCanteenStatisticsPage' }">
            Consulter les statistiques de votre collectivité (régions et départements)
          </router-link>
        </p>
      </v-col>
      <v-col cols="5">
        <v-img max-height="200px" contain src="/static/images/doodles-dsfr/primary/LovingDoodle.png"></v-img>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <DsfrSearchField
          v-model="searchTerm"
          placeholder="Chercher par nom ou SIRET"
          hide-details
          :searchAction="search"
        />
        <p class="my-4"><router-link :to="{ name: 'CanteensHome' }">Effectuer une recherche avancée</router-link></p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DsfrSearchField from "@/components/DsfrSearchField"

export default {
  name: "CanteenSearchLanding",
  components: { DsfrSearchField },
  data() {
    return {
      searchTerm: undefined,
    }
  },
  methods: {
    search() {
      this.$router.push({ name: "CanteensHome", query: { recherche: this.searchTerm } })
    },
  },
}
</script>
