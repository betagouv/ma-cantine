<template>
  <div class="fr-text">
    <ul role="list">
      <li v-if="diagnostic.communicatesOnFoodQuality">
        <v-icon color="primary" class="fill-height mr-2">$check-line</v-icon>
        <div>
          J’informe mes convives sur la part de produits de qualité et durables, entrant dans la composition des repas
          servis, et sur les démarches d’acquisition de produits issus d'un PAT (projet alimentaire territorial)
          <div v-if="diagnostic.communicationFrequency" class="font-weight-bold mt-2">
            {{ communicationFrequency }}
          </div>
        </div>
      </li>
      <li v-else-if="diagnosticUsesNullAsFalse || diagnostic.communicatesOnFoodQuality === false">
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n’informe pas mes convives sur la part de produits de qualité et durables, entrant dans la composition des
          repas servis, ni sur les démarches d’acquisition de produits issus d'un PAT (projet alimentaire territorial)
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          Informez-vous vos convives sur la part de produits de qualité et durables, entrant dans la composition des
          repas servis, et sur les démarches d’acquisition de produits issus d'un PAT (projet alimentaire territorial) ?
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
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          Je n'ai pas renseigné les supports utilisés pour communiquer sur la qualité des approvisionnements
        </div>
      </li>

      <li v-if="diagnostic.communicatesOnFoodPlan">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J'informe sur la qualité nutritionnelle des repas
        </div>
      </li>
      <li v-else-if="diagnosticUsesNullAsFalse || diagnostic.communicatesOnFoodPlan === false">
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n'informe pas sur la qualité nutritionnelle des repas
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          Informez-vous vos convives sur la qualité nutritionnelle des repas ?
        </div>
      </li>

      <li v-if="diagnostic.communicationSupportUrl">
        <v-icon color="primary" class="mr-2">$links-line</v-icon>
        <div>
          <a
            :href="diagnostic.communicationSupportUrl"
            target="_blank"
            rel="noopener external"
            title="Lien vers le support de communication - ouvre une nouvelle fenêtre"
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
import communicationSupports from "@/data/communication-supports.json"
import { selectListToObject, diagnosticUsesNullAsFalse } from "@/utils"
import Constants from "@/constants"

export default {
  name: "InformationMeasureSummary",
  props: {
    diagnostic: {},
  },
  computed: {
    communicationFrequency() {
      const items = selectListToObject(Constants.CommunicationFrequencies)
      return items[this.diagnostic.communicationFrequency]
    },
    communicationSupports() {
      if (!this.diagnostic.communicationSupports?.length && !this.diagnostic.otherCommunicationSupport) return null
      return [
        ...this.diagnostic.communicationSupports.map((x) => communicationSupports[x]),
        ...[this.diagnostic.otherCommunicationSupport],
      ].filter((x) => !!x)
    },
    diagnosticUsesNullAsFalse() {
      return diagnosticUsesNullAsFalse(this.diagnostic)
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
