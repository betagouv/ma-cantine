<template>
  <div class="fr-text">
    <ul>
      <li v-if="displayDiagnostic.hasWasteDiagnostic">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        J’ai réalisé un diagnostic sur les causes probables de gaspillage alimentaire
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        Je n’ai pas encore réalisé un diagnostic sur les causes probables de gaspillage alimentaire
      </li>

      <li v-if="displayDiagnostic.hasWastePlan">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        J’ai mis en place un plan d’action adapté au diagnostic réalisé
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        Je n’ai pas encore mis en place un plan d’action adapté au diagnostic réalisé
      </li>

      <li v-if="appliedWasteActions">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        J’ai mis en place les actions suivantes :
        <ul class="mt-2">
          <li class="fr-text-xs ml-9 mb-1" v-for="(action, index) in appliedWasteActions" :key="`${action}-${index}`">
            {{ action }}
          </li>
        </ul>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        Je n’ai pas encore mis en place des actions concrètes contre le gaspillage
      </li>

      <li v-if="displayDiagnostic.hasWasteMeasures">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        J’ai réalisé des mesures de mon gaspillage alimentaire :
        <ul class="mt-2">
          <li class="fr-text-xs ml-9 mb-1" v-for="measure in wasteMeasures" :key="measure.label">
            {{ measure.label }} :
            <span class="font-weight-bold">{{ measure.value }}</span>
          </li>
        </ul>
      </li>

      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        Je n’ai pas encore réalisé des mesures de mon gaspillage alimentaire
      </li>

      <li v-if="canteen.reservationExpeParticipant">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        Je suis volontaire pour l’expérimentation autour de la réservation de repas
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        Je ne suis pas volontaire pour l’expérimentation autour de la réservation de repas
      </li>
    </ul>
  </div>
</template>

<script>
import wasteActions from "@/data/waste-actions.json"

export default {
  name: "WasteMeasureSummary",
  props: {
    diagnostic: {},
    centralDiagnostic: {},
    canteen: {
      type: Object,
      required: true,
    },
  },
  computed: {
    appliedWasteActions() {
      if (!this.displayDiagnostic.wasteActions?.length) return null
      return [
        ...this.displayDiagnostic.wasteActions.map((x) => wasteActions[x]),
        ...[this.displayDiagnostic.otherWasteAction],
      ].filter((x) => !!x)
    },
    wasteMeasures() {
      const diag = this.displayDiagnostic
      return [
        { label: "Reste de pain", value: diag.breadLeftovers ? `${diag.breadLeftovers} kg/an` : "—" },
        { label: "Reste plateau", value: diag.servedLeftovers ? `${diag.servedLeftovers} kg/an` : "—" },
        { label: "Reste en production", value: diag.unservedLeftovers ? `${diag.unservedLeftovers} kg/an` : "—" },
        { label: "Reste de composantes", value: diag.sideLeftovers ? `${diag.sideLeftovers} kg/an` : "—" },
      ]
    },
    usesCentralDiagnostic() {
      return this.centralDiagnostic?.centralKitchenDiagnosticMode === "ALL"
    },
    displayDiagnostic() {
      return this.usesCentralDiagnostic ? this.centralDiagnostic : this.diagnostic
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
}
</style>
