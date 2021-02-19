<template>
  <div id="diagnostic-page">
    <h1>M'auto-évaluer</h1>
    <h2>Évaluez-vous sur les mesures déjà mises en place dans votre établissement, en cours ou les restes à faire.</h2>
    <div class="measure-diagnostic" v-for="measure in keyMeasures" :key="measure.id">
      <h3><KeyMeasureTitle :measure="measure"/></h3>
      <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id" class="sub-measure">
        <fieldset class="measure-headline">
          <legend>{{ subMeasure.title }}</legend>
          <button class="read-more" @click="toggleDescriptionDisplay(subMeasure)">
            {{ subMeasure.readMore ? "Moins" : "En savoir plus" }}
          </button>
          <div class="measure-status">
            <span v-for="(text, status) in STATUSES"
              :key="status"
              class="status-radio-button" :class="{selected: subMeasure.status === status}"
            >
              <input type="radio" :id="subMeasure.id + '-' + status" class="status-input"
              :name="'status-'+subMeasure.id" :value="status" v-model="subMeasure.status" @change="saveStatuses">
              <label :for="subMeasure.id + '-' + status" class="status-label">{{ text }}</label>
            </span>
          </div>
        </fieldset>
        <KeyMeasureDescription 
          v-if="subMeasure.readMore"
          class="measure-description"
          :measure="subMeasure" 
          :shrinkLogos="true"
        />
      </div>
    </div>
    <router-link :to="{ name: 'KeyMeasuresHome' }" id="summarise">Récapitulatif</router-link>
  </div>
</template>

<script>
  import { keyMeasures, saveStatuses } from "@/data/KeyMeasures.js"
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import KeyMeasureDescription from '@/components/KeyMeasureDescription';
  import STATUSES from '@/data/STATUSES.json';

  export default {
    components: {
      KeyMeasureTitle,
      KeyMeasureDescription
    },
    data() {
      return {
        keyMeasures,
        STATUSES
      };
    },
    methods: {
      toggleDescriptionDisplay(subMeasure) {
        subMeasure.readMore = !subMeasure.readMore;
      },
      saveStatuses
    }
  }
</script>

<style scoped lang="scss">
  #diagnostic-page {
    padding: 2em;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 1170px;
    margin: auto;
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

  .measure-diagnostic {
    text-align: left;
    margin-top: 1em;
    width: 90%;
  }

  .sub-measure {
    margin: 1.5em 0;
  }

  fieldset {
    margin-inline-start: 0;
    margin-inline-end: 0;
    padding-block-start: 0;
    padding-block-end: 0;
    padding-inline-start: 0;
    padding-inline-end: 0;
    border: none;
    min-inline-size: min-content;
  }

  .measure-headline {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  legend {
    width: 60%;
    font-weight: normal;
    float: left;
  }

  .read-more {
    border: none;
    background-color: $white;
    width: 15%;
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
    min-width: 11em;
    max-width: 14.5em;
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

  #summarise {
    color: $white;
    font-size: 24px;
    background-color: $orange;
    width: 10em;
    padding: 0.2em;
    border-radius: 1em;
    border: none;
    margin-top: 2em;
    cursor: pointer;
    text-decoration: none;
  }

  @media (max-width: 1000px) {
    .status-label {
      padding: 1em 0.3em;
    }
  }

  @media (max-width: 700px) {
    .measure-headline {
      flex-direction: column;
      align-items: flex-start;
    }

    legend {
      width: 100%;
      margin-bottom: 0;
    }

    .read-more {
      margin-left: 0;
      padding: 0;
      height: 3em;
      width: 10em;
    }

    .measure-status {
      margin: 0.5em 0;
    }

    .measure-description {
      width: 100%;
    }

    .status-label {
      padding: 1em;
    }
  }
</style>