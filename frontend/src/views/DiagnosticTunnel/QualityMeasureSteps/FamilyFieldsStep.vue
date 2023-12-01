<template>
  <div class="mt-n4">
    <p v-if="groupId === 'egalim'">
      <strong>Produit ayant plusieurs labels</strong>
      : la valeur d’achat ne pourra être comptée que dans une seule des catégories. Par exemple, un produit à la fois
      biologique et label rouge ne sera comptabilisé que dans la catégorie « bio ».
      <!-- TODO: list of prioritisation ? -->
    </p>
    <p v-else-if="groupId === 'nonEgalim'">
      Merci de renseigner les montants des produits hors EGAlim
    </p>
    <p v-else-if="groupId === 'outsideLaw'">
      Ici, vous pouvez affecter le produit dans plusieurs caractéristiques. Par exemple, un produit à la fois biologique
      et local pourra être comptabilisé dans les deux champs « bio » et « local ».
    </p>
    <p v-if="characteristicId === 'LOCAL'">
      Suivant votre propre définition de « local ».
    </p>
    <FormErrorCallout v-if="hasError" :errorMessages="errorMessages" />
    <v-row>
      <v-col v-for="(family, fId) in families" :key="fId" cols="12" md="6" class="py-2">
        <label :for="fId" class="fr-text">
          {{ family.text }}
        </label>

        <DsfrCurrencyField
          :id="fId"
          :rules="[
            validators.nonNegativeOrEmpty,
            validators.decimalPlaces(2),
            validators.lteOrEmpty(payload.valueTotalHt),
          ]"
          solo
          v-model.number="payload[diagnosticKey(fId)]"
          @blur="fieldUpdate(diagnosticKey(fId))"
          class="mt-2"
          :error="fieldHasError(diagnosticKey(fId))"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload[diagnosticKey(fId)]"
          :purchaseType="family.shortText + ' pour ce caractéristique'"
          :amount="purchasesSummary[diagnosticKey(fId)]"
          @autofill="fieldUpdate(diagnosticKey(fId))"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import FormErrorCallout from "@/components/FormErrorCallout"
import Constants from "@/constants"
import validators from "@/validators"
import { approTotals, toCurrency, getCharacteristicFromField } from "@/utils"

