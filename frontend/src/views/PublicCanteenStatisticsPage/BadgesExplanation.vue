<template>
  <DsfrAccordion :items="[{ title: 'Comment réussir les objectifs EGAlim ?' }]">
    <template v-slot:content>
      <div v-for="measure in keyMeasures" :key="measure.id">
        <v-row class="mb-2 mt-4 mx-0" align="center">
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
            Les repas servis dans la cantine comportent au moins 50 % de produits de qualité et durables dont au moins
            20 % issus de l'agriculture biologique ou en conversion en France continentale. Consultez
            <a
              href="https://ma-cantine.agriculture.gouv.fr/blog/16"
              target="_blank"
              title="notre blog - ouvre une nouvelle fenêtre"
            >
              notre blog
              <v-icon color="primary" small>mdi-open-in-new</v-icon>
            </a>
            pour le seuil des autres régions.
          </p>
        </div>
        <p v-else style="white-space: break-spaces;">{{ measure.successExplanation }}</p>
      </div>
    </template>
  </DsfrAccordion>
</template>

<script>
import DsfrAccordion from "@/components/DsfrAccordion"
import keyMeasures from "@/data/key-measures.json"

export default {
  name: "BadgesExplanation",
  components: { DsfrAccordion },
  data() {
    return {
      keyMeasures,
    }
  },
}
</script>
