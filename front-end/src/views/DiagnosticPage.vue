<template>
  <div id="diagnostic-page">
    <h1>M'auto-évaluer</h1>
    <h2>Évaluez-vous sur les mesures déjà mises en place dans votre établissement, en cours ou les restes à faire.</h2>
    <div id="diagnostic" v-for="measure in keyMeasures" :key="measure.id">
      <h3><KeyMeasureTitle :measure="measure"/></h3>
      <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id">
        <div class="measure-headline">
          <h4>{{ subMeasure.title }}</h4>
          <button class="read-more" @click="toggleDescriptionDisplay(subMeasure.id)">
            {{ readMore[subMeasure.id] ? "Moins" : "En savoir plus" }}
          </button>
          <div class="measure-status">
            <span v-for="(text, status) in STATUSES"
              :key="status"
              class="status-radio-button" :class="{selected: statuses[subMeasure.id] === status}"
            >
              <input type="radio" :id="subMeasure.id + '-' + status" class="status-input"
              :name="'status-'+subMeasure.id" :value="status" v-model="statuses[subMeasure.id]">
              <label :for="subMeasure.id + '-' + status" class="status-label">{{ text }}</label>
            </span>
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
  </div>
</template>

<script>
  import keyMeasures from "@/data/key-measures.json"
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import KeyMeasureDescription from '@/components/KeyMeasureDescription';

  const STATUSES = {
    done: 'Fait',
    planned: 'Programmé',
    notDone: 'Pas fait'
  };

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
        readMore,
        STATUSES,
        statuses: {}
      };
    },
    methods: {
      toggleDescriptionDisplay(id) {
        this.readMore[id] = !this.readMore[id]
      }
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
    justify-content: space-between;
  }

  h4 {
    width: 60%;
    font-weight: normal;
  }

  .read-more {
    border: none;
    background-color: $white;
    max-width: 10em;
    padding: 1em 0;
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

  .status-label {
    border: none;
    margin: 0;
    padding: 1em;
    white-space: nowrap;
    font-size: 14px;
    cursor: pointer;
    position: relative;
    top: 0.4em;
  }

  .status-input {
    opacity: 0;
    position: absolute;
  }

  .status-radio-button.selected, .status-radio-button:hover {
    background-color: $light-yellow;
  }

  .measure-description {
    width: 70%;
    padding-left: 1em;
    border-left: 1px $green solid;
  }

  @media (max-width: 1200px) {
    .measure-status {
      min-width: 11em;
    }

    .status {
      padding: 0 0.4em;
    }
  }

  @media (max-width: 700px) {
    .measure-headline {
      flex-direction: column;
      align-items: flex-start;
    }

    h4 {
      width: 100%;
      margin-bottom: 0;
    }

    .read-more {
      margin-left: 0;
      padding: 0;
      height: 3em;
    }

    .measure-status {
      margin: 0.5em 0;
    }

    .measure-description {
      width: 100%;
    }
  }
</style>