export default {
  name: "FamilyFieldsStep",
  props: {
    characteristicId: {
      type: String,
      required: true,
    },
    groupId: {
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
    FormErrorCallout,
  },
  data() {
    return {
      families: Constants.ProductFamilies,
      validators,
      fieldTotalErrorMessage: false,
      outsideLawErrorMessages: [],
      erroringFieldName: null,
      lastUpdatedFieldName: null,
      errorOnLoad: false,
      meatTotalErrorMessage: null,
      fishTotalErrorMessage: null,
    }
  },
  computed: {
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    hasError() {
      return (
        !!this.fieldTotalErrorMessage ||
        !!this.outsideLawErrorMessages.length ||
        !!this.meatTotalErrorMessage ||
        !!this.fishTotalErrorMessage
      )
    },
    hasTotalError() {
      return !!this.fieldTotalErrorMessage || !!this.outsideLawErrorMessages.length
    },
    errorMessages() {
      return [
        this.fieldTotalErrorMessage,
        ...this.outsideLawErrorMessages,
        this.meatTotalErrorMessage,
        this.fishTotalErrorMessage,
      ].filter((x) => !!x)
    },
  },
  methods: {
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
    populateSimplifiedDiagnostic() {
      if (this.hasError) return
      const { bioTotal, siqoTotal, perfExtTotal, egalimOthersTotal } = approTotals(this.payload)
      this.payload.valueBioHt = bioTotal
      this.payload.valueSustainableHt = siqoTotal
      this.payload.valueExternalityPerformanceHt = perfExtTotal
      this.payload.valueEgalimOthersHt = egalimOthersTotal

      const { meatPoultryEgalim, meatPoultryFrance } = this.meatPoultryTotals()
      this.payload.valueMeatPoultryEgalimHt = meatPoultryEgalim
      this.payload.valueMeatPoultryFranceHt = meatPoultryFrance

      const { fishEgalim } = this.fishTotals()
      this.payload.valueFishEgalimHt = fishEgalim
    },
    meatPoultryTotals() {
      const egalimFields = Constants.TeledeclarationCharacteristicGroups.egalim.fields
      const outsideLawFields = Constants.TeledeclarationCharacteristicGroups.outsideLaw.fields
      const allFields = egalimFields.concat(outsideLawFields)

      let meatPoultryEgalim = 0
      let meatPoultryFrance = 0

      allFields.forEach((field) => {
        const isMeatPoultry = field.includes("ViandesVolailles")
        const value = parseFloat(this.payload[field])
        if (!isMeatPoultry || !value) return
        const isEgalim = egalimFields.includes(field)

        // Note that it can be both egalim and provenance France
        if (isEgalim) meatPoultryEgalim += value
        if (field.endsWith("France")) meatPoultryFrance = value // only one France meat field
      })
      meatPoultryEgalim = +meatPoultryEgalim.toFixed(2)
      meatPoultryFrance = +meatPoultryFrance.toFixed(2)
      return { meatPoultryEgalim, meatPoultryFrance }
    },
    fishTotals() {
      let fishEgalim = 0

      const egalimFields = Constants.TeledeclarationCharacteristicGroups.egalim.fields

      egalimFields.forEach((field) => {
        const isFish = field.includes("ProduitsDeLaMer")
        const value = parseFloat(this.payload[field])
        if (!isFish || !value) return
        fishEgalim += value
      })
      fishEgalim = +fishEgalim.toFixed(2)
      return { fishEgalim }
    },
    checkTotal() {
      this.fieldTotalErrorMessage = null
      this.meatTotalErrorMessage = null
      this.fishTotalErrorMessage = null
      this.outsideLawErrorMessages = []

      const groups = Constants.TeledeclarationCharacteristicGroups
      const sumFields = groups.egalim.fields.concat(groups.nonEgalim.fields)
      const declaredTotal = +this.payload.valueTotalHt
      const fieldTotal = this.sum(sumFields)
      if (fieldTotal > declaredTotal) {
        this.fieldTotalErrorMessage = `Le total de tous vos achats ${toCurrency(
          fieldTotal
        )} doit être inferieur du total saisi ${toCurrency(declaredTotal)}`
      }
      const outsideLaw = {
        FRANCE: "France",
        SHORT_DISTRIBUTION: "ShortDistribution",
        LOCAL: "Local",
      }
      if (outsideLaw[this.characteristicId]) {
        // in the outsideLaw group, a product can be counted in more than one category, so we check if any of the
        // totals for each of the three categories is greater than the main total
        this.checkTotalForCategory(groups.outsideLaw, outsideLaw[this.characteristicId])
      }

      // check meat and fish totals
      const { meatPoultryEgalim } = this.meatPoultryTotals()
      const sumMeat = meatPoultryEgalim + (this.payload.valueViandesVolaillesNonEgalim || 0)
      const totalMeat = this.payload.valueMeatPoultryHt
      if (sumMeat > totalMeat) {
        this.meatTotalErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
          totalMeat
        )}) doit être supérieur à la somme des valeurs par label (${toCurrency(sumMeat)})`
      }
      const { fishEgalim } = this.fishTotals()
      const sumFish = fishEgalim + (this.payload.valueProduitsDeLaMerNonEgalim || 0)
      const totalFish = this.payload.valueFishHt
      if (sumFish > totalFish) {
        this.fishTotalErrorMessage = `Le total des achats produits aquatiques (${toCurrency(
          totalFish
        )}) doit être supérieur à la somme des valeurs par label (${toCurrency(sumFish)})`
      }

      if (!this.hasError) {
        this.errorOnLoad = false
        this.erroringFieldName = null
      }
    },
    checkTotalForCategory(group, fieldSuffix) {
      const fields = group.fields.filter((field) => field.endsWith(fieldSuffix))
      const total = this.sum(fields)
      if (total > this.payload.valueTotalHt) {
        const char = getCharacteristicFromField("_" + fieldSuffix, "_", group)
        const message = `Le total de vos achats « ${char.text} », ${toCurrency(
          total
        )}, doit être inferieur du total saisi ${toCurrency(this.payload.valueTotalHt)}`
        this.outsideLawErrorMessages.push(message)
      }
    },
    fieldUpdate(fieldName) {
      if (this.diagnostic[fieldName] === this.payload[fieldName]) return
      this.lastUpdatedFieldName = fieldName
      this.checkTotal()
      this.populateSimplifiedDiagnostic()
    },
    sum(fields) {
      return fields.reduce((acc, field) => acc + (this.payload[field] || 0), 0)
    },
    fieldHasError(fieldName) {
      if (fieldName.startsWith("valueViandesVolailles") && !!this.meatTotalErrorMessage) return true
      if (fieldName.startsWith("valueProduitsDeLaMer") && !!this.fishTotalErrorMessage) return true
      return !!this.payload[fieldName] && (this.errorOnLoad || this.hasTotalError)
    },
  },
  mounted() {
    this.checkTotal()
  },
  watch: {
    $route() {
      this.checkTotal()
    },
  },
}
</script>
