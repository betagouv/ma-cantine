<template>
  <div>
    <QualityMeasureValuesInput
      :originalDiagnostic="diagnostic"
      label="La valeur (en HT) de mes achats alimentaires..."
      :readonly="hasActiveTeledeclaration"
      :purchasesSummary="purchasesSummary"
    />
    <fieldset class="d-flex flex-column mt-4">
      <legend class="body-2 mb-2">
        Les valeurs par label des produits de qualité et durables hors bio (facultatif)
      </legend>
      <v-row>
        <v-col cols="12" md="9" class="pr-3">
          <label class="caption mb-1 mt-2" for="label-rouge">Label Rouge</label>
          <v-container class="d-flex pa-0 align-center">
            <div style="min-width: 100px; width: 100px;">
              <img src="/static/images/quality-labels/label-rouge.png" alt="" style="height: 2em;" />
            </div>
            <div class="flex-grow-1">
              <v-text-field
                id="label-rouge"
                hide-details="auto"
                type="number"
                suffix="€ HT"
                :rules="[validators.nonNegativeOrEmpty]"
                validate-on-blur
                solo
                dense
                v-model.number="diagnostic.valueLabelRougeHt"
                :readonly="hasActiveTeledeclaration"
                :disabled="hasActiveTeledeclaration"
              ></v-text-field>
              <PurchaseHint
                v-if="displayPurchaseHints"
                v-model="diagnostic.valueLabelRougeHt"
                purchaseType="Label Rouge"
                :amount="purchasesSummary.rouge"
              />
            </div>
          </v-container>
        </v-col>
        <v-col cols="12" md="9" class="pr-3">
          <label class="caption mb-1 mt-2" for="aoc-aop-igp">AOC / AOP / IGP</label>
          <v-container class="d-flex pa-0 align-center">
            <div style="min-width: 100px;">
              <img src="/static/images/quality-labels/Logo-AOC-AOP.png" alt="" style="height: 2em;" />
              <img src="/static/images/quality-labels/IGP.png" alt="" style="height: 2em;" class="mr-1" />
            </div>
            <div class="flex-grow-1">
              <v-text-field
                id="aoc-aop-igp"
                hide-details="auto"
                type="number"
                suffix="€ HT"
                :rules="[validators.nonNegativeOrEmpty]"
                validate-on-blur
                solo
                dense
                v-model.number="diagnostic.valueAocaopIgpStgHt"
                :readonly="hasActiveTeledeclaration"
                :disabled="hasActiveTeledeclaration"
              ></v-text-field>
              <PurchaseHint
                v-if="displayPurchaseHints"
                v-model="diagnostic.valueAocaopIgpStgHt"
                purchaseType="AOC / AOP / IGP"
                :amount="purchasesSummary.aocAopIgp"
              />
            </div>
          </v-container>
        </v-col>
        <v-col cols="12" md="9" class="pr-3">
          <label class="caption mb-1 mt-2" for="hve">Haute Valeur Environnementale</label>
          <v-container class="d-flex pa-0 align-center">
            <div style="min-width: 100px;">
              <img src="/static/images/quality-labels/hve.png" alt="" style="height: 2em;" />
            </div>
            <div class="flex-grow-1">
              <v-text-field
                id="hve"
                hide-details="auto"
                type="number"
                suffix="€ HT"
                :rules="[validators.nonNegativeOrEmpty]"
                validate-on-blur
                solo
                dense
                v-model.number="diagnostic.valueHveHt"
                :readonly="hasActiveTeledeclaration"
                :disabled="hasActiveTeledeclaration"
              ></v-text-field>
              <PurchaseHint
                v-if="displayPurchaseHints"
                v-model="diagnostic.valueHveHt"
                purchaseType="HVE"
                :amount="purchasesSummary.hve"
              />
            </div>
          </v-container>
        </v-col>
      </v-row>
    </fieldset>
  </div>
</template>

<script>
import QualityMeasureValuesInput from "@/components/KeyMeasureDiagnostic/QualityMeasureValuesInput"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import validators from "@/validators"

export default {
  name: "SimplifiedQualityValues",
  props: {
    originalDiagnostic: Object,
    purchasesSummary: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    QualityMeasureValuesInput,
    PurchaseHint,
  },
  computed: {
    validators() {
      return validators
    },
    diagnostic() {
      return this.originalDiagnostic
    },
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x) && !this.readonly
    },
    hasActiveTeledeclaration() {
      return this.diagnostic.teledeclaration && this.diagnostic.teledeclaration.status === "SUBMITTED"
    },
  },
}
</script>

<style scoped>
fieldset {
  border: none;
}
</style>
