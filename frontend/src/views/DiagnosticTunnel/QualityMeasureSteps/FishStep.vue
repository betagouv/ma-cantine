<template>
  <div>
    <FormErrorCallout v-if="hasError" :errorMessages="errorMessages" />
    <v-row>
      <v-col cols="12" md="4">
        <!-- Fish -->
        <label for="fish">
          Total (en € HT) de mes achats en poissons, produits de la mer et de l'aquaculture
          <span class="fr-hint-text mt-2">Optionnel</span>
        </label>
        <DsfrCurrencyField
          id="fish"
          v-model.number="payload.valueFishHt"
          :error="hasError"
          @blur="updatePayload"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueFishHt"
          @autofill="updatePayload"
          purchaseType="totaux de poissons, produits de la mer et de l'aquaculture"
          :amount="purchasesSummary.valueFishHt"
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
            <!-- Fish EGalim -->
            <div class="d-block d-sm-flex align-center">
              <v-icon v-if="$vuetify.breakpoint.smAndDown" size="30" color="#4d4db2" class="mr-2">$award-line</v-icon>
              <label for="fish-egalim">
                Total (en € HT) de mes achats EGalim en poissons, produits de la mer et de l'aquaculture
                <span class="fr-hint-text mt-2">Optionnel</span>
              </label>
            </div>
            <DsfrCurrencyField
              id="fish-egalim"
              v-model.number="payload.valueFishEgalimHt"
              :error="fishError"
              @blur="updatePayload"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            />
            <PurchaseHint
              v-if="displayPurchaseHints"
              v-model="payload.valueFishEgalimHt"
              @autofill="updatePayload"
              purchaseType="poissons, produits de la mer et de l'aquaculture EGalim"
              :amount="purchasesSummary.valueFishEgalimHt"
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
            <!-- Fish France -->
            <div class="d-block d-sm-flex align-center">
              <v-icon v-if="$vuetify.breakpoint.smAndDown" size="30" color="#4d4db2" class="mr-2">$france-line</v-icon>
              <label for="fish-france">
                Total (en € HT) de mes achats origine France en poissons, produits de la mer et de l'aquaculture
                <span class="fr-hint-text mt-2">Optionnel</span>
              </label>
            </div>
            <DsfrCurrencyField
              id="fish-france"
              v-model.number="payload.valueProduitsDeLaMerFrance"
              :error="fishError"
              @blur="updatePayload"
              :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
            />
            <PurchaseHint
              v-if="displayPurchaseHints"
              v-model="payload.valueProduitsDeLaMerFrance"
              @autofill="updatePayload"
              purchaseType="poissons, produits de la mer et de l'aquaculture origine France"
              :amount="purchasesSummary.valueProduitsDeLaMerFrance"
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
      fishTotalErrorMessage: null,
      fishErrorMessage: null,
      totalFamiliesErrorMessage: null,
      errorHelperUsed: false,
      errorHelperFields: [],
    }
  },
  computed: {
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    fishError() {
      return !!this.fishErrorMessage
    },
    totalFishError() {
      return !!this.fishTotalErrorMessage
    },
    totalFamiliesError() {
      return !!this.totalFamiliesErrorMessage
    },
    hasError() {
      return [this.totalFishError, this.fishError, this.totalFamiliesError].some((x) => !!x)
    },
    errorMessages() {
      return [this.fishTotalErrorMessage, this.fishErrorMessage, this.totalFamiliesErrorMessage].filter((x) => !!x)
    },
    erroringFields() {
      const fields = []
      if (this.totalFishError) fields.push("valueTotalHt")
      if (this.totalFamiliesError) fields.push(...["valueTotalHt", "valueMeatPoultryHt"])
      return fields
    },
  },
  methods: {
    updatePayload() {
      this.checkTotal()
      if (!this.hasError) this.$emit("update-payload", { payload: this.payload })
    },
    checkTotal() {
      this.fishTotalErrorMessage = null
      this.fishErrorMessage = null
      this.totalFamiliesErrorMessage = null

      const d = this.payload
      const sumFish = d.valueFishEgalimHt
      const total = d.valueTotalHt
      const totalFish = d.valueFishHt
      const totalMeatPoultry = d.valueMeatPoultryHt
      const totalFamilies = totalMeatPoultry + totalFish

      if (totalFish > total) {
        this.fishTotalErrorMessage = `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
          totalFish
        )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
        this.errorHelperFields.push("valueTotalHt")
      } else if (totalFamilies > total) {
        this.totalFamiliesErrorMessage = `Les totaux des achats « viandes et volailles » et « poissons, produits de la mer et de l'aquaculture » ensemble (${toCurrency(
          totalFamilies
        )}) ne doit pas dépasser le total de tous les achats (${toCurrency(total)})`
        this.errorHelperFields.push(...["valueTotalHt", "valueMeatPoultryHt"])
      }
      if (sumFish > totalFish) {
        this.fishErrorMessage = `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
          totalFish
        )}) doit être supérieur à la somme des valeurs par label (${toCurrency(sumFish)})`
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
