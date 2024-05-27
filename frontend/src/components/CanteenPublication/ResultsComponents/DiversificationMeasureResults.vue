<template>
  <GenericMeasureResults :badge="badge" :canteen="canteen" :serviceDiagnostics="serviceDiagnostics" />
</template>

<script>
import GenericMeasureResults from "./GenericMeasureResults"

export default {
  name: "DiversificationMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    serviceDiagnostics: Array,
  },
  components: { GenericMeasureResults },
}
</script>
