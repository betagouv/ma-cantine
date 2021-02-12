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
            <button
              class="status"
              :class="{selected: statuses[subMeasure.id] === STATUSES.done}"
              @click="statuses[subMeasure.id] = STATUSES.done"
            >
              Fait
            </button>
            <button
              class="status"
              :class="{selected: statuses[subMeasure.id] === STATUSES.planned}"
              @click="statuses[subMeasure.id] = STATUSES.planned"
            >
              Programmé
            </button>
            <button
              class="status"
              :class="{selected: statuses[subMeasure.id] === STATUSES.notDone}"
              @click="statuses[subMeasure.id] = STATUSES.notDone"
            >
              Pas fait
            </button>
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
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import KeyMeasureDescription from '@/components/KeyMeasureDescription';

  const STATUSES = {
    done: 'done',
    planned: 'planned',
    notDone: 'not done'
  };

  export default {
    components: {
      KeyMeasureTitle,
      KeyMeasureDescription
    },
    data() {
      let readMore = {}, statuses = {};
      Object.keys(keyMeasures).forEach(key => readMore[key] = false);
      Object.keys(keyMeasures).forEach(key => statuses[key] = undefined);
      return {
        keyMeasures,
        readMore,
        STATUSES,
        statuses
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
    align-items: center;
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

  .measure-status {
    border-radius: 1em;
    overflow: hidden;
    /* offset-x | offset-y | blur-radius | spread-radius | color */
    box-shadow: 0px 0px 5px 1px $dark-white;
    height: 2.5em;
    display: flex;
  }

  .status {
    border: none;
    margin: 0;
    background-color: $white;
    font-size: 14px;
    cursor: pointer;
  }

  .status.selected, .status:hover {
    background-color: $light-yellow;
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