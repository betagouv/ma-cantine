<template>
  <div>
    <div v-if="hasError">
      <DsfrCallout v-for="message in errorMessages" :key="message" color="red lighten-1">
        <p class="ma-0">{{ message }}</p>
      </DsfrCallout>
    </div>
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
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="hasError"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryHt"
          @autofill="checkTotal"
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
          :error="meatPoultryError"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryEgalimHt"
          @autofill="checkTotal"
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
          :error="meatPoultryError"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryFranceHt"
          @autofill="checkTotal"
          purchaseType="viandes et volailles provenance France"
          :amount="purchasesSummary.valueMeatPoultryFranceHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </v-col>
    </v-row>
    <ErrorHelper
      class="mt-8"
      :showFields="errorHelperFields"
      :class="`${totalMeatPoultryError || totalFamiliesError ? '' : 'd-none'}`"
      :diagnostic="payload"
      @check-total="checkTotal"
      :purchasesSummary="purchasesSummary"
    />
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import ErrorHelper from "./ErrorHelper"
import DsfrCallout from "@/components/DsfrCallout"
import { toCurrency } from "@/utils"

export default {
  name: "MeatPoultryStep",
  components: { DsfrCurrencyField, PurchaseHint, ErrorHelper, DsfrCallout },
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
      meatPoultryErrorMessage: null,
      totalFamiliesErrorMessage: null,
    }
  },
  computed: {
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    totalMeatPoultryError() {
      return !!this.totalMeatPoultryErrorMessage
    },
    meatPoultryError() {
      return !!this.meatPoultryErrorMessage
    },
    totalFamiliesError() {
      return !!this.totalFamiliesErrorMessage
    },
    hasError() {
      return [this.totalMeatPoultryError, this.meatPoultryError, this.totalFamiliesError].some((x) => !!x)
    },
    errorMessages() {
      return [this.totalMeatPoultryErrorMessage, this.meatPoultryErrorMessage, this.totalFamiliesErrorMessage].filter(
        (x) => !!x
      )
    },
    errorHelperFields() {
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
      const d = this.payload
      // Note that we do Math.max because some meat-poultry may be overlapped : both bio and provenance France
      const sumMeatPoultry = Math.max(d.valueMeatPoultryEgalimHt, d.valueMeatPoultryFranceHt)
      const total = d.valueTotalHt
      const totalMeatPoultry = d.valueMeatPoultryHt
      const totalFish = d.valueFishHt
      const totalFamilies = totalMeatPoultry + totalFish

      if (totalMeatPoultry > total) {
        this.totalMeatPoultryErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
          totalMeatPoultry
        )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
      } else this.totalMeatPoultryErrorMessage = null
      if (sumMeatPoultry > totalMeatPoultry) {
        this.meatPoultryErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
          totalMeatPoultry
        )}) doit être supérieur à la somme des valeurs par label (${toCurrency(sumMeatPoultry)})`
      } else this.meatPoultryErrorMessage = null
      if (totalFamilies > total) {
        this.totalFamiliesErrorMessage = `Les totaux des achats « viandes et volailles » et « poissons, produits de la mer et de l'aquaculture » ensemble (${toCurrency(
          totalFamilies
        )}) ne doit pas dépasser le total de tous les achats (${toCurrency(total)})`
      } else this.totalFamiliesErrorMessage = null
    },
  },
  watch: {
    payload: {
      handler() {
        this.updatePayload()
      },
      deep: true,
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