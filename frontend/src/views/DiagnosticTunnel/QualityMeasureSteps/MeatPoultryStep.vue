<template>
  <div>
    <FormErrorCallout v-if="hasError" :errorMessages="errorMessages" />
    <v-row>
      <v-col cols="12" md="4">
        <label for="meat-poultry">
          Total (en € HT) de mes achats en viandes et volailles fraiches ou surgelées
        </label>
        <DsfrCurrencyField
          id="meat-poultry"
          v-model.number="payload.valueMeatPoultryHt"
          @blur="updatePayload"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="hasError"
          :rules="[validators.required, validators.decimalPlaces(2)]"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryHt"
          @autofill="updatePayload"
          purchaseType="totaux viandes et volailles"
          :amount="purchasesSummary.valueMeatPoultryHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </v-col>
      <v-col cols="12" md="8">
        <v-row>
          <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="4" class="pl-14">
            <div class="d-flex align-center justify-center left-border fill-height">
              <v-icon size="25" color="#4d4db2">$award-line</v-icon>
              <p class="fr-text-xs font-weight-bold mb-0 ml-6">EGalim</p>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <!-- Viande et volailles EGalim -->
            <div class="d-block d-sm-flex align-center">
              <v-icon v-if="$vuetify.breakpoint.smAndDown" size="30" color="#4d4db2" class="mr-2">$award-line</v-icon>
              <label for="meat-poultry-egalim">
                Total (en € HT) de mes achats EGalim en viandes et volailles
              </label>
            </div>
            <DsfrCurrencyField
              id="meat-poultry-egalim"
              v-model.number="payload.valueMeatPoultryEgalimHt"
              @blur="updatePayload"
              :error="totalEgalimMeatPoultryError"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
              :rules="[validators.required, validators.decimalPlaces(2)]"
            />
            <PurchaseHint
              v-if="displayPurchaseHints"
              v-model="payload.valueMeatPoultryEgalimHt"
              @autofill="updatePayload"
              purchaseType="viandes et volailles EGalim"
              :amount="purchasesSummary.valueMeatPoultryEgalimHt"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="4" class="pl-14">
            <div class="d-flex align-center justify-center left-border fill-height">
              <v-icon size="25" color="#4d4db2">$france-line</v-icon>
              <p class="fr-text-xs font-weight-bold mb-0 ml-6">FRANCE</p>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <!-- Viande et volailles provenance FRANCE -->
            <div class="d-block d-sm-flex align-center">
              <v-icon v-if="$vuetify.breakpoint.smAndDown" size="30" color="#4d4db2" class="mr-2">$france-line</v-icon>
              <label for="meat-poultry-france">
                Total (en € HT) de mes achats origine France en viandes et volailles
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
import validators from "@/validators"
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
    validators() {
      return validators
    },
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
      const sumMeat = d.valueMeatPoultryEgalimHt + d.valueMeatPoultryFranceHt

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
      } else if (sumMeat > totalMeatPoultry) {
        this.totalFamiliesErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
          totalFish
        )}) doit être supérieur à la somme des valeurs par label (${toCurrency(sumMeat)})`
      } else {
        if (d.valueMeatPoultryEgalimHt > totalMeatPoultry) {
          this.totalEgalimMeatPoultryErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
            totalMeatPoultry
          )}) doit être supérieur au champ EGalim (${toCurrency(d.valueMeatPoultryEgalimHt)})`
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
