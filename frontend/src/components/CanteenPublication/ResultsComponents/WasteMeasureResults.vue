<template>
  <GenericMeasureResults :badge="badge" :canteen="canteen" :serviceDiagnostics="serviceDiagnostics" />
</template>

<script>
import GenericMeasureResults from "./GenericMeasureResults"

export default {
  name: "WasteMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    serviceDiagnostics: Array,
  },
  components: { GenericMeasureResults },
}
</script>
