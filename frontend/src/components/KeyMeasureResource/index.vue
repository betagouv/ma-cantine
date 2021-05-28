<template>
  <component :is="baseComponent" />
</template>

<script>
import DiversificationMeasure from "./DiversificationMeasure"
import InformDiners from "./InformDiners"
import QualityMeasure from "./QualityMeasure"
import WasteMeasure from "./WasteMeasure"

export default {
  props: {
    baseComponent: String,
  },
  components: {
    DiversificationMeasure,
    InformDiners,
    QualityMeasure,
    WasteMeasure,
  },
}
</script>
