<template>
  <div class="fr-text">
    <ul role="list">
      <li v-if="diagnostic.hasWasteDiagnostic">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J’ai réalisé un diagnostic sur les causes probables de gaspillage alimentaire
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n’ai pas encore réalisé un diagnostic sur les causes probables de gaspillage alimentaire
        </div>
      </li>

      <li v-if="diagnostic.hasWastePlan">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J’ai mis en place un plan d’action adapté au diagnostic réalisé
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n’ai pas encore mis en place un plan d’action adapté au diagnostic réalisé
        </div>
      </li>

      <li v-if="appliedWasteActions">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J’ai mis en place les actions suivantes :
          <ul role="list" class="mt-2">
            <li class="fr-text-xs mb-1" v-for="(action, index) in appliedWasteActions" :key="`${action}-${index}`">
              {{ action }}
            </li>
          </ul>
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n’ai pas encore mis en place des actions concrètes contre le gaspillage
        </div>
      </li>

      <li v-if="diagnostic.hasWasteMeasures">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J’ai réalisé des mesures de mon gaspillage alimentaire :
          <ul role="list" class="mt-2">
            <li class="fr-text-xs mb-1" v-for="measure in wasteMeasures" :key="measure.label">
              {{ measure.label }} :
              <span class="font-weight-bold ml-1">{{ measure.value }}</span>
            </li>
          </ul>
        </div>
      </li>

      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n’ai pas encore réalisé des mesures de mon gaspillage alimentaire
        </div>
      </li>

      <li v-if="displayDonationAgreementSegment && diagnostic.hasDonationAgreement">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je propose une ou des conventions de dons à des associations habilitées d’aide alimentaire
          <ul role="list" class="mt-2">
            <li class="fr-text-xs mb-1" v-for="measure in donationMeasures" :key="measure.label">
              {{ measure.label }} :
              <span class="font-weight-bold ml-1">{{ measure.value }}</span>
            </li>
          </ul>
        </div>
      </li>

      <li v-else-if="displayDonationAgreementSegment">
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je ne propose pas de convention de dons à des associations habilitées d’aide alimentaire
        </div>
      </li>

      <li v-if="canteen.reservationExpeParticipant">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je suis volontaire pour l’expérimentation autour de la réservation de repas
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je ne suis pas volontaire pour l’expérimentation autour de la réservation de repas
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import wasteActions from "@/data/waste-actions.json"
import { applicableDiagnosticRules } from "@/utils"

export default {
  name: "WasteMeasureSummary",
  props: {
    diagnostic: {},
    canteen: {
      type: Object,
      required: true,
    },
  },
  computed: {
    appliedWasteActions() {
      if (!this.diagnostic.wasteActions?.length) return null
      return [
        ...this.diagnostic.wasteActions.map((x) => wasteActions[x]),
        ...[this.diagnostic.otherWasteAction],
      ].filter((x) => !!x)
    },
    wasteMeasures() {
      const diag = this.diagnostic
      return [
        { label: "Reste de pain", value: diag.breadLeftovers ? `${diag.breadLeftovers} kg/an` : "—" },
        { label: "Reste plateau", value: diag.servedLeftovers ? `${diag.servedLeftovers} kg/an` : "—" },
        { label: "Reste en production", value: diag.unservedLeftovers ? `${diag.unservedLeftovers} kg/an` : "—" },
        { label: "Reste de composantes", value: diag.sideLeftovers ? `${diag.sideLeftovers} kg/an` : "—" },
      ]
    },
    displayDonationAgreementSegment() {
      return applicableDiagnosticRules(this.canteen).hasDonationAgreement
    },
    donationMeasures() {
      const d = this.diagnostic
      return [
        { label: "Fréquence de dons", value: d.donationFrequency ? `${d.donationFrequency} dons/an` : "—" },
        { label: "Quantité des denrées données", value: d.donationQuantity ? `${d.donationQuantity} kg/an` : "—" },
        { label: "Type de denrées données", value: d.donationFoodType ? `${d.donationFoodType}` : "—" },
      ]
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
