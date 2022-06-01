<template>
  <KeyMeasure :measure="measure" />
</template>

<script>
import KeyMeasure from "@/components/KeyMeasure"
import keyMeasures from "@/data/key-measures.json"

export default {
  components: {
    KeyMeasure,
  },
  props: {
    id: String,
  },
  data() {
    return {
      measure: keyMeasures.find((measure) => measure.id === this.id),
    }
  },
  created() {
    // simpler to specify the title here than in vue router meta data
    // due to the title being a function of the id parameter
    document.title = `${this.measure.title} - ma cantine`
  },
}
</script>
