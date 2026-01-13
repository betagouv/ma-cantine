<template>
  <div>
    <FormErrorCallout v-if="hasError" :errorMessages="errorMessages" />
    <v-row>
      <v-col cols="12" md="4">
        <label for="valeurViandesVolailles">
          Total (en € HT) de mes achats en viandes et volailles fraiches ou surgelées
        </label>
        <DsfrCurrencyField
          id="valeurViandesVolailles"
          v-model.number="payload.valeurViandesVolailles"
          @blur="updatePayload"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="hasError"
          :rules="[validators.required, validators.decimalPlaces(2)]"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valeurViandesVolailles"
          @autofill="updatePayload"
          purchaseType="totaux viandes et volailles"
          :amount="purchasesSummary.valeurViandesVolailles"
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
            <!-- viandesVolailles EGalim -->
            <div class="d-block d-sm-flex align-center">
              <v-icon v-if="$vuetify.breakpoint.smAndDown" size="30" color="#4d4db2" class="mr-2">$award-line</v-icon>
              <label for="valeurViandesVolaillesEgalim">
                Total (en € HT) de mes achats EGalim en viandes et volailles
              </label>
            </div>
            <DsfrCurrencyField
              id="valeurViandesVolaillesEgalim"
              v-model.number="payload.valeurViandesVolaillesEgalim"
              @blur="updatePayload"
              :error="totalEgalimViandesVolaillesError"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
              :rules="[validators.required, validators.decimalPlaces(2)]"
            />
            <PurchaseHint
              v-if="displayPurchaseHints"
              v-model="payload.valeurViandesVolaillesEgalim"
              @autofill="updatePayload"
              purchaseType="viandes et volailles EGalim"
              :amount="purchasesSummary.valeurViandesVolaillesEgalim"
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
            <!-- viandesVolailles France -->
            <div class="d-block d-sm-flex align-center">
              <v-icon v-if="$vuetify.breakpoint.smAndDown" size="30" color="#4d4db2" class="mr-2">$france-line</v-icon>
              <label for="valeurViandesVolaillesFrance">
                Total (en € HT) de mes achats origine France en viandes et volailles
                <span class="fr-hint-text mt-2">Optionnel</span>
              </label>
            </div>
            <DsfrCurrencyField
              id="valeurViandesVolaillesFrance"
              v-model.number="payload.valeurViandesVolaillesFrance"
              @blur="updatePayload"
              :error="totalFranceViandesVolaillesError"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            />
            <PurchaseHint
              v-if="displayPurchaseHints"
              v-model="payload.valeurViandesVolaillesFrance"
              @autofill="updatePayload"
              purchaseType="viandes et volailles origine France"
              :amount="purchasesSummary.valeurViandesVolaillesFrance"
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
      totalViandesVolaillesErrorMessage: null,
      totalEgalimViandesVolaillesErrorMessage: null,
      totalFranceViandesVolaillesErrorMessage: null,
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
    totalViandesVolaillesError() {
      return !!this.totalViandesVolaillesErrorMessage
    },
    totalEgalimViandesVolaillesError() {
      return !!this.totalEgalimViandesVolaillesErrorMessage
    },
    totalFranceViandesVolaillesError() {
      return !!this.totalFranceViandesVolaillesErrorMessage
    },
    totalFamiliesError() {
      return !!this.totalFamiliesErrorMessage
    },
    hasError() {
      return [
        this.totalViandesVolaillesError,
        this.totalEgalimViandesVolaillesError,
        this.totalFranceViandesVolaillesError,
        this.totalFamiliesError,
      ].some((x) => !!x)
    },
    errorMessages() {
      return [
        this.totalViandesVolaillesErrorMessage,
        this.totalFamiliesErrorMessage,
        this.totalEgalimViandesVolaillesErrorMessage,
        this.totalFranceViandesVolaillesErrorMessage,
      ].filter((x) => !!x)
    },
    erroringFields() {
      const fields = []
      if (this.totalViandesVolaillesError) fields.push("valeurTotale")
      if (this.totalFamiliesError) fields.push(...["valeurTotale", "valeurProduitsDeLaMer"])
      return fields
    },
  },
  methods: {
    updatePayload() {
      this.checkTotal()
      if (!this.hasError) this.$emit("update-payload", { payload: this.payload })
    },
    checkTotal() {
      this.totalViandesVolaillesErrorMessage = null
      this.totalFamiliesErrorMessage = null
      this.totalEgalimViandesVolaillesErrorMessage = null
      this.totalFranceViandesVolaillesErrorMessage = null

      const d = this.payload
      const total = d.valeurTotale
      const totalMeatPoultry = d.valeurViandesVolailles
      const totalFish = d.valeurProduitsDeLaMer
      const totalFamilies = totalMeatPoultry + totalFish

      if (totalMeatPoultry > total) {
        this.totalViandesVolaillesErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
          totalMeatPoultry
        )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
        this.errorHelperFields.push("valeurTotale")
      } else if (totalFamilies > total) {
        this.totalFamiliesErrorMessage = `Les totaux des achats « viandes et volailles » et « poissons, produits de la mer et de l'aquaculture » ensemble (${toCurrency(
          totalFamilies
        )}) ne doit pas dépasser le total de tous les achats (${toCurrency(total)})`
        this.errorHelperFields.push(...["valeurTotale", "valeurProduitsDeLaMer"])
      } else {
        if (d.valeurViandesVolaillesEgalim > totalMeatPoultry) {
          this.totalEgalimViandesVolaillesErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
            totalMeatPoultry
          )}) doit être supérieur au total EGalim en viandes et volailles (${toCurrency(
            d.valeurViandesVolaillesEgalim
          )})`
        }
        if (d.valeurViandesVolaillesFrance > totalMeatPoultry) {
          this.totalFranceViandesVolaillesErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
            totalMeatPoultry
          )}) doit être supérieur au total origine France en viandes et volailles (${toCurrency(
            d.valeurViandesVolaillesFrance
          )})`
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
