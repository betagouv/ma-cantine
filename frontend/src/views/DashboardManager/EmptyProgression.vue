<template>
  <v-card outlined class="pa-4">
    <v-row>
      <v-col cols="12" sm="6" md="5" class="d-flex flex-column">
        <div v-for="measure in keyMeasures" :key="measure.id" class="d-flex my-3">
          <p class="text-body-1 font-weight-bold my-0">
            <v-icon class="mr-2" size="20" :color="measure.mdiIconColor">{{ measure.mdiIcon }}</v-icon>
            {{ measure.shortTitle }}
          </p>
          <v-spacer></v-spacer>
          <v-chip small>À COMPLÈTER</v-chip>
        </div>
      </v-col>
      <v-col cols="12" sm="6" md="7" class="text-center">
        <v-card color="primary lighten-5 fill-height rounded">
          <v-card-text class="font-weight-bold">Tout est prêt pour se lancer !</v-card-text>
          <v-card-text>
            Réalisez un premier bilan, complet ou intermédiaire, pour mesurer votre avancée par rapport aux objectifs de
            la loi EGAlim, et parcourez des ressources personnalisées selon votre situation et vos résultats pour vous
            aider dans votre transition vers une alimentation plus durable.
          </v-card-text>
          <div>
            <v-btn color="primary">Faire le bilan</v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "EmptyProgression",
  computed: {
    keyMeasures() {
      return keyMeasures
    },
  },
}
</script>
