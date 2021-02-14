<template>
  <h1>Les 5 mesures phares de la loi EGAlim</h1>
  <div id="measures" v-for="measure in keyMeasures" :key="measure.id">
    <KeyMeasure :measure="measure"/>
  </div>
</template>

<script>
  import KeyMeasure from '@/components/KeyMeasure'
  import keyMeasures from '@/data/key-measures.json'

  export default {
    components: {
      KeyMeasure,
    },
    data() {
      return {
        keyMeasures,
      };
    }
  }
</script>

<style scoped lang="scss">
  h1 {
    font-weight: bold;
    font-size: 48px;
    color: $green;
    margin: 1em 0em;
  }

  #measures {
    display: flex;
  }
</style>
