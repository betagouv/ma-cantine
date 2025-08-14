<template>
  <v-container class="fr-text text-left">
    <BreadcrumbsNav />
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
          <router-link :to="{ name: 'Observatoire' }">
            Consulter les statistiques de votre collectivité (régions et départements)
          </router-link>
        </p>
      </v-col>
      <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="5">
        <v-img max-height="200px" contain src="/static/images/doodles-dsfr/primary/LovingDoodle.png"></v-img>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <DsfrSearchField
          v-model="searchTerm"
          placeholder="Recherche par nom ou SIRET de l'établissement"
          hide-details
          @search="search"
        />
        <p class="my-4">
          <router-link :to="{ name: 'CanteensHome' }" class="d-flex align-center">
            <v-icon small color="primary" class="mr-1">$arrow-right-line</v-icon>
            Effectuer une recherche avancée
          </router-link>
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import BreadcrumbsNav from "@/components/BreadcrumbsNav"
import DsfrSearchField from "@/components/DsfrSearchField"

export default {
  name: "CanteenSearchLanding",
  components: { BreadcrumbsNav, DsfrSearchField },
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
