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
          <label class="fr-text ml-4" :for="'valeurViandesVolailles' + diagnostic.year">
            La valeur totale (en € HT) de mes achats en viandes et volailles fraiches ou surgelées
          </label>
        </div>
        <DsfrCurrencyField
          :id="'valeurViandesVolailles' + diagnostic.year"
          v-model.number="payload.valeurViandesVolailles"
          @blur="checkTotal"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="hasViandesVolaillesError"
          :rules="[validators.required, validators.decimalPlaces(2)]"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valeurViandesVolailles"
          @autofill="checkTotal"
          purchaseType="totaux viandes et volailles"
          :amount="purchasesSummary.valeurViandesVolailles"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
        <!-- Poissons -->
        <div class="d-block d-sm-flex align-center mt-8">
          <div class="d-flex">
            <v-icon size="30" color="blue">
              mdi-fish
            </v-icon>
          </div>
          <label class="fr-text ml-4" :for="'valeurProduitsDeLaMer' + diagnostic.year">
            La valeur totale (en € HT) de mes achats en poissons, produits de la mer et de l'aquaculture
          </label>
        </div>
        <DsfrCurrencyField
          :id="'valeurProduitsDeLaMer' + diagnostic.year"
          v-model.number="payload.valeurProduitsDeLaMer"
          :error="hasProduitsDeLaMerError"
          @blur="checkTotal"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valeurProduitsDeLaMer"
          @autofill="checkTotal"
          purchaseType="totaux de poissons, produits de la mer et de l'aquaculture"
          :amount="purchasesSummary.valeurProduitsDeLaMer"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
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
</template>

<script>
import validators from "@/validators"
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import FormErrorCallout from "@/components/FormErrorCallout"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import ErrorHelper from "./ErrorHelper"
import Constants from "@/constants"
import { toCurrency, getCharacteristicFromField } from "@/utils"

