<template>
  <div id="diagnostic-page">
    <h1>M'auto-évaluer</h1>
    <h2>Évaluez-vous sur les mesures déjà mises en place dans votre établissement, en cours ou les restes à faire.</h2>
    <div id="diagnostic" v-for="measure in keyMeasures" :key="measure.id">
      <h3><KeyMeasureTitle :measure="measure"/></h3>
      <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id">
        <div class="measure-headline">
          <h4>{{ subMeasure.title }}</h4>
          <button class="read-more" @click="readMore[subMeasure.id] = !readMore[subMeasure.id]">
            {{ readMore[subMeasure.id] ? "Moins" : "En savoir plus" }}
          </button>
          <div class="measure-status">
            <button class="status">Fait</button>
            <button class="status">Programmé</button>
            <button class="status">Pas fait</button>
          </div>
        </div>
        <KeyMeasureDescription 
          v-if="readMore[subMeasure.id]"
          class="measure-description"
          :measure="subMeasure" 
          :shrinkLogos="true"
        />
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
      let readMore = {};
      Object.keys(keyMeasures).forEach(key => readMore[key] = false);
      return {
        keyMeasures,
        readMore
      };
    }
  }
</script>

<style scoped lang="scss">
  #diagnostic-page {
    padding: 2em;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  h1 {
    font-size: 48px;
    color: $green;
    margin: 1em 0em;
  }

  h2 {
    color: $light-grey;
    width: 80%;
    font-weight: normal;
  }

  #diagnostic {
    text-align: left;
    margin-top: 3em;
    width: 90%;
  }

  .measure-headline {
    display: flex;
  }

  h4 {
    width: 60%;
    font-weight: normal;
  }

  .read-more {
    border: none;
    background-color: $white;
    width: 10em;
    margin-left: 0.5em;
    text-align: left;
    font-size: 14px;
    color: $black;
    cursor: pointer;
  }

  .measure-description {
    width: 70%;
    padding-left: 1em;
    border-left: 1px $green solid;
  }

  @media (max-width: 700px) {
    .measure-headline {
      flex-direction: column;
    }

    h4 {
      width: 100%;
      margin: 0;
    }

    .read-more {
      margin-left: 0;
      padding: 0;
      height: 3em;
    }
  }
</style>