<template>
  <div id="advanced-diagnostic-modal" @click.self="$emit('closeModal')" role="dialog" aria-labelledby="measure-title">
    <div id="advanced-diagnostic-content">
      <button class="close" @click="$emit('closeModal')" aria-label="Fermer" title="Fermer"><i class="fas fa-times"></i></button>
      <h2 id="measure-title" tabindex="-1"><KeyMeasureTitle :measure="measure"/></h2>

      <form id="diagnostic-form" @submit.prevent="submit">
        <component
          :is="measureDiagnosticComponentName"
          v-model="diagnostic"
        />

        <input type="submit" id="submit" value="Valider">
      </form>
    </div>
  </div>
</template>

<script>
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import DiversificationMeasureDiagnostic from '@/components/KeyMeasureDiagnostic/DiversificationMeasure';
  import InformationMeasureDiagnostic from '@/components/KeyMeasureDiagnostic/InformationMeasure';
  import NoPlasticMeasureDiagnostic from '@/components/KeyMeasureDiagnostic/NoPlasticMeasure';
  import QualityMeasureDiagnostic from '@/components/KeyMeasureDiagnostic/QualityMeasure';
  import WasteMeasureDiagnostic from '@/components/KeyMeasureDiagnostic/WasteMeasure';
  import { diagnostics, saveDiagnostic } from "@/data/KeyMeasures.js";

  export default {
    components: {
      KeyMeasureTitle,
      DiversificationMeasureDiagnostic,
      InformationMeasureDiagnostic,
      NoPlasticMeasureDiagnostic,
      QualityMeasureDiagnostic,
      WasteMeasureDiagnostic
    },
    props: {
      measure: Object,
    },
    data() {
      return {
        diagnostic: diagnostics[this.measure.id] || {},
        measureDiagnosticComponentName: this.measure.baseComponent + "Diagnostic",
      };
    },
    methods: {
      submit() {
        saveDiagnostic(this.measure.id, this.diagnostic);
        this.$emit('closeModal');
      },
    },
  }
</script>

<style scoped lang="scss">
  #advanced-diagnostic-modal {
    position: fixed;
    z-index: 1;
    padding-top: 150px;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
  }

  #advanced-diagnostic-content {
    margin: auto;
    padding: 50px;
    width: 45%;
    border-radius: 2em;
    background-color: $dark-white;
    overflow-y: auto;
    max-height: calc(100vh - 300px);
  }

  .close {
    float: right;
    cursor: pointer;
    border: none;
    background-color: transparent;

    .fa-times {
      width: 25px;
      height: 25px;
      color: $grey;
    }
  }

  .close:hover {
    .fa-times:hover {
      color: $light-grey;
    }
  }

  #diagnostic-form {
    margin-top: 30px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    min-height: 500px;

    #submit {
      color: $white;
      font-size: 24px;
      background-color: $orange;
      width: 10em;
      padding: 0.2em;
      border-radius: 1em;
      cursor: pointer;
      margin-left: auto;
      text-align: center;
      border: none;
      margin-top: 10px;
      margin-bottom: 10px;
    }
  }

  @media (max-width: 750px) {
    #advanced-diagnostic-modal {
      z-index: 2000;
      padding-top: 20px;
    }

    #advanced-diagnostic-content {
      width: 70%;
      max-height: calc(100vh - 150px);
    }
  }
</style>
