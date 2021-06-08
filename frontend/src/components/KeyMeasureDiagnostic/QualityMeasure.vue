<template>
  <div id="quality-measure" class="text-left">
    <p class="text-center"><em>Si vous ne savez pas quelques valeurs, vous pouvez laisser le champ vide.</em></p>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="5" class="my-8">
        <div class="d-flex flex-column">
          <!-- TODO: Use text field suffix (euros HT) instead of (en HT) here? -->
          <!-- TODO: Use text field labels instead of separate p tags? -->
          <p>En 2019, la valeur (en HT) de mes achats alimentaires...</p>

          <p class="body-2 mb-1 mt-2">...totale</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="previousDiagnostic.valueTotalHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en produits bio</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="previousDiagnostic.valueBioHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en autres produits de qualité et durables (hors bio)</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="previousDiagnostic.valueSustainableHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en produits issus du commerce équitable</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="previousDiagnostic.valueFairTradeHt"
          ></v-text-field>
        </div>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="5" class="my-8">
        <div class="d-flex flex-column">
          <p>En 2020, la valeur (en HT) de mes achats alimentaires...</p>

          <p class="body-2 mb-1 mt-2">...totale</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="latestDiagnostic.valueTotalHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en produits bio</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="latestDiagnostic.valueBioHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en autres produits de qualité et durables (hors bio)</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="latestDiagnostic.valueSustainableHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en produits issus du commerce équitable</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="latestDiagnostic.valueFairTradeHt"
          ></v-text-field>
        </div>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="5" class="my-8">
        <div class="d-flex flex-column">
          <p>En 2021, la valeur prévisionnelle (en HT) de mes achats alimentaires...</p>

          <p class="body-2 mb-1 mt-2">...totale</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="provisionalYear1Diagnostic.valueTotalHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en produits bio</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="provisionalYear1Diagnostic.valueBioHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en autres produits de qualité et durables (hors bio)</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="provisionalYear1Diagnostic.valueSustainableHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en produits issus du commerce équitable</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="provisionalYear1Diagnostic.valueFairTradeHt"
          ></v-text-field>
        </div>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="12" sm="5" class="my-8">
        <div class="d-flex flex-column">
          <p>En 2022, la valeur prévisionnelle (en HT) de mes achats alimentaires...</p>

          <p class="body-2 mb-1 mt-2">...totale</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="provisionalYear2Diagnostic.valueTotalHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en produits bio</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="provisionalYear2Diagnostic.valueBioHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en autres produits de qualité et durables (hors bio)</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="provisionalYear2Diagnostic.valueSustainableHt"
          ></v-text-field>

          <p class="body-2 mb-1 mt-4">...en produits issus du commerce équitable</p>
          <v-text-field
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty]"
            solo
            v-model="provisionalYear2Diagnostic.valueFairTradeHt"
          ></v-text-field>
        </div>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  props: {
    diagnostics: Object,
  },
  data() {
    return {
      latestDiagnostic: this.diagnostics.latest,
      previousDiagnostic: this.diagnostics.previous,
      provisionalYear1Diagnostic: this.diagnostics.provisionalYear1,
      provisionalYear2Diagnostic: this.diagnostics.provisionalYear2,
    }
  },
  computed: {
    validators() {
      return validators
    },
  },
}
</script>
