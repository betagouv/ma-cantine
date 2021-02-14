<template>
  <KeyMeasure :measure="measure"/>
</template>

<script>
  import KeyMeasure from '@/components/KeyMeasure'
  import keyMeasures from '@/data/key-measures.json'

  export default {
    components: {
      KeyMeasure,
    },
    props: {
      id: String,
    },
    data() {
      return {
        measure: keyMeasures.find(measure => measure.id === this.id),
      };
    }
  }
</script>
