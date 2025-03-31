<template>
  <DsfrBadge v-if="isCompleted" :showIcon="false" mode="SUCCESS">Complété</DsfrBadge>
  <DsfrBadge v-else-if="isRequired" :showIcon="false" mode="ERROR">À compléter (obligatoire)</DsfrBadge>
  <DsfrBadge v-else :showIcon="false" mode="WARNING">À compléter (optionnel)</DsfrBadge>
</template>

<script>
import DsfrBadge from "@/components/DsfrBadge"
import keyMeasures from "@/data/key-measures.json"
import { missingCanteenData, hasSatelliteInconsistency, hasStartedMeasureTunnel } from "@/utils"

// TODO =
// 1 état rouge bloque la TD : à compléter
// 1 état jaune : à compléter (optionnel)
// 1 état gris / appro + SAT seulement :  à compléter (par livreur des repas)
// 2 états vert : complété solo || TD par livreur des repas

export default {
  name: "KeyMeasureBadge",
  props: {
    name: String,
    diagnostic: Object,
    canteen: Object,
    year: String,
  },
  computed: {
    isRequired() {
      return this.name === "etablissement" || this.name === "qualite-des-produits"
    },
    isCompleted() {
      return this.name === "etablissement" ? this.verifyEstablishmentCompleted() : this.verifyMeasureCompleted()
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
  },
  components: {
    DsfrBadge,
  },
  methods: {
    verifyEstablishmentCompleted() {
      return this.isCentralKitchen ? this.isCentralKitchenCompleted : !this.missingCanteenData
    },
    verifyMeasureCompleted() {
      const measure = keyMeasures.find((measure) => measure.id === this.name)
      const isAppro = this.name === "qualite-des-produits"
      if (isAppro) return hasStartedMeasureTunnel(this.diagnostic, measure) || this.hasCentralKitchenDeclared()
      else return hasStartedMeasureTunnel(this.diagnostic, measure)
    },
    hasCentralKitchenDeclared() {
      if (!this.isSatellite) return false
      const teledeclaredDiag = this.canteen.centralKitchenDiagnostics.filter((diagnostic) => {
        const isCurrentYear = diagnostic.year == this.year
        return isCurrentYear && diagnostic.isTeledeclared
      })
      return teledeclaredDiag.length > 0
    },
  },
}
</script>
