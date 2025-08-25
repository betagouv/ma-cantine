<template>
  <DsfrBadge v-if="isFilled" :showIcon="false" mode="SUCCESS">
    {{ isAppro && isSatellite ? "Complété (par votre livreur)" : "Complété" }}
  </DsfrBadge>
  <DsfrBadge v-else-if="isWaitingCentralKitchen" :showIcon="false" mode="NEUTRAL">
    À compléter (par votre livreur)
  </DsfrBadge>
  <DsfrBadge v-else-if="isRequired" :showIcon="false" mode="ERROR">À compléter (obligatoire)</DsfrBadge>
  <DsfrBadge v-else :showIcon="false" mode="WARNING">À compléter (optionnel)</DsfrBadge>
</template>

<script>
import DsfrBadge from "@/components/DsfrBadge"
import keyMeasures from "@/data/key-measures.json"
import { missingCanteenData, hasSatelliteInconsistency, hasStartedMeasureTunnel, hasDiagnosticApproData } from "@/utils"

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
    isFilled() {
      if (this.id === "etablissement") return this.verifyEstablishmentFilled()
      else if (this.id === "qualite-des-produits") return this.verifyApproFilled()
      else return this.verifyMeasureFilled()
    },
    isWaitingCentralKitchen() {
      return this.isAppro && this.isSatellite && !this.isFilled
    },
    isCentralKitchen() {
      return this.canteen?.productionType === "central" || this.canteen?.productionType === "central_serving"
    },
    missingDeclarationMode() {
      return this.isCentralKitchen && !this.diagnostic?.centralKitchenDiagnosticMode
    },
    isCentralKitchenFilled() {
      return !this.missingDeclarationMode && !this.hasSatelliteInconsistency && !this.missingCanteenData
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
    verifyEstablishmentFilled() {
      return this.isCentralKitchen ? this.isCentralKitchenFilled : !this.missingCanteenData
    },
    verifyApproFilled() {
      if (this.isSatellite) return this.hasCentralKitchenDeclared()
      return hasDiagnosticApproData(this.diagnostic)
    },
    verifyMeasureFilled() {
      const measure = keyMeasures.find((measure) => measure.id === this.id)
      return hasStartedMeasureTunnel(this.diagnostic, measure)
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
