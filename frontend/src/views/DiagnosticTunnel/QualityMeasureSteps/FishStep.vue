<template>
  <div>
    <FormErrorCallout v-if="hasError" :errorMessages="errorMessages" />
    <v-row>
      <v-col cols="12" md="4">
        <!-- Fish -->
        <label for="valeurProduitsDeLaMer">
          Total (en € HT) de mes achats en poissons, produits de la mer et de l'aquaculture
          <span class="fr-hint-text mt-2">Optionnel</span>
        </label>
        <DsfrCurrencyField
          id="valeurProduitsDeLaMer"
          v-model.number="payload.valeurProduitsDeLaMer"
          :error="hasError"
          @blur="updatePayload"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valeurProduitsDeLaMer"
          @autofill="updatePayload"
          purchaseType="totaux de poissons, produits de la mer et de l'aquaculture"
          :amount="purchasesSummary.valeurProduitsDeLaMer"
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
            <!-- produitsDeLaMer EGalim -->
            <div class="d-block d-sm-flex align-center">
              <v-icon v-if="$vuetify.breakpoint.smAndDown" size="30" color="#4d4db2" class="mr-2">$award-line</v-icon>
              <label for="valeurProduitsDeLaMerEgalim">
                Total (en € HT) de mes achats EGalim en poissons, produits de la mer et de l'aquaculture
                <span class="fr-hint-text mt-2">Optionnel</span>
              </label>
            </div>
            <DsfrCurrencyField
              id="valeurProduitsDeLaMerEgalim"
              v-model.number="payload.valeurProduitsDeLaMerEgalim"
              :error="produitsDeLaMerError"
              @blur="updatePayload"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            />
            <PurchaseHint
              v-if="displayPurchaseHints"
              v-model="payload.valeurProduitsDeLaMerEgalim"
              @autofill="updatePayload"
              purchaseType="poissons, produits de la mer et de l'aquaculture EGalim"
              :amount="purchasesSummary.valeurProduitsDeLaMerEgalim"
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
            <!-- produitsDeLaMer France -->
            <div class="d-block d-sm-flex align-center">
              <v-icon v-if="$vuetify.breakpoint.smAndDown" size="30" color="#4d4db2" class="mr-2">$france-line</v-icon>
              <label for="valeurProduitsDeLaMerFrance">
                Total (en € HT) de mes achats origine France en poissons, produits de la mer et de l'aquaculture
                <span class="fr-hint-text mt-2">Optionnel</span>
              </label>
            </div>
            <DsfrCurrencyField
              id="valeurProduitsDeLaMerFrance"
              v-model.number="payload.valeurProduitsDeLaMerFrance"
              :error="produitsDeLaMerError"
              @blur="updatePayload"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            />
            <PurchaseHint
              v-if="displayPurchaseHints"
              v-model="payload.valeurProduitsDeLaMerFrance"
              @autofill="updatePayload"
              purchaseType="poissons, produits de la mer et de l'aquaculture origine France"
              :amount="purchasesSummary.valeurProduitsDeLaMerFrance"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
            />
          </v-col>
        </v-row>
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
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import ErrorHelper from "./ErrorHelper"
import FormErrorCallout from "@/components/FormErrorCallout"
import { toCurrency } from "@/utils"

export default {
  name: "FishStep",
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
      produitsDeLaMerTotalErrorMessage: null,
      produitsDeLaMerErrorMessage: null,
      totalFamiliesErrorMessage: null,
      errorHelperUsed: false,
      errorHelperFields: [],
    }
  },
  computed: {
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    produitsDeLaMerError() {
      return !!this.produitsDeLaMerErrorMessage
    },
    totalProduitsDeLaMerError() {
      return !!this.produitsDeLaMerTotalErrorMessage
    },
    totalFamiliesError() {
      return !!this.totalFamiliesErrorMessage
    },
    hasError() {
      return [this.totalProduitsDeLaMerError, this.produitsDeLaMerError, this.totalFamiliesError].some((x) => !!x)
    },
    errorMessages() {
      return [
        this.produitsDeLaMerTotalErrorMessage,
        this.produitsDeLaMerErrorMessage,
        this.totalFamiliesErrorMessage,
      ].filter((x) => !!x)
    },
    erroringFields() {
      const fields = []
      if (this.totalProduitsDeLaMerError) fields.push("valeurTotale")
      if (this.totalFamiliesError) fields.push(...["valeurTotale", "valeurViandesVolailles"])
      return fields
    },
  },
  methods: {
    updatePayload() {
      this.checkTotal()
      if (!this.hasError) this.$emit("update-payload", { payload: this.payload })
    },
    checkTotal() {
      this.produitsDeLaMerTotalErrorMessage = null
      this.produitsDeLaMerErrorMessage = null
      this.totalFamiliesErrorMessage = null

      const d = this.payload
      const total = d.valeurTotale
      const totalFish = d.valeurProduitsDeLaMer
      const totalMeatPoultry = d.valeurViandesVolailles
      const totalFamilies = totalMeatPoultry + totalFish

      if (totalFish > total) {
        this.produitsDeLaMerTotalErrorMessage = `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
          totalFish
        )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
        this.errorHelperFields.push("valeurTotale")
      } else if (totalFamilies > total) {
        this.totalFamiliesErrorMessage = `Les totaux des achats « viandes et volailles » et « poissons, produits de la mer et de l'aquaculture » ensemble (${toCurrency(
          totalFamilies
        )}) ne doit pas dépasser le total de tous les achats (${toCurrency(total)})`
        this.errorHelperFields.push(...["valeurTotale", "valeurViandesVolailles"])
      }
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
