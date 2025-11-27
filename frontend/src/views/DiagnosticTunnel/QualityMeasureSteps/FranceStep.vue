<template>
  <div>
    <FormErrorCallout v-if="totalError" :errorMessages="[totalErrorMessage]" />
    <v-row class="my-0 my-md-6">
      <v-col cols="12" md="8" class="pr-4 pr-md-10">
        <!-- Viande -->
        <div>
          <div class="d-block d-sm-flex align-center">
            <v-icon v-if="$vuetify.breakpoint.smAndDown" size="30" color="#4d4db2" class="mr-2">$france-line</v-icon>
            <label for="meat-poultry-france">
              Total (en € HT) de mes achats provenance France en viandes et volailles
              <span class="fr-hint-text mt-2">Optionnel</span>
            </label>
          </div>
          <DsfrCurrencyField
            id="meat-poultry-france"
            v-model.number="payload.valueMeatPoultryFranceHt"
            @blur="updatePayload"
            :error="totalFranceMeatPoultryError"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          />
          <PurchaseHint
            v-if="displayPurchaseHints"
            v-model="payload.valueMeatPoultryFranceHt"
            @autofill="updatePayload"
            purchaseType="viandes et volailles provenance France"
            :amount="purchasesSummary.valueMeatPoultryFranceHt"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          />
        </div>

        <!-- Charcuterie -->
        <div class="mt-4">
          <label class="ml-4 ml-md-0" for="valueCharcuterieFrance">
            Total (en € HT) de mes achats origine France - Charcuterie
            <span class="fr-hint-text grey--text">
              Optionnel
            </span>
          </label>
          <DsfrCurrencyField
            id="valueCharcuterieFrance"
            v-model.number="payload.valueCharcuterieFrance"
            @blur="updatePayload"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            :error="totalError"
            :rules="[validators.decimalPlaces(2)]"
          />
          <PurchaseHint
            v-if="displayPurchaseHints"
            v-model="payload.valueCharcuterieFrance"
            @autofill="updatePayload"
            purchaseType="« charcuterie origine France »"
            :amount="purchasesSummary.valueCharcuterieFrance"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          />
        </div>

        <!-- Fruits et légumes frais et surgelés -->
        <div class="mt-4">
          <label class="ml-4 ml-md-0" for="valueFruitsEtLegumesFrance">
            Total (en € HT) de mes achats origine France - Fruits et légumes frais et surgelés
            <span class="fr-hint-text grey--text">
              Optionnel
            </span>
          </label>
          <DsfrCurrencyField
            id="valueFruitsEtLegumesFrance"
            v-model.number="payload.valueFruitsEtLegumesFrance"
            @blur="updatePayload"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            :error="totalError"
            :rules="[validators.decimalPlaces(2)]"
          />
          <PurchaseHint
            v-if="displayPurchaseHints"
            v-model="payload.valueFruitsEtLegumesFrance"
            @autofill="updatePayload"
            purchaseType="« fruits et légumes frais et surgelés origine France origine France »"
            :amount="purchasesSummary.valueFruitsEtLegumesFrance"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          />
        </div>

        <!-- BOF (Produits laitiers, beurre et œufs) -->
        <div class="mt-4">
          <label class="ml-4 ml-md-0" for="valueProduitsLaitiersFrance">
            Total (en € HT) de mes achats origine France - BOF (Produits laitiers, beurre et œufs)
            <span class="fr-hint-text grey--text">
              Optionnel
            </span>
          </label>
          <DsfrCurrencyField
            id="valueProduitsLaitiersFrance"
            v-model.number="payload.valueProduitsLaitiersFrance"
            @blur="updatePayload"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            :error="totalError"
            :rules="[validators.decimalPlaces(2)]"
          />
          <PurchaseHint
            v-if="displayPurchaseHints"
            v-model="payload.valueProduitsLaitiersFrance"
            @autofill="updatePayload"
            purchaseType="« BOF (Produits laitiers, beurre et œufs) origine France »"
            :amount="purchasesSummary.valueProduitsLaitiersFrance"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          />
        </div>

        <!-- Boulangerie / Pâtisserie fraîches -->
        <div class="mt-4">
          <label class="ml-4 ml-md-0" for="valueBoulangerieFrance">
            Total (en € HT) de mes achats origine France - Boulangerie / Pâtisserie fraîches
            <span class="fr-hint-text grey--text">
              Optionnel
            </span>
          </label>
          <DsfrCurrencyField
            id="valueBoulangerieFrance"
            v-model.number="payload.valueBoulangerieFrance"
            @blur="updatePayload"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            :error="totalError"
            :rules="[validators.decimalPlaces(2)]"
          />
          <PurchaseHint
            v-if="displayPurchaseHints"
            v-model="payload.valueBoulangerieFrance"
            @autofill="updatePayload"
            purchaseType="« boulangerie / pâtisserie fraîches origine France »"
            :amount="purchasesSummary.valueBoulangerieFrance"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          />
        </div>

        <!-- Boissons -->
        <div class="mt-4">
          <label class="ml-4 ml-md-0" for="valueBoissonsFrance">
            Total (en € HT) de mes achats origine France - Boissons
            <span class="fr-hint-text grey--text">
              Optionnel
            </span>
          </label>
          <DsfrCurrencyField
            id="valueBoissonsFrance"
            v-model.number="payload.valueBoissonsFrance"
            @blur="updatePayload"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            :error="totalError"
            :rules="[validators.decimalPlaces(2)]"
          />
          <PurchaseHint
            v-if="displayPurchaseHints"
            v-model="payload.valueBoissonsFrance"
            @autofill="updatePayload"
            purchaseType="« boissons origine France »"
            :amount="purchasesSummary.valueBoissonsFrance"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          />
        </div>

        <!-- Autres produits frais, surgelés et d’épicerie -->
        <div class="mt-4">
          <label class="ml-4 ml-md-0" for="valueAutresFrance">
            Total (en € HT) de mes achats origine France - Autres produits frais, surgelés et d’épicerie
            <span class="fr-hint-text grey--text">
              Optionnel
            </span>
          </label>
          <DsfrCurrencyField
            id="valueAutresFrance"
            v-model.number="payload.valueAutresFrance"
            @blur="updatePayload"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            :error="totalError"
            :rules="[validators.decimalPlaces(2)]"
          />
          <PurchaseHint
            v-if="displayPurchaseHints"
            v-model="payload.valueAutresFrance"
            @autofill="updatePayload"
            purchaseType="« autres produits frais, surgelés et d’épicerie origine France »"
            :amount="purchasesSummary.valueAutresFrance"
            :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          />
        </div>
      </v-col>
      <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="4" class="pl-14">
        <div class="d-flex align-center justify-center left-border fill-height">
          <v-icon size="25" color="#4d4db2">$france-line</v-icon>
          <p class="fr-text-xs font-weight-bold mb-0 ml-6">FRANCE</p>
        </div>
      </v-col>
      <!--
        <v-col md="4" class="d-flex align-center pl-10 left-border" v-if="$vuetify.breakpoint.mdAndUp">
          Tile
        </v-col>
      -->
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
        d.valueCharcuterieFrance,
        d.valueFruitsLegumesFrance,
        d.valueBoeufFrance,
        d.valueBoulangerieFrance,
        d.valueBoissonsFrance,
        d.valueAutresFrance,
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
