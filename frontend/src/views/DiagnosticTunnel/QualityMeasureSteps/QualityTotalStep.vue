<template>
  <div>
    <div class="mb-16" v-if="displayPurchaseHints && purchasesSummary.valeurTotale > 0">
      <DsfrCallout icon="$money-euro-box-fill">
        <div>
          <p>
            Vous avez renseigné un total de
            <span class="font-weight-bold">{{ toCurrency(purchasesSummary.valeurTotale) }}</span>
            d'achats en {{ diagnostic.year }}. Voulez-vous compléter votre bilan avec les montants de ces achats ?
          </p>
          <v-btn outlined color="primary" @click="autofillWithPurchases">Compléter avec mes achats</v-btn>
        </div>
      </DsfrCallout>
    </div>
    <FormErrorCallout v-if="hasError" :errorMessages="errorMessages" />
    <DsfrCurrencyField
      v-model.number="payload.valeurTotale"
      :rules="[validators.greaterThanZero, validators.decimalPlaces(2)]"
      validate-on-blur
      @blur="updatePayload"
      :error="hasError"
      label="Total (en € HT) de tous mes achats alimentaires"
      ref="totalField"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="payload.valeurTotale"
      @autofill="onPurchaseAutofill"
      purchaseType=""
      :amount="purchasesSummary.valeurTotale"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />
    <ErrorHelper
      v-if="hasError || errorHelperUsed"
      class="mt-8"
      :showFields="errorHelperFields"
      :errorFields="erroringFields"
      :diagnostic="payload"
      @field-update="errorUpdate"
      :purchasesSummary="purchasesSummary"
    />
    <DsfrHighlight v-if="displayMealPrice" class="mt-8 ml-0">
      <p>
        <strong>
          Coût repas estimé {{ mealPrice }} € = {{ payload.valeurTotale }} €HT / {{ canteen.yearlyMealCount }} repas
          annuel
        </strong>
      </p>
      <p class="mb-0">
        La fourchette en restauration collective est comprise entre 0,50 € et 20 €.
        <br />
        Le nombre de repas annuels renseigné est incorrect ?
        <button class="text-decoration-underline fr-link" @click="modifyYearlyMealCount">
          Cliquez-ici pour le modifier
        </button>
      </p>
      <p>
        Besoin d'aide pour calculer le nombre de couverts annuels ?
        <a
          class="text-decoration-underline fr-link"
          style="color: inherit"
          :href="documentation.calculerNombreCouverts"
          target="_blank"
        >
          Consultez notre documentation
        </a>
      </p>
      <p v-if="mealPriceError" class="color-warning">
        <v-icon class="color-warning">$error-warning-line</v-icon>
        Attention, donnée potentiellement aberrante : le coût estimé semble incohérent
      </p>
    </DsfrHighlight>
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import DsfrHighlight from "@/components/DsfrHighlight"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import ErrorHelper from "./ErrorHelper"
import FormErrorCallout from "@/components/FormErrorCallout"
import DsfrCallout from "@/components/DsfrCallout"
import { toCurrency } from "@/utils"
import validators from "@/validators"
import Constants from "@/constants"
import documentation from "../../../../../2024-frontend/src/data/documentation.json"

const DEFAULT_TOTAL_ERROR = "Le total doit être plus que la somme des valeurs par label"

