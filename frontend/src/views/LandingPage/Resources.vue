<template>
  <div>
    <v-row>
      <v-col cols="12" sm="4" v-for="resource in resources" :key="resource.title">
        <v-card elevation="0">
          <v-card-title class="text-body-1 text-left font-weight-bold">
            <v-icon color="grey darken-3 mr-2">{{ resource.icon }}</v-icon>
            <span class="ml-2">{{ resource.title }}</span>
          </v-card-title>
          <v-card-text class="text-left">
            {{ resource.description }}
          </v-card-text>
          <v-card-actions class="px-4">
            <v-btn
              outlined
              color="primary"
              :to="resource.to"
              :href="resource.url"
              :target="resource.url ? '_blank' : null"
              :rel="resource.url ? 'noopener noreferrer' : null"
            >
              {{ resource.ctaText }}
              <v-icon v-if="resource.url" small class="ml-2">mdi-open-in-new</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  data() {
    const resources = []
    if (this.$store.state.loggedUser) {
      resources.push({
        title: "Générer mon affiche",
        icon: "$article-fill",
        description: "Obtenez un PDF à afficher ou à envoyer par mail à vos convives",
        url: null,
        to: { name: "GeneratePosterPage" },
        ctaText: "Générer mon affiche",
      })
    } else {
      resources.push({
        title: "Autodiagnostic",
        icon: "mdi-chart-pie",
        description: "Simulez un diagnostic avec les données de votre établissement",
        url: null,
        to: { name: "DiagnosticPage" },
        ctaText: "Rentrer mes données",
      })
    }
    resources.push({
      title: "Communauté",
      icon: "$team-fill",
      description: "Découvrez nos événements et échangez avec des autres gestionnaires",
      url: null,
      to: { name: "CommunityPage" },
      ctaText: "Rencontrer la communauté",
    })
    resources.push({
      title: "Documentation",
      icon: "$book-2-fill",
      description: "Ressources pour les acteurs et actrices de la restauration collective",
      url: "https://ma-cantine-1.gitbook.io/ma-cantine-egalim/",
      to: null,
      ctaText: "Consulter nos ressources",
    })

    return { resources }
  },
}
</script>
