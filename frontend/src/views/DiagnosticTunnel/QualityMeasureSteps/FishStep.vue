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
          <label class="body-2 ml-4" for="fish">
            La valeur (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture total
            <span class="fr-hint-text mt-2">Optionnel</span>
          </label>
        </div>
        <DsfrCurrencyField
          id="fish"
          v-model.number="payload.valueFishHt"
          :error="hasError"
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
          <label class="body-2 ml-4" for="fish-egalim">
            La valeur (en HT) des mes achats EGAlim en poissons, produits de la mer et de l'aquaculture
            <span class="fr-hint-text mt-2">Optionnel</span>
          </label>
        </div>
        <DsfrCurrencyField
          id="fish-egalim"
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
      :showFields="errorHelperFields"
      :class="`${totalFishError || totalFamiliesError ? '' : 'd-none'}`"
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
      fishTotalErrorMessage: null,
      fishErrorMessage: null,
      totalFamiliesErrorMessage: null,
    }
  },
  computed: {
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
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
    errorHelperFields() {
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
      } else this.fishTotalErrorMessage = null

      if (sumFish > totalFish) {
        this.fishErrorMessage = `Le total des achats poissons, produits de la mer et de l'aquaculture (${toCurrency(
          totalFish
        )}) doit être supérieur à la somme des valeurs par label (${toCurrency(sumFish)})`
      } else this.fishErrorMessage = null
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
