<template>
  <v-expansion-panels hover accordion tile flat>
    <v-expansion-panel>
      <v-expansion-panel-header class="px-3" expand-icon="mdi-plus" disable-icon-rotate>
        <h3 class="font-weight-medium">
          <v-icon color="primary" class="mr-2">$question-line</v-icon>
          Comment est-ce qu'on reussi les objectives EGAlim ?
        </h3>
      </v-expansion-panel-header>
      <v-expansion-panel-content class="faq-answer">
        <div v-for="measure in keyMeasures" :key="measure.id">
          <v-row class="mb-2 mt-4" align="center">
            <v-img
              width="30"
              max-width="30"
              contain
              :src="`/static/images/badges/${measure.badgeId}.svg`"
              class="mr-2"
              alt=""
            ></v-img>
            <h4>{{ measure.title }}</h4>
          </v-row>
          <div v-if="measure.id === 'qualite-des-produits'">
            <p>
              <!-- TODO: tailor by region -->
              Les repas servis dans la cantine comportent au moins 50 % de produits de qualité et durables dont au moins
              20 % issus de l'agriculture biologique ou en conversion en France continentale. Consultez
              <a href="https://ma-cantine.agriculture.gouv.fr/blog/16" target="_blank">
                notre blog
                <v-icon color="primary" small>mdi-open-in-new</v-icon>
              </a>
              pour le seuil des autres régions.
            </p>
          </div>
          <p v-else style="white-space: break-spaces;">{{ measure.successExplanation }}</p>
        </div>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "BadgesExplanation",
  data() {
    return {
      keyMeasures,
    }
  },
}
</script>
