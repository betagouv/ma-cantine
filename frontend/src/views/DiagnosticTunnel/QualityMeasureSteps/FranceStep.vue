<template>
  <section>
    <!-- A SUPPR -->
    <pre>{{ purchasesSummary }}</pre>
    <!-- A SUPPR on garde uniquement la div dans tpl -->

    <div>
      <FormErrorCallout v-if="totalError" :errorMessages="[totalErrorMessage]" />

      <v-row class="my-0 my-md-6">
        <v-col cols="12" md="8" class="pr-4 pr-md-10">
          <!-- Charcuterie -->
          <div>
            <label class="ml-4 ml-md-0" for="TO_FILL_TOTAL_FRANCE_CHARCUTERIE">
              Total (en € HT) de mes achats origine France - Charcuterie
              <span class="fr-hint-text grey--text">
                Optionnel
              </span>
            </label>
            <DsfrCurrencyField
              id="TO_FILL_TOTAL_FRANCE_CHARCUTERIE"
              v-model.number="payload.TO_FILL_TOTAL_FRANCE_CHARCUTERIE"
              @blur="updatePayload"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
              :error="totalError"
              :rules="[validators.decimalPlaces(2)]"
            />
            <PurchaseHint
              v-if="displayPurchaseHints"
              v-model="payload.valueCharcuterieFrance"
              @autofill="updatePayload"
              purchaseType="charcuterie origine France"
              :amount="purchasesSummary.valueCharcuterieFrance"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
            />
          </div>

          <!-- Fruits et légumes frais et surgelés -->
          <div class="mt-4">
            <label class="ml-4 ml-md-0" for="TO_FILL_TOTAL_FRANCE_FRUITS_ET_LEGUMES">
              Total (en € HT) de mes achats origine France - Fruits et légumes frais et surgelés
              <span class="fr-hint-text grey--text">
                Optionnel
              </span>
            </label>
            <DsfrCurrencyField
              id="TO_FILL_TOTAL_FRANCE_FRUITS_ET_LEGUMES"
              v-model.number="payload.TO_FILL_TOTAL_FRANCE_FRUITS_ET_LEGUMES"
              @blur="updatePayload"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
              :error="totalError"
              :rules="[validators.decimalPlaces(2)]"
            />
            <PurchaseHint
              v-if="displayPurchaseHints"
              v-model="payload.valueFruitsEtLegumesFrance"
              @autofill="updatePayload"
              purchaseType="fruits et légumes frais et surgelés origine France"
              :amount="purchasesSummary.valueFruitsEtLegumesFrance"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
            />
          </div>

          <!-- BOF (Produits laitiers, beurre et œufs) -->
          <div class="mt-4">
            <label class="ml-4 ml-md-0" for="TO_FILL_TOTAL_FRANCE_BOF">
              Total (en € HT) de mes achats origine France - BOF (Produits laitiers, beurre et œufs)
              <span class="fr-hint-text grey--text">
                Optionnel
              </span>
            </label>
            <DsfrCurrencyField
              id="TO_FILL_TOTAL_FRANCE_BOF"
              v-model.number="payload.TO_FILL_TOTAL_FRANCE_BOF"
              @blur="updatePayload"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
              :error="totalError"
              :rules="[validators.decimalPlaces(2)]"
            />
            <PurchaseHint
              v-if="displayPurchaseHints"
              v-model="payload.valueProduitsLaitiersFrance"
              @autofill="updatePayload"
              purchaseType="BOF (Produits laitiers, beurre et œufs)"
              :amount="purchasesSummary.valueProduitsLaitiersFrance"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
            />
          </div>
        </v-col>
        <v-col md="4" class="d-flex align-center pl-10 left-border" v-if="$vuetify.breakpoint.mdAndUp">
          <!-- Tile -->
        </v-col>
      </v-row>
      <ErrorHelper
        v-if="hasError || errorHelperUsed"
        :showFields="errorHelperFields"
        :errorFields="erroringFields"
        :diagnostic="payload"
        :purchasesSummary="purchasesSummary"
        @field-update="errorUpdate"
        class="mt-8"
      />
    </div>
  </section>
</template>

<script>
import validators from "@/validators"
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import { toCurrency } from "@/utils"
import FormErrorCallout from "@/components/FormErrorCallout"
import ErrorHelper from "./ErrorHelper"

export default {
  name: "OtherEgalimStep",
  components: { DsfrCurrencyField, PurchaseHint, FormErrorCallout, ErrorHelper },
  props: {
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
  data() {
    return {
      totalErrorMessage: null,
      errorHelperUsed: false,
      errorHelperFields: ["valueTotalHt"],
    }
  },
  computed: {
    validators() {
      return validators
    },
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    totalError() {
      return !!this.totalErrorMessage
    },
    erroringFields() {
      return this.totalError ? this.errorHelperFields : []
    },
    hasError() {
      return [this.totalErrorMessage].some((x) => !!x)
    },
  },
  methods: {
    updatePayload() {
      this.checkTotal()
      if (!this.totalError) this.$emit("update-payload", { payload: this.payload })
    },
    checkTotal() {
      this.totalErrorMessage = null

      const d = this.payload
      const sumFrance = this.sumAllFrance()
      const total = d.valueTotalHt

      if (sumFrance > total) {
        this.totalErrorMessage = `Le total de vos achats alimentaires (${toCurrency(
          d.valueTotalHt
        )}) doit être plus élévé que la somme des valeurs origine France (${toCurrency(sumFrance || 0)})`
      }
    },
    sumAllFrance() {
      const d = this.payload
      const franceValues = [
        d.TO_FILL_TOTAL_FRANCE_CHARCUTERIE,
        d.TO_FILL_TOTAL_FRANCE_FRUITS_ET_LEGUMES,
        d.TO_FILL_TOTAL_FRANCE_BOF,
      ]
      let total = 0
      franceValues.forEach((val) => {
        total += parseFloat(val) || 0
      })
      return total
    },
    errorUpdate() {
      this.errorHelperUsed = true
      this.checkTotal()
    },
  },
  mounted() {
    this.checkTotal()
  },
}
</script>

<style scoped>
.left-border {
  border-left: solid #4d4db2;
}
</style>
