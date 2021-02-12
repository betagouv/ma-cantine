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
        <!-- TODO: refactor description handling to a reusable component -->
        <p>{{ subMeasure.description || subMeasure.htmlDescription }}</p>
      </div>
    </div>
    <button id="summarise">Récapitulatif</button>
  </div>
</template>

<script>
  import keyMeasures from "@/data/key-measures.json"
  import KeyMeasureTitle from '../components/KeyMeasureTitle';

  export default {
  components: { KeyMeasureTitle },
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