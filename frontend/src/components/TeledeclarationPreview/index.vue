<template>
  <v-dialog v-model="isOpen" max-width="900" :scrollable="false">
    <v-card ref="content">
      <!-- maybe make dialog fullscreen for xs (and s) ? -->
      <v-row align="center" class="pt-4 mx-0" v-if="diagnostics && diagnostics.length">
        <v-col cols="6" sm="8" md="9" class="pb-1">
          <v-progress-linear :value="(idx / diagnostics.length) * 100" rounded height="6"></v-progress-linear>
        </v-col>
        <v-col class="text-right pb-1">
          <p class="caption my-0">{{ idx }} / {{ diagnostics.length }} diagnostics télédéclarés</p>
        </v-col>
      </v-row>

      <v-card-title class="font-weight-bold">
        {{ "Télédéclaration : " + canteenForTD.name }}
      </v-card-title>
      <v-card-text class="text-left pb-0">
        Veuillez vérifier les données pour {{ diagnosticForTD.year }} ci-dessous.
      </v-card-text>
      <PreviewTable ref="table" :canteen="canteenForTD" :diagnostic="diagnosticForTD" />
      <div v-if="unusualData.length" class="text-left px-6">
        <p>Ces données sont-elles correctes ?</p>
        <ul>
          <li v-for="data in unusualData" :key="data.id" class="mb-4">{{ data.text }}</li>
        </ul>
      </div>
      <v-form ref="teledeclarationForm" v-model="teledeclarationFormIsValid" id="teledeclaration-form" class="px-6">
        <v-checkbox
          :rules="[validators.checked]"
          label="Je déclare sur l’honneur la véracité de mes informations"
          v-model="tdConfirmed"
        ></v-checkbox>
      </v-form>
      <v-card-actions class="d-flex pr-4 pb-4">
        <v-spacer></v-spacer>
        <v-btn :disabled="tdLoading" outlined color="primary" class="px-4" @click="close">Annuler</v-btn>
        <v-btn
          :disabled="tdLoading"
          outlined
          color="primary"
          class="ml-4 px-4"
          @click="goToEditing"
          v-if="!fromDiagPage"
        >
          Modifier
        </v-btn>
        <v-btn :disabled="tdLoading" color="primary" class="ml-4 px-4" @click="confirmTeledeclaration">
          Télédéclarer ces données
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import PreviewTable from "./PreviewTable"
import validators from "@/validators"

