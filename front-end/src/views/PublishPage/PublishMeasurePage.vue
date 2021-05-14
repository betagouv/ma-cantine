<template>
  <div v-if="diagnostics">
    <KeyMeasureDiagnostic
      :measure="measure"
      :originalDiagnostics="diagnostics"
      @afterSave="goToNextStep"
    />
  </div>
</template>

<script>
  import keyMeasures from '@/data/key-measures.json';
  import KeyMeasureDiagnostic from '@/components/KeyMeasureDiagnostic';

  export default {
    components: {
      KeyMeasureDiagnostic
    },
    props: ['routeProps', 'id'],
    data() {
      return {
        measure: keyMeasures.find(measure => measure.id === this.id),
      };
    },
    computed: {
      diagnostics() {
        return this.routeProps;
      },
    },
    created() {
      document.title = `${this.measure.title} - Publication`;
    },
    methods: {
      goToNextStep() {
        const currentMeasureIndex = keyMeasures.findIndex(measure => measure.id === this.id);

        if (currentMeasureIndex === 4) {
          return this.$router.push({ name: 'SubmitPublicationPage' });
        }

        const nextMeasureId = keyMeasures[currentMeasureIndex + 1].id;

        return this.$router.push({ name: 'PublishMeasurePage', params: { id: nextMeasureId } });
      },
    }
  }
</script>
