<template>
  <GenericMeasureResults :badge="badge" :canteen="canteen" />
</template>

<script>
import GenericMeasureResults from "./GenericMeasureResults"

export default {
  name: "DiversificationMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    diagnostics: Array,
    editable: Boolean,
  },
  components: { GenericMeasureResults },
}
</script>