export default {
  components: { PreviewTable },
  props: {
    value: {
      required: true,
    },
    diagnostic: Object,
    canteen: Object,
    diagnostics: Array,
    tdLoading: Boolean,
    idx: Number,
  },
  data() {
    return {
      validators,
      tdConfirmed: false,
      teledeclarationFormIsValid: true,
      maxSatellitesExpected: 200,
      minCostPerMealExpected: 0.1,
      maxCostPerMealExpected: 10,
      minDaysOpenExpected: 50,
      maxDaysOpenExpected: 365,
    }
  },
  computed: {
    isOpen: {
      get() {
        return this.value && this.canteenForTD
      },
      set(newValue) {
        this.$emit("input", newValue)
      },
    },
    canteenForTD() {
      return this.canteen || this.diagnosticForTD?.canteen
    },
    diagnosticForTD() {
      if (this.diagnostics) return this.diagnostics[this.idx]
      return this.diagnostic
    },
    unusualData() {
      const unusualData = []
      if (this.isCentralCuisine) {
        if (this.canteenForTD.satelliteCanteensCount === 1) {
          unusualData.push({
            text: "Votre établissement livre des repas à un seul site",
            id: "td-satellite-count-is-1",
          })
        } else if (this.canteenForTD.satelliteCanteensCount > this.maxSatellitesExpected) {
          unusualData.push({
            text: `Votre établissement livre des repas à plus de ${this.maxSatellitesExpected} sites (${this.canteenForTD.satelliteCanteensCount} au total)`,
            id: `td-satellite-count-over-${this.maxSatellitesExpected}`,
            value: this.canteenForTD.satelliteCanteensCount,
          })
        }
      }
      if (this.showApproItems) {
        const text = `Votre cout denrées est estimé à ${this.costPerMeal} € par repas servi. S'il s'agit d'une erreur, veuillez modifier les données d'achat et/ou le nombre de repas par an.`
        if (this.costPerMeal > this.maxCostPerMealExpected) {
          unusualData.push({
            text,
            id: `td-meal-cost-over-${this.maxCostPerMealExpected}`,
            value: this.costPerMeal,
          })
        } else if (this.costPerMeal < this.minCostPerMealExpected) {
          unusualData.push({
            text,
            id: `td-meal-cost-under-${this.minCostPerMealExpected}`,
            value: this.costPerMeal,
          })
        }
      }
      if (this.daysOpenPerYear) {
        const text = `Vos jours de service sont estimés à ${this.daysOpenPerYear} par an. S'il s'agit d'une erreur, veuillez modifier les chiffres « nombre de repas par jour » et/ou « nombre de repas par an ».`
        if (this.daysOpenPerYear > this.maxDaysOpenExpected) {
          unusualData.push({
            text,
            id: `td-days-open-over-${this.maxDaysOpenExpected}`,
            value: this.daysOpenPerYear,
          })
        } else if (this.daysOpenPerYear < this.minDaysOpenExpected) {
          unusualData.push({
            text,
            id: `td-days-open-under-${this.minDaysOpenExpected}`,
            value: this.daysOpenPerYear,
          })
        }
      }
      return unusualData
    },
    fromDiagPage() {
      return this.$route.name === "DiagnosticModification"
    },
    canteenUrlComponent() {
      return this.canteenForTD ? this.$store.getters.getCanteenUrlComponent(this.canteenForTD) : null
    },
    showApproItems() {
      if (this.canteenForTD.productionType === "site_cooked_elsewhere" && this.centralKitchenDiagostic) {
        return (
          this.centralKitchenDiagostic.centralKitchenDiagnosticMode !== "APPRO" &&
          this.centralKitchenDiagostic.centralKitchenDiagnosticMode !== "ALL"
        )
      }
      return true
    },
    daysOpenPerYear() {
      if (!this.canteenForTD.dailyMealCount || !this.canteenForTD.yearlyMealCount) return
      // can't easily estimate days open for even central_serving without taking into account all satellites
      if (this.canteenForTD.isCentralCuisine) return
      return Number(this.canteenForTD.yearlyMealCount / this.canteenForTD.dailyMealCount).toFixed(0)
    },
    costPerMeal() {
      if (!this.showApproItems || !this.canteenForTD.yearlyMealCount) return
      return Number(this.diagnosticForTD.valueTotalHt / this.canteenForTD.yearlyMealCount).toFixed(2)
    },
    isCentralCuisine() {
      // cannot use this.canteen.isCentralCuisine because that field may not be updated with latest canteen changes
      return this.canteenForTD.productionType === "central" || this.canteenForTD.productionType === "central_serving"
    },
  },
  methods: {
    teledeclare() {
      this.$emit("teledeclare", this.diagnosticForTD, this.keepDialog)
    },
    keepDialog() {
      return !this.diagnostics || this.idx + 1 < this.diagnostics.length
    },
    close() {
      this.$emit("input", false)
    },
    goToEditing() {
      this.$emit("input", false)
      this.$router
        .push({
          name: "DiagnosticModification",
          params: { canteenUrlComponent: this.canteenUrlComponent, year: this.diagnosticForTD.year },
        })
        .catch(() => {})
    },
    calculateTableHeight() {
      if (!this.$refs || !this.$refs.table || !this.$refs.content) return
      const contentHeight = this.$refs.content.$el.offsetHeight
      const currentTableHeight = this.$refs.table.$el.offsetHeight
      const remainingItemsHeight = contentHeight - currentTableHeight

      // If not enough space (for example in a phone), everything must scroll
      if (remainingItemsHeight > contentHeight * 0.75) {
        this.$refs.table.$refs.innerTable.style.height = "auto"
        return
      }
      const innerTableHeight = this.$refs.table.$refs.innerSimpleTable.$el.offsetHeight + 4 // 4 is the padding value
      const calculatedHeight = Math.min(window.innerHeight * 0.9 - remainingItemsHeight, innerTableHeight)
      this.$refs.table.$refs.innerTable.style.height = `${parseInt(calculatedHeight)}px`
    },
    confirmTeledeclaration() {
      if (this.$refs["teledeclarationForm"]) {
        const teledeclarationFormIsValid = this.$refs["teledeclarationForm"].validate()
        if (!teledeclarationFormIsValid) return
      }
      this.handlePreviewClose("teledeclare")
      this.teledeclare()
    },
    handlePreviewClose(eventAction) {
      const eventCategory = "data-warning"
      if (this.$matomo) {
        this.unusualData.forEach((data) => {
          if (data.value) this.$matomo.trackEvent(eventCategory, eventAction, data.id, data.value)
          else this.$matomo.trackEvent(eventCategory, eventAction, data.id)
        })
      }
    },
  },
  mounted() {
    window.addEventListener("resize", this.calculateTableHeight)
    this.calculateTableHeight()
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.calculateTableHeight)
  },
  watch: {
    value(newValue) {
      if (newValue) {
        this.$nextTick().then(this.calculateTableHeight)
      }
      // doesn't get here from confirmTeledeclaration, so we know this is a close
      else {
        this.handlePreviewClose("go-back")
      }
    },
    idx() {
      // we get here if there are multiple TDs to get through at once
      this.tdConfirmed = false
      this.teledeclarationFormIsValid = true
      this.$refs["teledeclarationForm"].reset()
    },
  },
}
</script>
