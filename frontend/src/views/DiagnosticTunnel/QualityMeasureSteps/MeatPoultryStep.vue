<template>
  <div>
    <FormErrorCallout v-if="hasError" :errorMessages="errorMessages" />
    <v-row>
      <v-col cols="12" md="8">
        <div class="d-block d-sm-flex align-center">
          <div class="d-flex">
            <v-icon size="30" color="brown">
              mdi-food-steak
            </v-icon>
            <v-icon size="30" color="brown">
              mdi-food-drumstick
            </v-icon>
          </div>
          <label class="ml-4" for="meat-poultry">
            La valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total
            <span class="fr-hint-text mt-2">Optionnel</span>
          </label>
        </div>
        <DsfrCurrencyField
          id="meat-poultry"
          v-model.number="payload.valueMeatPoultryHt"
          @blur="updatePayload"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="hasError"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryHt"
          @autofill="updatePayload"
          purchaseType="totaux viandes et volailles"
          :amount="purchasesSummary.valueMeatPoultryHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />

        <!-- Viande et volailles EGALIM -->
        <div class="d-block d-sm-flex align-center mt-8">
          <div class="d-flex">
            <v-icon size="30" color="green">
              $checkbox-circle-fill
            </v-icon>
            <v-icon size="30" color="brown">
              mdi-food-steak
            </v-icon>
            <v-icon size="30" color="brown">
              mdi-food-drumstick
            </v-icon>
          </div>
          <label class="ml-4" for="meat-poultry-egalim">
            La valeur (en HT) des mes achats EGAlim en viandes et volailles fraiches ou surgelées
            <span class="fr-hint-text mt-2">Optionnel</span>
          </label>
        </div>
        <DsfrCurrencyField
          id="meat-poultry-egalim"
          v-model.number="payload.valueMeatPoultryEgalimHt"
          @blur="updatePayload"
          :error="totalEgalimMeatPoultryError"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryEgalimHt"
          @autofill="updatePayload"
          purchaseType="viandes et volailles EGAlim"
          :amount="purchasesSummary.valueMeatPoultryEgalimHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />

        <!-- Viande et volailles provenance FRANCE -->
        <div class="d-block d-sm-flex align-center mt-8">
          <div class="d-flex">
            <v-icon size="30" color="indigo">
              $france-line
            </v-icon>
            <v-icon size="30" color="brown">
              mdi-food-steak
            </v-icon>
            <v-icon size="30" color="brown">
              mdi-food-drumstick
            </v-icon>
          </div>
          <label class="ml-4" for="meat-poultry-france">
            La valeur (en HT) des mes achats provenance France en viandes et volailles fraiches ou surgelées
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
      </v-col>
    </v-row>
    <ErrorHelper
      v-if="erroringFields.length || errorHelperUsed"
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
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import ErrorHelper from "./ErrorHelper"
import FormErrorCallout from "@/components/FormErrorCallout"
import { toCurrency } from "@/utils"

export default {
  name: "MeatPoultryStep",
  components: { DsfrCurrencyField, PurchaseHint, ErrorHelper, FormErrorCallout },
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
      totalMeatPoultryErrorMessage: null,
      totalEgalimMeatPoultryErrorMessage: null,
      totalFranceMeatPoultryErrorMessage: null,
      totalFamiliesErrorMessage: null,
      errorHelperUsed: false,
      errorHelperFields: [],
    }
  },
  computed: {
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    totalMeatPoultryError() {
      return !!this.totalMeatPoultryErrorMessage
    },
    totalEgalimMeatPoultryError() {
      return !!this.totalEgalimMeatPoultryErrorMessage
    },
    totalFranceMeatPoultryError() {
      return !!this.totalFranceMeatPoultryErrorMessage
    },
    totalFamiliesError() {
      return !!this.totalFamiliesErrorMessage
    },
    hasError() {
      return [
        this.totalMeatPoultryError,
        this.totalEgalimMeatPoultryError,
        this.totalFranceMeatPoultryError,
        this.totalFamiliesError,
      ].some((x) => !!x)
    },
    errorMessages() {
      return [
        this.totalMeatPoultryErrorMessage,
        this.totalFamiliesErrorMessage,
        this.totalEgalimMeatPoultryErrorMessage,
        this.totalFranceMeatPoultryErrorMessage,
      ].filter((x) => !!x)
    },
    erroringFields() {
      const fields = []
      if (this.totalMeatPoultryError) fields.push("valueTotalHt")
      if (this.totalFamiliesError) fields.push(...["valueTotalHt", "valueFishHt"])
      return fields
    },
  },
  methods: {
    updatePayload() {
      this.checkTotal()
      if (!this.hasError) this.$emit("update-payload", { payload: this.payload })
    },
    checkTotal() {
      this.totalMeatPoultryErrorMessage = null
      this.totalFamiliesErrorMessage = null
      this.totalEgalimMeatPoultryErrorMessage = null
      this.totalFranceMeatPoultryErrorMessage = null

      const d = this.payload
      const total = d.valueTotalHt
      const totalMeatPoultry = d.valueMeatPoultryHt
      const totalFish = d.valueFishHt
      const totalFamilies = totalMeatPoultry + totalFish

      if (totalMeatPoultry > total) {
        this.totalMeatPoultryErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
          totalMeatPoultry
        )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
        this.errorHelperFields.push("valueTotalHt")
      } else if (totalFamilies > total) {
        this.totalFamiliesErrorMessage = `Les totaux des achats « viandes et volailles » et « poissons, produits de la mer et de l'aquaculture » ensemble (${toCurrency(
          totalFamilies
        )}) ne doit pas dépasser le total de tous les achats (${toCurrency(total)})`
        this.errorHelperFields.push(...["valueTotalHt", "valueFishHt"])
      } else {
        if (d.valueMeatPoultryEgalimHt > totalMeatPoultry) {
          this.totalEgalimMeatPoultryErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
            totalMeatPoultry
          )}) doit être supérieur au champ EGAlim (${toCurrency(d.valueMeatPoultryEgalimHt)})`
        }
        if (d.valueMeatPoultryFranceHt > totalMeatPoultry) {
          this.totalFranceMeatPoultryErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
            totalMeatPoultry
          )}) doit être supérieur au champ provenance France (${toCurrency(d.valueMeatPoultryFranceHt)})`
        }
      }
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
