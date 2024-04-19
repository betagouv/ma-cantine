<template>
  <GenericMeasureResults :badge="badge" :canteen="canteen" :diagnosticSet="diagnosticSet" />
</template>

<script>
import GenericMeasureResults from "./GenericMeasureResults"

export default {
  name: "DiversificationMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    diagnosticSet: Array,
  },
  components: { GenericMeasureResults },
}
</script>
