<template>
  <div>
    <pre>{{ purchasesSummary }}</pre>
  </div>
</template>

<script>
// import DsfrCurrencyField from "@/components/DsfrCurrencyField"
// import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
// import ErrorHelper from "./ErrorHelper"
// import FormErrorCallout from "@/components/FormErrorCallout"
import { toCurrency } from "@/utils"

export default {
  name: "FishStep",
  // components: { DsfrCurrencyField, PurchaseHint, ErrorHelper, FormErrorCallout },
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
