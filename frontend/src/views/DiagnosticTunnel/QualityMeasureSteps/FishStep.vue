<template>
  <div>
    <div v-if="hasError">
      <DsfrCallout v-for="message in errorMessages" :key="message" color="red lighten-1">
        <p class="ma-0">{{ message }}</p>
      </DsfrCallout>
    </div>
    <v-row>
      <v-col cols="12" md="8">
        <!-- Poissons -->
        <div class="d-block d-sm-flex align-center">
          <div class="d-flex">
            <v-icon size="30" color="blue">
              mdi-fish
            </v-icon>
          </div>
          <label class="body-2 ml-4" :for="'fish-' + diagnostic.year">
            La valeur (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture total
          </label>
        </div>
        <DsfrCurrencyField
          :id="'fish-' + diagnostic.year"
          v-model.number="payload.valueFishHt"
          :error="fishError || totalFishError"
          @blur="checkTotal"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueFishHt"
          @autofill="checkTotal"
          purchaseType="totaux de poissons, produits de la mer et de l'aquaculture"
          :amount="purchasesSummary.valueFishHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />

        <!-- Poissons EGALIM -->
        <div class="d-block d-sm-flex align-center mt-8">
          <div class="d-flex">
            <v-icon size="30" color="green">
              $checkbox-circle-fill
            </v-icon>
            <v-icon size="30" color="blue">
              mdi-fish
            </v-icon>
          </div>
          <label class="body-2 ml-4" :for="'fish-egalim-' + diagnostic.year">
            La valeur (en HT) des mes achats EGAlim en poissons, produits de la mer et de l'aquaculture
          </label>
        </div>
        <DsfrCurrencyField
          :id="'fish-egalim-' + diagnostic.year"
          v-model.number="payload.valueFishEgalimHt"
          :error="fishError"
          @blur="checkTotal"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueFishEgalimHt"
          @autofill="checkTotal"
          purchaseType="poissons, produits de la mer et de l'aquaculture EGAlim"
          :amount="purchasesSummary.valueFishEgalimHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </v-col>
    </v-row>
    <ErrorHelper
      class="mt-8"
      :showFields="['valueTotalHt']"
      v-if="totalFishError"
      :diagnostic="payload"
      @check-total="checkTotal"
    />
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import ErrorHelper from "./ErrorHelper.vue"
import DsfrCallout from "@/components/DsfrCallout"
import { toCurrency } from "@/utils"

export default {
  name: "FishStep",
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
      fishError: false,
      totalFishError: false,
      fishTotalErrorMessage: null,
      fishErrorMessage: null,
    }
  },
  computed: {
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
    },
    hasError() {
      return [this.totalFishError, this.fishError].some((x) => !!x)
    },
    errorMessages() {
      return [this.fishTotalErrorMessage, this.fishErrorMessage].filter((x) => !!x)
    },
  },
  methods: {
    updatePayload() {
      this.checkTotal()
      if (!this.hasError) this.$emit("update-payload", { payload: this.payload })
    },
    checkTotal() {
      const d = this.payload
      const sumFish = d.valueFishEgalimHt
      const total = d.valueTotalHt
      const totalFish = d.valueFishHt

      this.totalFishError = totalFish > total
      this.fishError = sumFish > totalFish

      if (this.totalFishError) {
        this.fishTotalErrorMessage = `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
          totalFish
        )}) ne peut pas excéder le total des achats (${toCurrency(total)})`
      } else this.fishTotalErrorMessage = null

      if (this.fishError) {
        this.fishErrorMessage = `Le total des achats viandes et volailles (${toCurrency(
          totalFish
        )}) doit être supérieur à la somme des valeurs par label (${toCurrency(sumFish)})`
      } else this.fishErrorMessage = null

      return [this.totalFishError, this.fishError].every((x) => !x)
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
}
</script>

<style scoped>
.left-border {
  border-left: solid #4d4db2;
}
</style>
