<template>
  <div>
    <div class="d-flex mb-4 align-center">
      <LogoBio v-if="characteristicId === 'BIO'" style="max-height: 30px;" />
      <div
        v-else
        v-for="label in qualityLabels(characteristicId)"
        :key="label.title || label.icon"
        class="d-flex flex-column justify-center"
      >
        <img v-if="label.src" :src="`/static/images/quality-labels/${label.src}`" alt="" style="max-height: 30px;" />
        <v-icon class="mt-n1" :color="label.color" v-else-if="label.icon" size="30">
          {{ label.icon }}
        </v-icon>
      </div>
      <h2 class="ml-4">{{ characteristicName }}</h2>
    </div>
    <p v-if="groupId === 'egalim'" class="fr-text-sm">
      <strong>Produit ayant plusieurs labels</strong>
      : la valeur d’achat ne pourra être comptée que dans une seule des catégories. Par exemple, un produit à la fois
      biologique et label rouge ne sera comptabilisé que dans la catégorie « bio ».
      <!-- TODO: list of prioritisation ? -->
    </p>
    <p v-else-if="groupId === 'nonEgalim'" class="fr-text-sm">
      Merci de renseigner les montants des produits hors EGalim
    </p>
    <p v-else-if="groupId === 'outsideLaw'" class="fr-text-sm">
      Ici, vous pouvez affecter le produit dans plusieurs caractéristiques. Par exemple, un produit à la fois biologique
      et local pourra être comptabilisé dans les deux champs « bio » et « local ».
    </p>
    <p v-if="characteristicId === 'LOCAL'" class="fr-text-sm">
      Suivant votre propre définition de « local ».
    </p>
    <FormErrorCallout v-if="hasError" :errorMessages="errorMessages" />
    <v-row>
      <v-col v-for="(family, fId) in families" :key="fId" cols="12" md="6" class="py-2">
        <label :for="fId" :class="`fr-text ${!validFamily(fId) ? 'grey--text text--darken-1' : ''}`">
          {{ family.text }}
        </label>
        <div v-if="validFamily(fId)">
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
            :disabled="!validFamily(fId)"
            :readonly="!validFamily(fId)"
          />
          <PurchaseHint
            v-if="displayPurchaseHints && validFamily(fId)"
            v-model="payload[diagnosticKey(fId)]"
            :purchaseType="family.shortText + ' pour cette caractéristique'"
            :amount="purchasesSummary[diagnosticKey(fId)]"
            @autofill="fieldUpdate(diagnosticKey(fId))"
          />
        </div>
        <p v-else class="fr-text-sm grey--text text--darken-1 mt-2">
          Non applicable
        </p>
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
import labels from "@/data/quality-labels.json"
import LogoBio from "@/components/LogoBio"
import { approTotals, toCurrency, getCharacteristicFromFieldSuffix } from "@/utils"

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
    LogoBio,
    FormErrorCallout,
  },
  data() {
    return {
      families: Constants.ProductFamilies,
      validators,
      fieldTotalErrorMessage: false,
      outsideLawErrorMessages: [],
      erroringFieldName: null,
      errorOnLoad: false,
      meatTotalErrorMessage: null,
      fishTotalErrorMessage: null,
      meatFieldPrefix: "valueViandesVolailles",
      fishFieldPrefix: "valueProduitsDeLaMer",
    }
  },
  computed: {
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    characteristicName() {
      return Constants.TeledeclarationCharacteristics[this.characteristicId]?.text
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
    possibleFamilies() {
      const exceptions = Constants.CharacteristicFamilyExceptions[this.characteristicId] || []
      return Object.keys(this.families).filter((id) => exceptions.indexOf(id) === -1)
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
        const isMeatPoultry = field.startsWith(this.meatFieldPrefix)
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
        const isFish = field.startsWith(this.fishFieldPrefix)
        const value = parseFloat(this.payload[field])
        if (!isFish || !value) return
        fishEgalim += value
      })
      fishEgalim = +fishEgalim.toFixed(2)
      return { fishEgalim }
    },
    qualityLabels(characteristicId) {
      let singleLabel
      let labelGroup
      switch (characteristicId) {
        case "LABEL_ROUGE":
          singleLabel = labels.find((l) => l.src.startsWith("label-rouge"))
          break
        case "AOCAOP_IGP_STG":
          labelGroup = [
            labels.find((l) => l.src.startsWith("Logo-AOC")),
            labels.find((l) => l.src.startsWith("IGP")),
            labels.find((l) => l.src.startsWith("STG")),
          ]
          return labelGroup
        case "HVE":
          singleLabel = labels.find((l) => l.src.startsWith("hve"))
          break
        case "PECHE_DURABLE":
          singleLabel = labels.find((l) => l.src.endsWith("peche-durable.png"))
          break
        case "RUP":
          singleLabel = labels.find((l) => l.src.startsWith("rup"))
          break
        case "COMMERCE_EQUITABLE":
          singleLabel = labels.find((l) => l.src.startsWith("commerce-equitable"))
          break
      }
      singleLabel = singleLabel || Constants.MiscLabelIcons[characteristicId]
      if (singleLabel) {
        return [singleLabel]
      }
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
        this.fieldTotalErrorMessage = this.errorMessage(fieldTotal, declaredTotal, 1)
      }
      const outsideLawSuffix = {
        FRANCE: "France",
        SHORT_DISTRIBUTION: "ShortDistribution",
        LOCAL: "Local",
      }[this.characteristicId]

      if (outsideLawSuffix) {
        // in the outsideLaw group, a product can be counted in more than one category, so we check if any of the
        // totals for each of the three categories is greater than the main total
        const totalErrorMessage = this.getOutsideLawTotalErrorMessage(outsideLawSuffix)
        if (totalErrorMessage) this.outsideLawErrorMessages.push(totalErrorMessage)

        const char = getCharacteristicFromFieldSuffix(outsideLawSuffix, groups.outsideLaw)

        const meatFieldName = this.meatFieldPrefix + outsideLawSuffix
        const meatOutsideLaw = this.payload[meatFieldName]
        const meatTotal = this.payload.valueMeatPoultryHt
        if (meatOutsideLaw > meatTotal) {
          const message = this.errorMessage(meatOutsideLaw, meatTotal, 3, this.meatFieldPrefix, char.text)
          this.outsideLawErrorMessages.push(message)
        }

        const fishFieldName = this.fishFieldPrefix + outsideLawSuffix
        const fishOutsideLaw = this.payload[fishFieldName]
        const fishTotal = this.payload.valueFishHt
        if (fishOutsideLaw > fishTotal) {
          const message = this.errorMessage(fishOutsideLaw, fishTotal, 3, this.fishFieldPrefix, char.text)
          this.outsideLawErrorMessages.push(message)
        }
      }

      // check meat and fish totals
      const { meatPoultryEgalim } = this.meatPoultryTotals()
      const sumMeat = meatPoultryEgalim + (this.payload.valueViandesVolaillesNonEgalim || 0)
      const totalMeat = this.payload.valueMeatPoultryHt
      if (sumMeat > totalMeat) {
        this.meatTotalErrorMessage = this.errorMessage(sumMeat, totalMeat, 3, this.meatFieldPrefix)
      }
      const { fishEgalim } = this.fishTotals()
      const sumFish = fishEgalim + (this.payload.valueProduitsDeLaMerNonEgalim || 0)
      const totalFish = this.payload.valueFishHt
      if (sumFish > totalFish) {
        this.fishTotalErrorMessage = this.errorMessage(sumFish, totalFish, 3, this.fishFieldPrefix)
      }

      if (!this.hasError) {
        this.errorOnLoad = false
        this.erroringFieldName = null
      }
    },
    getOutsideLawTotalErrorMessage(fieldSuffix) {
      const outsideLaw = Constants.TeledeclarationCharacteristicGroups.outsideLaw
      const fields = outsideLaw.fields.filter((field) => field.endsWith(fieldSuffix))
      const total = this.sum(fields)
      if (total > this.payload.valueTotalHt) {
        const char = getCharacteristicFromFieldSuffix(fieldSuffix, outsideLaw)
        return this.errorMessage(total, this.payload.valueTotalHt, 1, undefined, char.text)
      }
    },
    fieldUpdate(fieldName) {
      if (this.diagnostic[fieldName] === this.payload[fieldName]) return
      this.checkTotal()
      this.populateSimplifiedDiagnostic()
    },
    sum(fields) {
      const sum = fields.reduce((acc, field) => acc + (this.payload[field] || 0), 0)
      return +sum.toFixed(2)
    },
    fieldHasError(fieldName) {
      if (fieldName.startsWith(this.meatFieldPrefix) && !!this.meatTotalErrorMessage) return true
      if (fieldName.startsWith(this.fishFieldPrefix) && !!this.fishTotalErrorMessage) return true
      return !!this.payload[fieldName] && (this.errorOnLoad || this.hasTotalError)
    },
    errorMessage(problemValue, totalValue, stepNumber, familyFieldPrefix, characteristicText) {
      // family can be undefined
      const familyTextChoices = {
        [this.fishFieldPrefix]: "des produits aquatiques ",
        [this.meatFieldPrefix]: "des viandes et volailles ",
      }
      let familyText = familyTextChoices[familyFieldPrefix] || ""
      const stepTextChoices = {
        1: "dans la première étape ",
        3: "dans la troisième étape ",
      }
      const stepText = stepTextChoices[stepNumber] || ""
      problemValue = toCurrency(problemValue)
      totalValue = toCurrency(totalValue)
      if (characteristicText) {
        characteristicText = `« ${characteristicText} » `
        return `Le total ${familyText}${characteristicText}(${problemValue}) excède le total ${familyText}saisi ${stepText}(${totalValue})`
      }
      return `Les montants détaillés ${familyText}(${problemValue}) excédent le total ${familyText}saisi ${stepText}(${totalValue})`
    },
    validFamily(id) {
      return this.possibleFamilies.indexOf(id) > -1
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
