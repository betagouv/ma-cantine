<template>
  <div id="diagnostic-page">
    <h1>M'auto-évaluer</h1>
    <div id="diagnostic" v-for="measure in keyMeasures" :key="measure.id">
      <h2><KeyMeasureTitle :measure="measure"/></h2>
      <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id">
        <div class="measure-headline">
          <h3>{{ subMeasure.title }}</h3>
          <button class="about">En savoir plus</button>
          <div class="measure-status">
            <button class="status">Fait</button>
            <button class="status">Programmé</button>
            <button class="status">Pas fait</button>
          </div>
        </div>
        <KeyMeasureDescription :measure="subMeasure" />
      </div>
    </div>
    <button id="summarise">Récapitulatif</button>
  </div>
</template>

<script>
  import keyMeasures from "@/data/key-measures.json"
  import KeyMeasureTitle from '../components/KeyMeasureTitle';
  import KeyMeasureDescription from '../components/KeyMeasureDescription';

  export default {
    components: {
      KeyMeasureTitle,
      KeyMeasureDescription
    },
    data() {
      return {
        keyMeasures
      };
    }
  }
</script>

<style scoped>
  #diagnostic {
    text-align: left;
  }

  .measure-headline {
    display: flex;
  }

  h3 {
    flex-grow: 2;
  }
</style>