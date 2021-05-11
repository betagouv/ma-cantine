<template>
  <div>
    <h2 id="modal-title" tabindex="-1"><KeyMeasureTitle :measure="measure"/></h2>

    <form id="diagnostic-form" @submit.prevent="submit">
      <component
        :is="measureDiagnosticComponentName"
        v-model="diagnostics"
      />

      <input type="submit" id="submit" value="Valider">
    </form>
  </div>
</template>

<script>
  import KeyMeasureTitle from '@/components/KeyMeasureTitle';
  import DiversificationMeasureDiagnostic from '@/components/KeyMeasureDiagnostic/DiversificationMeasure';
  import InformationMeasureDiagnostic from '@/components/KeyMeasureDiagnostic/InformationMeasure';
  import NoPlasticMeasureDiagnostic from '@/components/KeyMeasureDiagnostic/NoPlasticMeasure';
  import QualityMeasureDiagnostic from '@/components/KeyMeasureDiagnostic/QualityMeasure';
  import WasteMeasureDiagnostic from '@/components/KeyMeasureDiagnostic/WasteMeasure';
  import { saveDiagnostics, saveDiagnostic } from "@/data/KeyMeasures.js";

  export default {
    components: {
      KeyMeasureTitle,
      DiversificationMeasureDiagnostic,
      InformationMeasureDiagnostic,
      NoPlasticMeasureDiagnostic,
      QualityMeasureDiagnostic,
      WasteMeasureDiagnostic
    },
    props: ['measure', 'closeModal', 'originalDiagnostics'],
    data() {
      return {
        measureDiagnosticComponentName: this.measure.baseComponent + "Diagnostic",
      };
    },
    methods: {
      async submit() {
        (this.measureDiagnosticComponentName === 'QualityMeasureDiagnostic') ?
          await saveDiagnostics(this.diagnostics) :
          await saveDiagnostic(this.diagnostics);
        this.$emit('closeModal');
      },
    },
    computed: {
      diagnostics() {
        return (this.measureDiagnosticComponentName === 'QualityMeasureDiagnostic') ?
          this.originalDiagnostics :
          this.originalDiagnostics[0];
      }
    }
  }
</script>

<style scoped lang="scss">
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
</style>
