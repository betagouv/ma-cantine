<template>
  <div id="key-measures">
    <h1>Les 5 mesures phares de la loi EGAlim</h1>
    <div id="measures" v-for="measure in keyMeasures" :key="measure.id">
      <KeyMeasure :measure="measure"/>
    </div>
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
  #key-measures {
    text-align: center;
    padding: 1em 1em;

    h1 {
      font-weight: bold;
      font-size: 48px;
      color: $green;
      margin: 1em 0em;
    }

    #measures {
      text-align: left;
      display: flex;
      overflow: hidden;
      align-items: center;
      max-width: 1170px;
      margin: auto;
    }
  }

  @media (max-width: 480px) {
    #key-measures {
      text-align: center;
      padding: 1em 0.5em;
    }
  }
</style>