export default {
  name: "MeatFishStep",
  components: { DsfrCurrencyField, FormErrorCallout, PurchaseHint, ErrorHelper },
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
    const tdGroups = Constants.TeledeclarationCharacteristicGroups

    const viandesVolaillesLawFields = []
    const produitsDeLaMerLawFields = []
    const lawFields = tdGroups.egalim.fields.concat(tdGroups.nonEgalim.fields)
    lawFields.forEach((field) => {
      if (field.startsWith("valeurViandesVolailles")) viandesVolaillesLawFields.push(field)
      else if (field.startsWith("valeurProduitsDeLaMer")) produitsDeLaMerLawFields.push(field)
    })
    const viandesVolaillesOutsideLawFields = []
    const produitsDeLaMerOutsideLawFields = []
    const outsideLawFields = [...tdGroups.outsideLaw.fields]
    outsideLawFields.forEach((field) => {
      if (field.startsWith("valeurViandesVolailles")) viandesVolaillesOutsideLawFields.push(field)
      else if (field.startsWith("valeurProduitsDeLaMer")) produitsDeLaMerOutsideLawFields.push(field)
    })

    return {
      errorHelperFields: [],
      errorHelperUsed: false,
      totalField: "valeurTotale",
      viandesVolaillesLawFields,
      viandesVolaillesOutsideLawFields,
      produitsDeLaMerLawFields,
      produitsDeLaMerOutsideLawFields,
      viandesVolaillesTotalError: false,
      produitsDeLaMerTotalError: false,
      combinedTotalError: false,
      viandesVolaillesLawSubtotalError: false,
      viandesVolaillesOutsideLawSubtotalErrors: [],
      produitsDeLaMerLawSubtotalError: false,
      produitsDeLaMerOutsideLawSubtotalErrors: [],
    }
  },
  computed: {
    validators() {
      return validators
    },
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
    },
    erroringFields() {
      const fields = []
      if (this.viandesVolaillesTotalError) fields.push(this.totalField)
      if (this.produitsDeLaMerTotalError) fields.push(this.totalField)
      if (this.combinedTotalError) fields.push(this.totalField)
      if (this.viandesVolaillesLawSubtotalError) fields.push(...this.viandesVolaillesLawFields)
      fields.push(...this.viandesVolaillesOutsideLawSubtotalErrors)
      if (this.produitsDeLaMerLawSubtotalError) fields.push(...this.produitsDeLaMerLawFields)
      fields.push(...this.produitsDeLaMerOutsideLawSubtotalErrors)
      return fields
    },
    hasError() {
      return this.erroringFields.length
    },
    hasViandesVolaillesError() {
      return (
        this.viandesVolaillesTotalError || this.combinedTotalError || this.viandesVolaillesLawSubtotalError // || this.viandesVolaillesOutsideLawSubtotalError
      )
    },
    hasProduitsDeLaMerError() {
      return (
        this.produitsDeLaMerTotalError || this.combinedTotalError || this.produitsDeLaMerLawSubtotalError // || this.produitsDeLaMerOutsideLawSubtotalError
      )
    },
    errorMessages() {
      return [
        this.viandesVolaillesTotalErrorMessage,
        this.produitsDeLaMerTotalErrorMessage,
        this.combinedTotalErrorMessage,
        this.viandesVolaillesLawSubtotalErrorMessage,
        ...this.viandesVolaillesOutsideLawSubtotalErrorMessages,
        this.produitsDeLaMerLawSubtotalErrorMessage,
        ...this.produitsDeLaMerOutsideLawSubtotalErrorMessages,
      ].filter((x) => !!x)
    },
    // error messages text
    viandesVolaillesTotalErrorMessage() {
      if (!this.viandesVolaillesTotalError) return null
      return `Le total des achats viandes et volailles (${toCurrency(
        this.payload.valeurViandesVolailles
      )}) ne peut pas excéder le total des achats (${toCurrency(this.payload.valeurTotale)})`
    },
    produitsDeLaMerTotalErrorMessage() {
      if (!this.produitsDeLaMerTotalError) return null
      return `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
        this.payload.valeurProduitsDeLaMer
      )}) ne peut pas excéder le total des achats (${toCurrency(this.payload.valeurTotale)})`
    },
    combinedTotalErrorMessage() {
      if (!this.combinedTotalError) return null
      const totalFamilies = (this.payload.valeurViandesVolailles || 0) + (this.payload.valeurProduitsDeLaMer || 0)
      return `Les totaux des achats « viandes et volailles » et « poissons, produits de la mer et de l'aquaculture » ensemble (${toCurrency(
        totalFamilies
      )}) ne doit pas dépasser le total de tous les achats (${toCurrency(this.payload.valeurTotale)})`
    },
    viandesVolaillesLawSubtotalErrorMessage() {
      if (!this.viandesVolaillesLawSubtotalError) return null
      const byLabel = this.sum(this.viandesVolaillesLawFields)
      return `Le total des achats viandes et volailles (${toCurrency(
        this.payload.valeurViandesVolailles
      )}) doit être supérieur à la somme des valeurs par label (${toCurrency(byLabel)})`
    },
    viandesVolaillesOutsideLawSubtotalErrorMessages() {
      const fieldPrefix = "valeurViandesVolailles"
      const outsideLawGroup = Constants.TeledeclarationCharacteristicGroups.outsideLaw
      const totalField = this.payload.valeurViandesVolailles
      return this.viandesVolaillesOutsideLawSubtotalErrors.map((field) => {
        const characteristic = getCharacteristicFromField(field, fieldPrefix, outsideLawGroup)
        return `Le total des achats viandes et volailles (${toCurrency(
          totalField
        )}) doit être supérieur au champ « viandes et volailles : ${characteristic.text} » (${toCurrency(
          this.payload[field]
        )})`
      })
    },
    produitsDeLaMerLawSubtotalErrorMessage() {
      if (!this.produitsDeLaMerLawSubtotalError) return null
      const byLabel = this.sum(this.produitsDeLaMerLawFields)
      return `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
        this.payload.valeurProduitsDeLaMer
      )}) doit être supérieur à la somme des valeurs par label (${toCurrency(byLabel)})`
    },
    produitsDeLaMerOutsideLawSubtotalErrorMessages() {
      const fieldPrefix = "valeurProduitsDeLaMer"
      const outsideLawGroup = Constants.TeledeclarationCharacteristicGroups.outsideLaw
      const totalField = this.payload.valeurProduitsDeLaMer
      return this.produitsDeLaMerOutsideLawSubtotalErrors.map((field) => {
        const characteristic = getCharacteristicFromField(field, fieldPrefix, outsideLawGroup)
        return `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
          totalField
        )}) doit être supérieur au champ « poissons, produits de la mer et de l'aquaculture : ${
          characteristic.text
        } » (${toCurrency(this.payload[field])})`
      })
    },
  },
  methods: {
    checkTotal() {
      this.checkFamilyTotal("viandesVolailles")
      this.checkFamilyTotal("produitsDeLaMer")

      this.combinedTotalError = false

      const d = this.payload
      const total = d.valeurTotale
      const viandesVolaillesTotal = d.valeurViandesVolailles
      const produitsDeLaMerTotal = d.valeurProduitsDeLaMer

      if (
        !this.viandesVolaillesTotalError &&
        !this.produitsDeLaMerTotalError &&
        viandesVolaillesTotal + produitsDeLaMerTotal > total
      ) {
        this.combinedTotalError = true
        this.errorHelperFields.push(this.totalField)
      }
    },
    checkFamilyTotal(family) {
      // family === "viandesVolailles" or "produitsDeLaMer"
      this[`${family}TotalError`] = false
      this[`${family}LawSubtotalError`] = false
      this[`${family}OutsideLawSubtotalError`] = false

      const d = this.payload
      const total = d.valeurTotale
      const familyTotal = family === "viandesVolailles" ? d.valeurViandesVolailles : d.valeurProduitsDeLaMer
      if (!familyTotal) return

      if (familyTotal > total) {
        this[`${family}TotalError`] = true
        this.errorHelperFields.push(this.totalField)
      }

      if (!this[`${family}TotalError`] && this.sum(this[`${family}LawFields`]) > familyTotal) {
        this[`${family}LawSubtotalError`] = true
        this.errorHelperFields.push(...this[`${family}LawFields`])
      }
      this[`${family}OutsideLawSubtotalErrors`] = []
      this[`${family}OutsideLawFields`].forEach((field) => {
        if (!this[`${family}TotalError`] && d[field] > familyTotal) {
          this[`${family}OutsideLawSubtotalErrors`].push(field)
          this.errorHelperFields.push(field)
        }
      })
    },
    errorUpdate() {
      this.errorHelperUsed = true
      this.checkTotal()
    },
    sum(fields) {
      const sum = fields.reduce((acc, field) => acc + (this.payload[field] || 0), 0)
      return +sum.toFixed(2)
    },
  },
  mounted() {
    this.checkTotal()
  },
}
</script>
