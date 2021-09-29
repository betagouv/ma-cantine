<template>
  <div id="quality-measure" class="text-left">
    <p class="text-center help">Si vous ne connaissez pas une valeur, laissez le champ vide.</p>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="5" class="my-8">
        <QualityMeasureValuesInput
          :originalDiagnostic="previousDiagnostic"
          :label="`En ${previousDiagnostic.year}, la valeur (en HT) de mes achats alimentaires...`"
        />
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="5" class="my-8">
        <QualityMeasureValuesInput
          :originalDiagnostic="latestDiagnostic"
          :label="`En ${latestDiagnostic.year}, la valeur (en HT) de mes achats alimentaires...`"
        />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <p class="text-center help mx-4">
      Indiquez ci-après les montants estimés de produits durables et de qualité sur la base des actions mises en œuvre
      ou prévues.
      <br />
      (ex : renouvellement de marchés, modification de contrats d’approvisionnements, rationalisation des consommations
      évolution des grammages, etc.)
    </p>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="5" class="my-8">
        <QualityMeasureValuesInput
          :originalDiagnostic="provisionalYear1Diagnostic"
          :label="
            `En ${provisionalYear1Diagnostic.year}, la valeur prévisionnelle (en HT) de mes achats alimentaires...`
          "
        />
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="5" class="my-8">
        <QualityMeasureValuesInput
          :originalDiagnostic="provisionalYear2Diagnostic"
          :label="
            `En ${provisionalYear2Diagnostic.year}, la valeur prévisionnelle (en HT) de mes achats alimentaires...`
          "
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
      provisionalYear1Diagnostic: this.diagnostics.provisionalYear1,
      provisionalYear2Diagnostic: this.diagnostics.provisionalYear2,
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
