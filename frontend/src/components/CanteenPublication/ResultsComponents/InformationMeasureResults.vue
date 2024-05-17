<template>
  <div>
    <GenericMeasureResults :badge="badge" :canteen="canteen" :serviceDiagnostics="serviceDiagnostics" />
    <p v-if="diagnostic && diagnostic.communicationSupportUrl" class="fr-text">
      Cette cantine communique aux usagers sur
      <a :href="diagnostic.communicationSupportUrl">{{ diagnostic.communicationSupportUrl }}</a>
    </p>
  </div>
</template>

<script>
import GenericMeasureResults from "./GenericMeasureResults"
import { latestCreatedDiagnostic } from "@/utils"

export default {
  name: "InformationMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    serviceDiagnostics: Array,
  },
  components: { GenericMeasureResults },
  computed: {
    diagnostic() {
      if (!this.serviceDiagnostics) return
      return latestCreatedDiagnostic(this.serviceDiagnostics)
    },
  },
}
</script>
