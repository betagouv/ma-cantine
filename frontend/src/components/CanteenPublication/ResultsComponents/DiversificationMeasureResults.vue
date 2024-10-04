<template>
  <GenericMeasureResults :badge="badge" :canteen="canteen" :diagnostics="diagnostics" />
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
