<template>
  <GenericMeasureResults :badge="badge" :canteen="canteen" />
</template>

<script>
import GenericMeasureResults from "./GenericMeasureResults"

export default {
  name: "NoPlasticMeasureResults",
  props: {
    badge: Object,
    canteen: Object,
  },
  components: { GenericMeasureResults },
}
</script>
