<template>
  <DsfrBadge v-if="isCompleted && isAppro && isSatellite" :showIcon="false" mode="SUCCESS">
    Complété (par livreur)
  </DsfrBadge>
  <DsfrBadge v-else-if="isCompleted" :showIcon="false" mode="SUCCESS">Complété</DsfrBadge>
  <DsfrBadge v-else-if="isWaitingCentralKitchen" :showIcon="false" mode="NEUTRAL">
    À compléter (par livreur)
  </DsfrBadge>
  <DsfrBadge v-else-if="isRequired" :showIcon="false" mode="ERROR">À compléter (obligatoire)</DsfrBadge>
  <DsfrBadge v-else :showIcon="false" mode="WARNING">À compléter (optionnel)</DsfrBadge>
</template>

<script>
import DsfrBadge from "@/components/DsfrBadge"
import keyMeasures from "@/data/key-measures.json"
import { missingCanteenData, hasSatelliteInconsistency, hasStartedMeasureTunnel } from "@/utils"

export default {
  name: "KeyMeasureBadge",
  props: {
    id: String,
    diagnostic: Object,
    canteen: Object,
    year: Number,
  },
  computed: {
    isRequired() {
      return this.id === "etablissement" || this.id === "qualite-des-produits"
    },
    isCompleted() {
      return this.id === "etablissement" ? this.verifyEstablishmentCompleted() : this.verifyMeasureCompleted()
    },
    isWaitingCentralKitchen() {
      return this.isAppro && this.isSatellite && !this.isCompleted
    },
    isCentralKitchen() {
      return this.canteen?.productionType === "central" || this.canteen?.productionType === "central_serving"
    },
    missingDeclarationMode() {
      return this.isCentralKitchen && !this.diagnostic?.centralKitchenDiagnosticMode
    },
    isCentralKitchenCompleted() {
      return !this.missingDeclarationMode && !this.hasSatelliteInconsistency
    },
    missingCanteenData() {
      return !this.canteen || missingCanteenData(this.canteen, this.$store.state.sectors)
    },
    hasSatelliteInconsistency() {
      return !this.canteen || hasSatelliteInconsistency(this.canteen)
    },
    isSatellite() {
      return this.canteen?.productionType === "site_cooked_elsewhere"
    },
    isAppro() {
      return this.id === "qualite-des-produits"
    },
  },
  components: {
    DsfrBadge,
  },
  methods: {
    verifyEstablishmentCompleted() {
      return this.isCentralKitchen ? this.isCentralKitchenCompleted : !this.missingCanteenData
    },
    verifyMeasureCompleted() {
      const measure = keyMeasures.find((measure) => measure.id === this.id)
      if (this.isAppro) return hasStartedMeasureTunnel(this.diagnostic, measure) || this.hasCentralKitchenDeclared()
      else return hasStartedMeasureTunnel(this.diagnostic, measure)
    },
    hasCentralKitchenDeclared() {
      if (!this.isSatellite) return false
      const teledeclaredDiag = this.canteen.centralKitchenDiagnostics.filter((diagnostic) => {
        const isCurrentYear = diagnostic.year === this.year
        return isCurrentYear && diagnostic.isTeledeclared
      })
      return teledeclaredDiag.length > 0
    },
  },
}
</script>