export default {
  name: "QualityTotalStep",
  components: { DsfrCurrencyField, DsfrHighlight, PurchaseHint, ErrorHelper, FormErrorCallout, DsfrCallout },
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
    canteen: {
      type: Object,
    },
  },
  data() {
    return {
      totalErrorMessage: null,
      viandesVolaillesErrorMessage: null,
      produitsDeLaMerErrorMessage: null,
      totalFamiliesErrorMessage: null,
      errorHelperUsed: false,
      errorHelperFields: [],
      minCostPerMealExpected: 0.5,
      maxCostPerMealExpected: 20,
      documentation: documentation,
    }
  },
  computed: {
    displayMealPrice() {
      return this.payload.valeurTotale && this.payload.valeurTotale !== null && this.canteen.yearlyMealCount !== null
    },
    mealPrice() {
      return Number(this.payload.valeurTotale / this.canteen.yearlyMealCount).toFixed(2)
    },
    mealPriceError() {
      return this.mealPrice < this.minCostPerMealExpected || this.mealPrice > this.maxCostPerMealExpected
    },
    validators() {
      return validators
    },
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    totalViandesVolaillesError() {
      return !!this.totalViandesVolaillesErrorMessage
    },
    totalProduitsDeLaMerError() {
      return !!this.totalProduitsDeLaMerErrorMessage
    },
    totalError() {
      return !!this.totalErrorMessage
    },
    totalFamiliesError() {
      return !!this.totalFamiliesErrorMessage
    },
    errorMessages() {
      return [
        this.totalErrorMessage,
        this.viandesVolaillesErrorMessage,
        this.produitsDeLaMerErrorMessage,
        this.totalFamiliesErrorMessage,
      ].filter((x) => !!x)
    },
    hasError() {
      return [
        this.totalViandesVolaillesError,
        this.totalProduitsDeLaMerError,
        this.totalError,
        this.totalFamiliesError,
      ].some((x) => !!x)
    },
    erroringFields() {
      const fields = []
      if (this.totalError)
        fields.push(...["valeurBio", "valeurSiqo", "valeurEgalimAutres", "valeurExternalitesPerformance"])
      if (this.totalViandesVolaillesError) fields.push("valeurViandesVolailles")
      if (this.totalProduitsDeLaMerError) fields.push("valeurProduitsDeLaMer")
      if (this.totalFamiliesError) fields.push(...["valeurViandesVolailles", "valeurProduitsDeLaMer"])
      return fields
    },
  },
  methods: {
    modifyYearlyMealCount() {
      const editPageName =
        this.canteen.productionType === "groupe"
          ? "GestionnaireCantineGroupeModifier"
          : "GestionnaireCantineRestaurantModifier"
      this.$emit("save-diagnostic-and-go-to-page", {
        payload: this.payload,
        nextPage: {
          name: editPageName,
          params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(this.canteen) },
          query: { redirection: this.$router.currentRoute.path },
        },
      })
    },
    updatePayload() {
      this.checkTotal()
      if (!this.hasError) this.$emit("update-payload", { payload: this.payload })
    },
    toCurrency,
    checkTotal() {
      if (this.payload.valeurTotale < 0) {
        return // this error is handled by vuetify validation
      }

      this.totalErrorMessage = null
      this.viandesVolaillesErrorMessage = null
      this.produitsDeLaMerErrorMessage = null
      this.totalFamiliesErrorMessage = null

      const d = this.payload
      const sumEgalim = this.sumAllEgalim()
      const total = d.valeurTotale
      const totalMeatPoultry = d.valeurViandesVolailles
      const totalFish = d.valeurProduitsDeLaMer
      const totalFamilies = totalMeatPoultry + totalFish

      if (sumEgalim > total) {
        this.totalErrorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${toCurrency(sumEgalim || 0)}`
        if (!this.diagnostic.diagnosticType || this.diagnostic.diagnosticType === "SIMPLE") {
          this.errorHelperFields.push(
            ...["valeurBio", "valeurSiqo", "valeurEgalimAutres", "valeurExternalitesPerformance"]
          )
        }
      }
      if (totalFamilies > total) {
        this.totalFamiliesErrorMessage = `Les totaux des achats « viandes et volailles » et « poissons, produits de la mer et de l'aquaculture » ensemble (${toCurrency(
          totalFamilies
        )}) ne doit pas dépasser le total de tous les achats (${toCurrency(total)})`
        this.errorHelperFields.push(...["valeurViandesVolailles", "valeurProduitsDeLaMer"])
      } else {
        if (totalMeatPoultry > total) {
          this.viandesVolaillesErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
            totalMeatPoultry
          )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
          this.errorHelperFields.push("valeurViandesVolailles")
        }
        if (totalFish > total) {
          this.produitsDeLaMerErrorMessage = `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
            totalFish
          )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
          this.errorHelperFields.push("valeurProduitsDeLaMer")
        }
      }
    },
    sumAllEgalim() {
      const d = this.payload
      const egalimValues = [d.valeurBio, d.valeurSiqo, d.valeurExternalitesPerformance, d.valeurEgalimAutres]
      let total = 0
      egalimValues.forEach((val) => {
        total += parseFloat(val) || 0
      })
      return total
    },
    errorUpdate() {
      this.errorHelperUsed = true
      this.checkTotal()
    },
    onPurchaseAutofill() {
      this.updatePayload()
      this.$nextTick(this.$refs.totalField.validate)
    },
    autofillWithPurchases() {
      const purchasesWithEmptyValue = this.replaceOptionnalValueWithEmpty(this.purchasesSummary)
      Object.assign(this.payload, { diagnosticType: "COMPLETE" }, purchasesWithEmptyValue)
      this.$emit("tunnel-autofill", {
        payload: this.payload,
        message: {
          status: "success",
          message: "Vos achats on été rapportés dans votre bilan.",
        },
      })
    },
    replaceOptionnalValueWithEmpty(purchases) {
      const nonEgalimFields = Constants.TeledeclarationCharacteristicGroups.nonEgalim.fields
      const outsideLawFields = Constants.TeledeclarationCharacteristicGroups.outsideLaw.fields
      const optionnalEgalimFields = Constants.TeledeclarationCharacteristicGroups.egalim.fields.filter(
        (field) => field.endsWith("Performance") || field.endsWith("Externalites")
      )
      const optionnalFields = [
        ...optionnalEgalimFields,
        ...nonEgalimFields,
        ...outsideLawFields,
        "valueProduitsDeLaMerPecheDurable",
      ]
      const purchasesKeys = Object.keys(purchases)
      const purchasesWithEmptyValue = {}
      purchasesKeys.map((key) => {
        const isOptionnal = optionnalFields.includes(key)
        const isEmpty = purchases[key] === 0
        const value = isOptionnal && isEmpty ? null : purchases[key]
        purchasesWithEmptyValue[key] = value
      })
      return purchasesWithEmptyValue
    },
  },
  mounted() {
    this.checkTotal()
  },
}
</script>

<style>
.color-warning {
  color: #fc5d00 !important;
}
</style>
