<template>
  <div id="quality-measure" class="text-left">
    <p class="text-center help">Si vous ne connaissez pas une valeur, laissez le champ vide.</p>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="5" class="my-8">
        <QualityMeasureValuesInput
          :originalDiagnostic="previousDiagnostic"
          :label="`En ${previousDiagnostic.year}, la valeur (en € HT) de mes achats alimentaires...`"
        />
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="5" class="my-8">
        <QualityMeasureValuesInput
          :originalDiagnostic="latestDiagnostic"
          :label="`En ${latestDiagnostic.year}, la valeur (en € HT) de mes achats alimentaires...`"
        />
      </v-col>
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
    }
  },
}
</script>

<style scoped lang="scss">
p.help {
  color: $ma-cantine-grey;
  font-size: 0.95em;
}
</style>
