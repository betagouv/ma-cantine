<template>
  <div>
    <p>
      <strong>Produit ayant plusieurs labels</strong>
      : la valeur d’achat ne pourra être comptée que dans une seule des catégories. Par exemple, un produit à la fois
      biologique et label rouge ne sera comptabilisé que dans la catégorie 'bio'.
    </p>

    <DsfrCallout v-if="totalError" color="red lighten-1">
      {{ totalErrorMessage }}
    </DsfrCallout>

    <!-- Bio -->
    <v-row class="my-0 my-md-6">
      <v-col cols="12" md="8" class="pr-4 pr-md-10">
        <div class="d-block d-sm-flex align-center">
          <LogoBio style="max-height: 30px;" v-if="$vuetify.breakpoint.smAndDown" />
          <label class="ml-4 ml-md-0" for="bio">
            La valeur (en HT) de mes achats Bio ou en conversion Bio (Optionnel)
          </label>
        </div>
        <DsfrCurrencyField
          id="bio"
          v-model.number="payload.valueBioHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="totalError"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueBioHt"
          purchaseType="bio"
          :amount="purchasesSummary.valueBioHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          @autofill="checkTotal"
        />
      </v-col>
      <v-col md="4" class="d-flex align-center left-border" v-if="$vuetify.breakpoint.mdAndUp">
        <LogoBio style="max-height: 60px;" class="pl-8 d-none d-md-block" />
      </v-col>
    </v-row>

    <!-- SIQO -->
    <v-row>
      <v-col cols="12" md="8" class="pr-4 pr-md-10">
        <div class="d-block d-sm-flex align-center">
          <div class="d-flex" v-if="$vuetify.breakpoint.smAndDown">
            <div v-for="label in siqoLabels" :key="label.title">
              <img
                :src="`/static/images/quality-labels/${label.src}`"
                :alt="label.title"
                :title="label.title"
                style="max-height: 30px;"
              />
            </div>
          </div>
          <label class="ml-4 ml-md-0" for="siqo">
            La valeur (en HT) de mes achats SIQO (AOP/AOC, IGP, STG, Label Rouge)
          </label>
        </div>
        <DsfrCurrencyField
          id="siqo"
          v-model.number="payload.valueSustainableHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="totalError"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueSustainableHt"
          purchaseType="SIQO"
          :amount="purchasesSummary.valueSustainableHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          @autofill="checkTotal"
        />
      </v-col>
      <v-col md="4" class="d-flex align-center pl-10 left-border" v-if="$vuetify.breakpoint.mdAndUp">
        <div v-for="label in siqoLabels" :key="label.title">
          <img
            :src="`/static/images/quality-labels/${label.src}`"
            :alt="label.title"
            :title="label.title"
            class="mr-1"
            style="max-height: 40px;"
          />
        </div>
      </v-col>
    </v-row>
    <ErrorHelper
      :showFields="['valueTotalHt', 'valueEgalimOthersHt', 'valueExternalityPerformanceHt']"
      :class="`${totalError ? '' : 'd-none'}`"
      :diagnostic="payload"
      @check-total="checkTotal"
      :purchasesSummary="purchasesSummary"
    />
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import DsfrCallout from "@/components/DsfrCallout"
import ErrorHelper from "./ErrorHelper.vue"
import labels from "@/data/quality-labels.json"
import LogoBio from "@/components/LogoBio"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import { toCurrency } from "@/utils"

export default {
  name: "BioSiqoStep",
  components: { DsfrCurrencyField, LogoBio, PurchaseHint, ErrorHelper, DsfrCallout },
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
    const siqoLogos = [
      "Logo Label Rouge",
      "Logo Appellation d'origine (AOC/AOP)",
      "Logo indication géographique",
      "Logo Spécialité traditionnelle garantie",
    ]
    return {
      totalError: false,
      totalErrorMessage: "",
      siqoLabels: labels.filter((x) => siqoLogos.includes(x.title)),
    }
  },
  computed: {
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
    },
  },
  methods: {
    updatePayload() {
      this.checkTotal()
      if (!this.totalError) this.$emit("update-payload", { payload: this.payload })
    },
    checkTotal() {
      const d = this.payload
      const sumEgalim = this.sumAllEgalim()
      const total = d.valueTotalHt
      this.totalError = sumEgalim > total

      if (this.totalError) {
        this.totalErrorMessage = `Le total de vos achats alimentaires (${toCurrency(
          d.valueTotalHt
        )}) doit être plus élévé que la somme des valeurs EGAlim (${toCurrency(sumEgalim || 0)})`
      } else this.totalErrorMessage = null
      return !!this.totalError
    },
    sumAllEgalim() {
      const d = this.payload
      const egalimValues = [d.valueBioHt, d.valueSustainableHt, d.valueExternalityPerformanceHt, d.valueEgalimOthersHt]
      let total = 0
      egalimValues.forEach((val) => {
        total += parseFloat(val) || 0
      })
      return total
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
