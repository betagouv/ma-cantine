<template>
  <div id="diagnostic-page">
    <h1>M'auto-évaluer</h1>
    <h2>Évaluez-vous sur les mesures déjà mises en place dans votre établissement, programmées ou celles restantes à faire.</h2>
    <div class="measure-diagnostic" v-for="measure in keyMeasures" :key="measure.id">
      <h3><KeyMeasureTitle :measure="measure"/></h3>
      <div v-for="subMeasure in measure.subMeasures" :key="subMeasure.id" class="sub-measure">
        <fieldset class="measure-headline">
          <legend>{{ subMeasure.title }}</legend>
          <button class="read-more" @click="toggleDescriptionDisplay(subMeasure)">
            {{ subMeasure.readMore ? "Moins" : "En savoir plus" }}
          </button>
          <KeyMeasureStatusOption :initialMeasure="subMeasure" />
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
  import { keyMeasures } from "@/data/KeyMeasures.js"
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import KeyMeasureDescription from '@/components/KeyMeasureDescription';
  import KeyMeasureStatusOption from '@/components/KeyMeasureStatusOption';

  export default {
    components: {
      KeyMeasureTitle,
      KeyMeasureDescription,
      KeyMeasureStatusOption
    },
    data() {
      return {
        keyMeasures
      };
    },
    methods: {
      toggleDescriptionDisplay(subMeasure) {
        subMeasure.readMore = !subMeasure.readMore;
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

    .measure-description {
      width: 100%;
    }
  }
</style>
