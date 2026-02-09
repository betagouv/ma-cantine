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
          {{ getFamilyText(family) }}
          <span v-if="isOptionnalField(fId)" class="fr-hint-text mt-2">Optionnel</span>
        </label>
        <div v-if="validFamily(fId)">
          <DsfrCurrencyField
            :id="fId"
            :rules="getValidatorsRules(fId)"
            @blur="fieldUpdate()"
            solo
            v-model.number="payload[diagnosticKey(fId)]"
            validate
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
            @autofill="fieldUpdate()"
          />
          <v-row v-if="characteristicId === 'BIO'" class="my-0 my-md-6">
            <v-col cols="1" class="pt-0 d-flex align-top justify-end">
              <div class="input-child-icon"></div>
            </v-col>
            <v-col cols="11">
              <label class="ml-4 ml-md-0" for="valeurBioDontCommerceEquitable">
                Dont Bio et Commerce équitable
                <span class="fr-hint-text my-2">Optionnel</span>
              </label>
              <DsfrCurrencyField
                :id="`${fId}_DONT_COMMERCE_EQUITABLE`"
                :rules="[validators.decimalPlaces(2), validators.lteOrEmpty(payload[diagnosticKey(fId)])]"
                @blur="fieldUpdate()"
                v-model.number="payload[diagnosticKey(fId, '_DONT_COMMERCE_EQUITABLE')]"
                validate-on-blur
                class="mt-2"
                :error="fieldHasError(diagnosticKey(fId, '_DONT_COMMERCE_EQUITABLE'))"
              />
              <PurchaseHint
                v-if="displayPurchaseHints && validFamily(fId)"
                v-model="payload[diagnosticKey(fId, '_DONT_COMMERCE_EQUITABLE')]"
                :purchaseType="family.shortText + ' dont commerce équitable pour cette caractéristique'"
                :amount="purchasesSummary[diagnosticKey(fId, '_DONT_COMMERCE_EQUITABLE')]"
                @autofill="fieldUpdate()"
              />
            </v-col>
          </v-row>
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
      viandesVolaillesTotalErrorMessage: null,
      produitsDeLaMerTotalErrorMessage: null,
      viandesVolaillesFieldPrefix: "valeurViandesVolailles",
      produitsDeLaMerFieldPrefix: "valeurProduitsDeLaMer",
      requiredCategories: ["bio", "egalim"],
      exceptionCaracteristics: ["EXTERNALITES", "PERFORMANCE"],
      exceptionFields: ["valueProduitsDeLaMerPecheDurable"],
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
        !!this.viandesVolaillesTotalErrorMessage ||
        !!this.produitsDeLaMerTotalErrorMessage
      )
    },
    hasTotalError() {
      return !!this.fieldTotalErrorMessage || !!this.outsideLawErrorMessages.length
    },
    errorMessages() {
      return [
        this.fieldTotalErrorMessage,
        ...this.outsideLawErrorMessages,
        this.viandesVolaillesTotalErrorMessage,
        this.produitsDeLaMerTotalErrorMessage,
      ].filter((x) => !!x)
    },
    possibleFamilies() {
      const exceptions = Constants.CharacteristicFamilyExceptions[this.characteristicId] || []
      return Object.keys(this.families).filter((id) => exceptions.indexOf(id) === -1)
    },
  },
  methods: {
    getValidatorsRules(fId) {
      const rules = []
      // Champ non applicable
      if (!this.validFamily(fId)) return rules
      rules.push(this.validators.nonNegativeOrEmpty)
      rules.push(this.validators.decimalPlaces(2))
      rules.push(this.validators.lteOrEmpty(this.payload.valeurTotale))
      // Obligatoire
      const isOptionnalField = this.isOptionnalField(fId)
      if (!isOptionnalField) rules.push(this.validators.required)
      // Sous-catégories origine France : groupId : "valeurAutresCircuitCourt" "valeurAutresLocal"
      const franceSubcategoryGroupIDd = ["CIRCUIT_COURT", "LOCAL"]
      if (franceSubcategoryGroupIDd.includes(this.characteristicId)) {
        const franceKeyName = this.camelize(`valeur_${fId}_france`)
        rules.push(
          this.validators.lteOrEmpty(
            this.payload[franceKeyName],
            "€ le total renseigné dans cette catégorie pour les achats origine France"
          )
        )
      }
      return rules
    },
    isOptionnalField(fId) {
      const isRequiredCategory = this.requiredCategories.includes(this.groupId)
      const isExceptionFields = this.exceptionFields.includes(this.diagnosticKey(fId))
      const isExceptionCaracteristic = this.exceptionCaracteristics.includes(this.characteristicId)
      return !isRequiredCategory || isExceptionFields || isExceptionCaracteristic
    },
    diagnosticKey(family, extra) {
      let keyName = `valeur_${family}_${this.characteristicId}`
      if (extra) keyName += extra.toLowerCase()
      return this.camelize(keyName)
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
      const {
        bioTotal,
        bioDontCommerceEquitableTotal,
        siqoTotal,
        externalitesPerformanceTotal,
        egalimAutresTotal,
      } = approTotals(this.payload)
      this.payload.valeurBio = bioTotal
      this.payload.valeurBioDontCommerceEquitable = bioDontCommerceEquitableTotal
      this.payload.valeurSiqo = siqoTotal
      this.payload.valeurExternalitesPerformance = externalitesPerformanceTotal
      this.payload.valeurEgalimAutres = egalimAutresTotal

      const { viandesVolaillesEgalim, viandesVolaillesFrance } = this.viandesVolaillesTotals()
      this.payload.valeurViandesVolaillesEgalim = viandesVolaillesEgalim
      this.payload.valeurViandesVolaillesFrance = viandesVolaillesFrance

      const { produitsDeLaMerEgalim } = this.produitsDeLaMerTotals()
      this.payload.valeurProduitsDeLaMerEgalim = produitsDeLaMerEgalim
    },
    viandesVolaillesTotals() {
      const egalimFields = Constants.TeledeclarationCharacteristicGroups.egalim.fields.filter(
        (name) => name.indexOf("BioDontCommerceEquitable") === -1
      )
      const outsideLawFields = Constants.TeledeclarationCharacteristicGroups.outsideLaw.fields
      const allFields = egalimFields.concat(outsideLawFields)

      let viandesVolaillesEgalim = 0
      let viandesVolaillesFrance = 0

      allFields.forEach((field) => {
        const isViandesVolailles = field.startsWith(this.viandesVolaillesFieldPrefix)
        const value = parseFloat(this.payload[field])
        if (!isViandesVolailles || !value) return
        const isEgalim = egalimFields.includes(field)

        // Note that it can be both egalim and provenance France
        if (isEgalim) viandesVolaillesEgalim += value
        if (field.endsWith("France")) viandesVolaillesFrance = value // only one France meat field
      })
      viandesVolaillesEgalim = +viandesVolaillesEgalim.toFixed(2)
      viandesVolaillesFrance = +viandesVolaillesFrance.toFixed(2)
      return { viandesVolaillesEgalim, viandesVolaillesFrance }
    },
    produitsDeLaMerTotals() {
      let produitsDeLaMerEgalim = 0

      const egalimFields = Constants.TeledeclarationCharacteristicGroups.egalim.fields.filter(
        (name) => name.indexOf("BioDontCommerceEquitable") === -1
      )

      egalimFields.forEach((field) => {
        const isProduitsDeLaMer = field.startsWith(this.produitsDeLaMerFieldPrefix)
        const value = parseFloat(this.payload[field])
        if (!isProduitsDeLaMer || !value) return
        produitsDeLaMerEgalim += value
      })
      produitsDeLaMerEgalim = +produitsDeLaMerEgalim.toFixed(2)
      return { produitsDeLaMerEgalim }
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
      this.viandesVolaillesTotalErrorMessage = null
      this.produitsDeLaMerTotalErrorMessage = null
      this.outsideLawErrorMessages = []

      const groups = Constants.TeledeclarationCharacteristicGroups
      const groupsWithoutCommerceEquitable = groups.egalim.fields.filter(
        (name) => name.indexOf("BioDontCommerceEquitable") === -1
      )
      const sumFields = groupsWithoutCommerceEquitable.concat(groups.nonEgalim.fields)
      const declaredTotal = +this.payload.valeurTotale
      const fieldTotal = this.sum(sumFields)
      if (fieldTotal > declaredTotal) {
        this.fieldTotalErrorMessage = this.errorMessage(fieldTotal, declaredTotal, 1)
      }
      const outsideLawSuffix = {
        FRANCE: "France",
        CIRCUIT_COURT: "CircuitCourt",
        LOCAL: "Local",
      }[this.characteristicId]

      if (outsideLawSuffix) {
        // in the outsideLaw group, a product can be counted in more than one category, so we check if any of the
        // totals for each of the three categories is greater than the main total
        const totalErrorMessage = this.getOutsideLawTotalErrorMessage(outsideLawSuffix)
        if (totalErrorMessage) this.outsideLawErrorMessages.push(totalErrorMessage)

        const char = getCharacteristicFromFieldSuffix(outsideLawSuffix, groups.outsideLaw)

        const viandesVolaillesFieldName = this.viandesVolaillesFieldPrefix + outsideLawSuffix
        const viandesVolaillesOutsideLaw = this.payload[viandesVolaillesFieldName]
        const viandesVolaillesTotal = this.payload.valeurViandesVolailles
        if (viandesVolaillesOutsideLaw > viandesVolaillesTotal) {
          const message = this.errorMessage(
            viandesVolaillesOutsideLaw,
            viandesVolaillesTotal,
            3,
            this.viandesVolaillesFieldPrefix,
            char.text
          )
          this.outsideLawErrorMessages.push(message)
        }

        const produitsDeLaMerFieldName = this.produitsDeLaMerFieldPrefix + outsideLawSuffix
        const produitsDeLaMerOutsideLaw = this.payload[produitsDeLaMerFieldName]
        const produitsDeLaMerTotal = this.payload.valeurProduitsDeLaMer
        if (produitsDeLaMerOutsideLaw > produitsDeLaMerTotal) {
          const message = this.errorMessage(
            produitsDeLaMerOutsideLaw,
            produitsDeLaMerTotal,
            3,
            this.produitsDeLaMerFieldPrefix,
            char.text
          )
          this.outsideLawErrorMessages.push(message)
        }
      }

      // check meat and fish totals
      const { viandesVolaillesEgalim } = this.viandesVolaillesTotals()
      const nonEgalimMeat = this.payload.valeurViandesVolaillesNonEgalim
        ? Number(this.payload.valeurViandesVolaillesNonEgalim.toFixed(2))
        : 0
      const sumMeat = viandesVolaillesEgalim + nonEgalimMeat
      const totalMeat = this.payload.valeurViandesVolailles
      if (sumMeat > totalMeat) {
        this.viandesVolaillesTotalErrorMessage = this.errorMessage(
          sumMeat,
          totalMeat,
          3,
          this.viandesVolaillesFieldPrefix
        )
      }
      const { produitsDeLaMerEgalim } = this.produitsDeLaMerTotals()
      const nonEgalimFish = this.payload.valeurProduitsDeLaMerNonEgalim
        ? Number(this.payload.valeurProduitsDeLaMerNonEgalim.toFixed(2))
        : 0
      const sumFish = produitsDeLaMerEgalim + nonEgalimFish
      const totalFish = this.payload.valeurProduitsDeLaMer
      if (sumFish > totalFish) {
        this.produitsDeLaMerTotalErrorMessage = this.errorMessage(
          sumFish,
          totalFish,
          3,
          this.produitsDeLaMerFieldPrefix
        )
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
      if (total > this.payload.valeurTotale) {
        const char = getCharacteristicFromFieldSuffix(fieldSuffix, outsideLaw)
        return this.errorMessage(total, this.payload.valeurTotale, 1, undefined, char.text)
      }
    },
    fieldUpdate() {
      this.checkTotal()
      this.populateSimplifiedDiagnostic()
    },
    sum(fields) {
      const sum = fields.reduce((acc, field) => acc + (this.payload[field] || 0), 0)
      return +sum.toFixed(2)
    },
    fieldHasError(fieldName) {
      if (fieldName.startsWith(this.viandesVolaillesFieldPrefix) && !!this.viandesVolaillesTotalErrorMessage)
        return true
      if (fieldName.startsWith(this.produitsDeLaMerFieldPrefix) && !!this.produitsDeLaMerTotalErrorMessage) return true
      return !!this.payload[fieldName] && (this.errorOnLoad || this.hasTotalError)
    },
    errorMessage(problemValue, totalValue, stepNumber, familyFieldPrefix, characteristicText) {
      // family can be undefined
      const familyTextChoices = {
        [this.produitsDeLaMerFieldPrefix]: "des produits aquatiques ",
        [this.viandesVolaillesFieldPrefix]: "des viandes et volailles ",
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
    getFamilyText(family) {
      let familyText = family.text
      if (this.characteristicId === "COMMERCE_EQUITABLE") familyText += " (hors bio)"
      return familyText
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

<style scoped lang="scss">
@import "../../../scss/common.scss";
</style>
