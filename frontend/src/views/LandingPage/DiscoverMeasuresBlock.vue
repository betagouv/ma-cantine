<template>
  <div>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="8">
        <h2 class="text-h4 font-weight-black">Les mesures phares de la loi EGAlim en restauration collective</h2>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <p class="text-left mt-8">
      Découvrez les mesures, leurs échéances, le public cible ainsi que des ressources pour vous aider à atteindre leurs
      objectifs.
    </p>

    <v-row class="justify-center mt-8 mx-0 mx-md-n4 cta-group pa-4">
      <v-col cols="12" sm="4" v-for="measure in keyMeasures" :key="measure.id">
        <v-card
          outlined
          :ripple="false"
          :to="{ name: 'KeyMeasurePage', params: { id: measure.id } }"
          class="fill-height d-flex flex-column px-3 dsfr"
        >
          <v-card-text class="pb-1 pt-6">
            <v-icon>{{ measure.mdiIcon }}</v-icon>
          </v-card-text>
          <v-card-title class="text-body-1 text-left font-weight-bold">
            {{ measure.title }}
          </v-card-title>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4 py-4">
            <v-spacer></v-spacer>
            <v-icon color="primary">mdi-arrow-right</v-icon>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"

export default {
  data() {
    return {
      keyMeasures,
    }
  },
}
</script>
