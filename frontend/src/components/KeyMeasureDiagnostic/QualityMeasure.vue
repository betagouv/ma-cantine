<template>
  <div id="quality-measure" class="text-left">
    <v-row>
      <v-spacer></v-spacer>
      <QualityMeasureValuesInput
        :originalDiagnostic="previousDiagnostic"
        label="En 2019, la valeur (en HT) de mes achats alimentaires..."
      />
      <v-spacer></v-spacer>
      <QualityMeasureValuesInput
        :originalDiagnostic="latestDiagnostic"
        label="En 2020, la valeur (en HT) de mes achats alimentaires..."
      />
      <v-spacer></v-spacer>
    </v-row>
    <v-row>
      <v-spacer></v-spacer>
      <QualityMeasureValuesInput
        :originalDiagnostic="provisionalYear1Diagnostic"
        label="En 2021, la valeur prévisionnelle (en HT) de mes achats alimentaires..."
      />
      <v-spacer></v-spacer>
      <QualityMeasureValuesInput
        :originalDiagnostic="provisionalYear2Diagnostic"
        label="En 2022, la valeur prévisionnelle (en HT) de mes achats alimentaires..."
      />
      <v-spacer></v-spacer>
    </v-row>
  </div>
</template>

<script>
import QualityMeasureValuesInput from "./QualityMeasureValuesInput"

export default {
  props: {
    diagnostics: Object,
  },
  components: {
    QualityMeasureValuesInput,
  },
  data() {
    return {
      latestDiagnostic: this.diagnostics.latest,
      previousDiagnostic: this.diagnostics.previous,
      provisionalYear1Diagnostic: this.diagnostics.provisionalYear1,
      provisionalYear2Diagnostic: this.diagnostics.provisionalYear2,
    }
  },
}
</script>
