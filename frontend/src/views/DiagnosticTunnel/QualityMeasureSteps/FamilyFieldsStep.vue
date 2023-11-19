<template>
  <v-row class="mb-2">
    <v-col v-for="(family, fId) in families" :key="fId" cols="12" md="6">
      <label :for="inputHtmlId(fId)" class="body-2">
        {{ family.text }}
      </label>

      <DsfrCurrencyField
        :id="inputHtmlId(fId)"
        :rules="[
          validators.nonNegativeOrEmpty,
          validators.decimalPlaces(2),
          validators.lteOrEmpty(payload.valueTotalHt),
        ]"
        solo
        v-model.number="payload[diagnosticKey(fId)]"
        class="mt-2"
        @blur="checkTotal"
      />
      <PurchaseHint
        v-if="displayPurchaseHints"
        v-model="payload[diagnosticKey(fId)]"
        :purchaseType="family.shortText + ' pour ce caractéristique'"
        :amount="purchasesSummary[diagnosticKey(fId)]"
      />
    </v-col>
  </v-row>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import Constants from "@/constants"
import validators from "@/validators"

export default {
  name: "FamilyFieldsStep",
  props: {
    characteristicId: {
      type: String,
      required: true,
    },
    diagnostic: {
      type: Object,
      required: true,
    },
    payload: {
      type: Object,
      required: true,
    },
    purchasesSummary: {
      type: Object,
    },
  },
  components: {
    DsfrCurrencyField,
    PurchaseHint,
  },
  data() {
    return {
      families: Constants.ProductFamilies,
      validators,
    }
  },
  computed: {
    displayPurchaseHints() {
      return false
    },
  },
  methods: {
    inputHtmlId(fId) {
      return `${fId}-${this.characteristicId}-${this.payload.year}`
    },
    checkTotal() {},
    diagnosticKey(family) {
      return this.camelize(`value_${family}_${this.characteristicId}`)
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

<style></style>
