<template>
  <div>
    <label :for="'total-' + diagnostic.year" class="body-2">
      La valeur (en HT) de mes achats alimentaires total
    </label>

    <v-text-field
      :id="'total-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[
        validators.nonNegativeOrEmpty,
        validators.gteSum([diagnostic.valueBioHt, diagnostic.valueSustainableHt], totalErrorMessage),
      ]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueTotalHt"
      :readonly="readonly"
      :disabled="readonly"
      :messages="totalError ? [totalErrorMessage] : undefined"
      :error="totalError"
      @blur="totalError = false"
      class="mt-2"
    ></v-text-field>

    <table class="my-4">
      <thead>
        <tr>
          <td></td>
          <th v-for="(family, fId) in families" :key="fId" class="caption" :style="'width: 12%'">
            {{ family.shortText || family.text }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(characteristic, cId) in characteristics" :key="cId">
          <td class="caption">{{ characteristic.text }}</td>
          <th v-for="(family, fId) in families" :key="fId" class="caption">
            <v-text-field
              :id="`${fId}-${cId}-${diagnostic.year}`"
              hide-details="auto"
              type="number"
              :rules="[validators.nonNegativeOrEmpty]"
              validate-on-blur
              solo
              placeholder="0"
              v-model.number="diagnostic[camelize(`${fId}_${cId}`)]"
              :readonly="readonly"
              :disabled="readonly"
              dense
              class="caption"
            ></v-text-field>
            <!-- TODO: label referencing, send values input, validation, styling -->
          </th>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
// import QualityMeasureValuesInput from "@/components/KeyMeasureDiagnostic/QualityMeasureValuesInput"
// import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import validators from "@/validators"
import Constants from "@/constants"

export default {
  name: "ExtendedQualityValues",
  props: {
    originalDiagnostic: Object,
    purchasesSummary: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  // components: {
  //   QualityMeasureValuesInput,
  //   PurchaseHint,
  // },
  data() {
    return {
      totalError: false,
      totalErrorMessage: "Le totale ne peut pas être moins que le somme des valeurs suivantes",
      families: Constants.ProductFamilies,
      characteristics: Constants.TeledeclarationCharacteristics,
    }
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
  methods: {
    checkTotal() {
      // TODO: update
      const result = validators.gteSum(
        [this.diagnostic.valueBioHt, this.diagnostic.valueSustainableHt],
        this.totalErrorMessage
      )(this.diagnostic.valueTotalHt)
      this.totalError = result !== true
    },
    camelize(underscoredString) {
      const stringArray = underscoredString.split("_")
      let string = stringArray[0].toLowerCase()
      for (let index = 1; index < stringArray.length; index++) {
        string += stringArray[index].slice(0, 1).toUpperCase() + stringArray[index].slice(1).toLowerCase()
      }
      return string
    },
  },
}
</script>
