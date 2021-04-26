<template>
  <div id="diagnostic-page">
    <h1>M'auto-évaluer</h1>
    <h2>Évaluez-vous sur les mesures déjà mises en place dans votre établissement, programmées ou celles restantes à faire.</h2>
    <div class="sector">
      <label for="sectors">Secteur de mon restaurant : </label>
      <select id="sectors" v-model="sector">
        <option v-for="(label, key) in sectors" :key="key" :value="key">
          {{label}}
        </option>
      </select>
    </div>
    <div class="measure-diagnostic" v-for="measure in sectorMeasures" :key="measure.id">
      <div class="measure-title">
        <h3><KeyMeasureTitle :measure="measure"/></h3>
        <button @click="showDiagnosticModal(measure)">Je m'évalue !</button>
      </div>
      <div v-for="subMeasure in getFilteredSubMeasures(measure)" :key="subMeasure.id" class="sub-measure">
        <fieldset class="measure-headline">
          <!-- Wrap legend in span to correctly position with flexbox in Safari -->
          <span><legend>{{ subMeasure.title }}</legend></span>
          <button class="read-more" @click="toggleDescriptionDisplay(subMeasure)">
            {{ subMeasure.readMore ? "Moins" : "En savoir plus" }}
          </button>
        </fieldset>
        <KeyMeasureDescription
          v-if="subMeasure.readMore"
          class="measure-description"
          :measure="subMeasure"
        />
      </div>
    </div>
    <BaseModal v-if="measureDiagnosticModal" @closeModal="closeDiagnosticModal">
      <KeyMeasureDiagnostic
        :measure="measureDiagnosticModal"
        @closeModal="closeDiagnosticModal"
      />
    </BaseModal>
    <router-link :to="{ name: 'KeyMeasuresHome' }" id="summarise">
      Récapitulatif
    </router-link>
  </div>
</template>

<script>
  import { keyMeasures } from "@/data/KeyMeasures.js"
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import KeyMeasureDescription from '@/components/KeyMeasureDescription';
  import KeyMeasureDiagnostic from '@/components/KeyMeasureDiagnostic';
  import BaseModal from '@/components/BaseModal';
  import sectors from "@/data/sectors.json";

  export default {
    components: {
      KeyMeasureTitle,
      KeyMeasureDescription,
      KeyMeasureDiagnostic,
      BaseModal
    },
    data() {
      return {
        sectors,
        measureDiagnosticModal: null,
        sector: "scolaire",
      };
    },
    computed: {
      sectorMeasures() {
        return keyMeasures.filter(keyMeasure => keyMeasure.sectors.includes(this.sector));
      },
    },
    methods: {
      toggleDescriptionDisplay(subMeasure) {
        subMeasure.readMore = !subMeasure.readMore;
      },
      showDiagnosticModal(measure) {
        this.measureDiagnosticModal = measure;
      },
      closeDiagnosticModal() {
        this.measureDiagnosticModal = null;
      },
      getFilteredSubMeasures(measure) {
        return measure.specificSectorsForSubMeasures ?
          measure.subMeasures.filter(subMeasure => subMeasure.sectors.includes(this.sector)) :
          measure.subMeasures;
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

  .sector {
    text-align: left;
    width: 90%;
    font-size: 24px;
    margin-top: 1em;

    select {
      font-size: 20px;
      padding: 5px;
      border: none;
      background-color: white;
      border-radius: 5px;
      box-shadow: 0 0 5px $light-grey;
    }
  }

  .measure-diagnostic {
    text-align: left;
    margin-top: 2em;
    width: 90%;
  }

  .measure-title {
    display: flex;
    justify-content: space-between;

    button {
      background-color: $white;
      font-size: 1em;
      margin: auto 0;
      color: $dark-orange;
      border: 1px solid $dark-orange;
      border-radius: 20px;
      width: 130px;
      text-align: center;
      padding: 5px;
      cursor: pointer;
    }
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

    span {
      width: 60%;
      font-weight: normal;
    }
  }

  .read-more {
    border: none;
    background-color: $white;
    width: 15%;
    padding: 1em 0;
    margin: 0 0.5em;
    text-align: right;
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
    .measure-title {
      flex-direction: column;
    }

    .measure-headline {
      flex-direction: column;
      align-items: flex-start;

      span {
        width: 100%;
        margin-bottom: 0;
      }
    }

    .read-more {
      margin-left: 0;
      padding: 0;
      height: 3em;
      width: 10em;
      text-align: left;
    }

    .measure-description {
      width: 100%;
    }
  }
</style>
