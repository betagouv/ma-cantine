<template>
  <div>
    <GenericMeasureResults :badge="badge" :canteen="canteen" :diagnostics="diagnostics" />
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
    diagnostics: Array,
    editable: Boolean,
  },
  components: { GenericMeasureResults },
  computed: {
    diagnostic() {
      if (!this.diagnostics) return
      return latestCreatedDiagnostic(this.diagnostics)
    },
  },
}
</script>
