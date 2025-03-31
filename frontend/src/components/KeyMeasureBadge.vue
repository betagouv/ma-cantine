<template>
  <DsfrBadge v-if="isCompleted" :showIcon="false" mode="SUCCESS">Complété</DsfrBadge>
  <DsfrBadge v-else-if="isRequired" :showIcon="false" mode="ERROR">À compléter (obligatoire)</DsfrBadge>
  <DsfrBadge v-else :showIcon="false" mode="WARNING">À compléter (optionnel)</DsfrBadge>
</template>

<script>
import DsfrBadge from "@/components/DsfrBadge"
import keyMeasures from "@/data/key-measures.json"
import { hasStartedMeasureTunnel } from "@/utils"

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
  },
  computed: {
    isRequired() {
      return this.name === "etablissement" || this.name === "qualite-des-produits"
    },
    isCompleted() {
      if (this.name === "etablissement") return "TODO"
      const measure = keyMeasures.find((measure) => measure.id === this.name)
      return hasStartedMeasureTunnel(this.diagnostic, measure)
    },
  },
  components: {
    DsfrBadge,
  },
  methods: {
    hasCentralKitchenDeclared(measure) {
      if (measure.badgeId !== "appro") return false
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
