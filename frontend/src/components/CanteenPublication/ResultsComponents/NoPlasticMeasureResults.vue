<template>
  <GenericMeasureResults :badge="badge" />
</template>

<script>
import GenericMeasureResults from "./GenericMeasureResults"

export default {
  name: "NoPlasticMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
    diagnosticSet: Array,
  },
  components: { GenericMeasureResults },
}
</script>
