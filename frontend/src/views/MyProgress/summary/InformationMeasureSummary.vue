<template>
  <div class="fr-text">
    <ul role="list">
      <li v-if="displayDiagnostic.communicatesOnFoodQuality">
        <v-icon color="primary" class="fill-height mr-2">$check-line</v-icon>
        <div>
          J’informe mes convives sur la part de produits de qualité et durables, entrant dans la composition des repas
          servis, et sur les démarches d’acquisition de produits issus d'un PAT (projet alimentaire territorial)
          <div v-if="displayDiagnostic.communicationFrequency" class="font-weight-bold mt-2">
            {{ communicationFrequency }}
          </div>
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n’informe pas mes convives sur la part de produits de qualité et durables, entrant dans la composition des
          repas servis, ni sur les démarches d’acquisition de produits issus d'un PAT (projet alimentaire territorial)
        </div>
      </li>

      <li v-if="communicationSupports">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J’informe les convives sur la qualité des approvisionnements :
          <ul role="list" class="mt-2">
            <li class="fr-text-xs mb-1" v-for="(support, idx) in communicationSupports" :key="`${support}-${idx}`">
              {{ support }}
            </li>
          </ul>
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n'ai pas renseigné les supports utilisés pour communiquer sur la qualité des approvisionnements
        </div>
      </li>

      <li v-if="displayDiagnostic.communicatesOnFoodPlan">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J'informe sur la qualité nutritionnelle des repas
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n'informe pas sur la qualité nutritionnelle des repas
        </div>
      </li>

      <li v-if="displayDiagnostic.communicationSupportUrl">
        <v-icon color="primary" class="mr-2">$links-line</v-icon>
        <div>
          <a
            :href="displayDiagnostic.communicationSupportUrl"
            target="_blank"
            rel="noopener"
            class="grey--text text--darken-4"
          >
            Lien vers le support de communication
            <v-icon small color="grey darken-4" class="ml-1">mdi-open-in-new</v-icon>
          </a>
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n'ai pas de lien vers le support de communication
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "InformationMeasureSummary",
  props: {
    diagnostic: {},
    centralDiagnostic: {},
  },
  computed: {
    usesCentralDiagnostic() {
      return this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL"
    },
    displayDiagnostic() {
      return this.usesCentralDiagnostic ? this.centralDiagnostic : this.diagnostic
    },
    communicationFrequency() {
      return {
        REGULARLY: "Régulièrement au cours de l’année",
        YEARLY: "Une fois par an",
        LESS_THAN_YEARLY: "Moins d'une fois par an",
      }[this.displayDiagnostic.communicationFrequency]
    },
    communicationSupports() {
      if (!this.displayDiagnostic.communicationSupports?.length && !this.displayDiagnostic.otherCommunicationSupport)
        return null
      const supports = {
        DISPLAY: "Par affichage sur le lieu de restauration",
        DIGITAL: "Par voie électronique (envoi d’e-mail aux convives, sur site internet ou intranet (mairie, pronote))",
      }
      return [
        ...this.displayDiagnostic.communicationSupports.map((x) => supports[x]),
        ...[this.displayDiagnostic.otherCommunicationSupport],
      ].filter((x) => !!x)
    },
  },
}
</script>

<style scoped>
ul {
  list-style-type: none;
  padding-left: 0;
}
li {
  margin-bottom: 14px;
  display: flex;
}
li .v-icon {
  align-items: baseline;
}
</style>
