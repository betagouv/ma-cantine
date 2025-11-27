<template>
  <div>
    <p>
      <strong>Produit ayant plusieurs labels</strong>
      : la valeur d’achat ne pourra être comptée que dans une seule des catégories. Par exemple, un produit à la fois
      biologique et label rouge ne sera comptabilisé que dans la catégorie 'bio'.
    </p>

    <FormErrorCallout v-if="totalError" :errorMessages="[totalErrorMessage]" />

    <!-- Bio -->
    <v-row class="my-0 my-md-6">
      <v-col cols="12" md="8" class="pr-4 pr-md-10">
        <div class="d-block d-sm-flex align-center">
          <LogoBio style="max-height: 30px;" v-if="$vuetify.breakpoint.smAndDown" />
          <label class="ml-4 ml-md-0" for="bio">
            La valeur (en € HT) de mes achats Bio ou en conversion Bio
          </label>
        </div>
        <DsfrCurrencyField
          id="bio"
          v-model.number="payload.valueBioHt"
          @blur="updatePayload"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="totalError"
          :rules="[validators.required, validators.decimalPlaces(2)]"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueBioHt"
          purchaseType="bio"
          :amount="purchasesSummary.valueBioHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          @autofill="updatePayload"
        />
      </v-col>
      <v-col md="4" class="d-flex align-center left-border" v-if="$vuetify.breakpoint.mdAndUp">
        <LogoBio style="max-height: 60px;" class="pl-8 d-none d-md-block" />
      </v-col>
    </v-row>

    <!-- Bio dont commerce équitable -->
    <v-row class="my-0 my-md-6">
      <v-col cols="1" class="pt-0 d-flex align-top justify-end">
        <div class="input-child-icon"></div>
      </v-col>
      <v-col cols="11" md="7" class="pr-4 pr-md-10">
        <div class="d-block d-sm-flex align-center">
          <LogoBio style="max-height: 30px;" v-if="$vuetify.breakpoint.smAndDown" />
          <img
            v-if="$vuetify.breakpoint.smAndDown"
            class="ml-2"
            :src="`/static/images/quality-labels/${commerceEquitableLabels[0].src}`"
            :alt="commerceEquitableLabels[0].title"
            :title="commerceEquitableLabels[0].title"
            style="max-height: 40px;"
          />
          <label class="ml-4 ml-md-0" for="bio-commerce-equitable">
            Dont valeur (en € HT) de mes achats Bio et Commerce équitable
            <span class="fr-hint-text my-2">Optionnel</span>
          </label>
        </div>
        <DsfrCurrencyField
          id="bio-commerce-equitable"
          v-model.number="payload.valueBioDontCommerceEquitableHt"
          @blur="updatePayload"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="totalError"
          :rules="[validators.decimalPlaces(2)]"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueBioDontCommerceEquitableHt"
          purchaseType="Bio et Commerce équitable"
          :amount="purchasesSummary.valueBioDontCommerceEquitableHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          @autofill="updatePayload"
        />
      </v-col>
      <v-col cols="12" md="4" class="d-flex align-center left-border" v-if="$vuetify.breakpoint.mdAndUp">
        <LogoBio style="max-height: 60px;" class="pl-8 d-none d-md-block" />
        <img
          class="ml-2"
          :src="`/static/images/quality-labels/${commerceEquitableLabels[0].src}`"
          :alt="commerceEquitableLabels[0].title"
          :title="commerceEquitableLabels[0].title"
          style="max-height: 40px;"
        />
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
                aria-hidden="true"
                :title="label.title"
                style="max-height: 30px;"
              />
            </div>
          </div>
          <label class="ml-4 ml-md-0" for="siqo">
            La valeur (en € HT) de mes achats SIQO (Label Rouge, AOC / AOP, IGP, STG)
          </label>
        </div>
        <DsfrCurrencyField
          id="siqo"
          v-model.number="payload.valueSustainableHt"
          @blur="updatePayload"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="totalError"
          :rules="[validators.required, validators.decimalPlaces(2)]"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueSustainableHt"
          purchaseType="SIQO"
          :amount="purchasesSummary.valueSustainableHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
          @autofill="updatePayload"
        />
      </v-col>
      <v-col md="4" class="d-flex align-center pl-10 left-border" v-if="$vuetify.breakpoint.mdAndUp">
        <div v-for="label in siqoLabels" :key="label.title">
          <img
            :src="`/static/images/quality-labels/${label.src}`"
            aria-hidden="true"
            :title="label.title"
            class="mr-1"
            style="max-height: 40px;"
          />
        </div>
      </v-col>
    </v-row>
    <ErrorHelper
      v-if="totalError || errorHelperUsed"
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
import validators from "@/validators"
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import FormErrorCallout from "@/components/FormErrorCallout"
import ErrorHelper from "./ErrorHelper"
import labels from "@/data/quality-labels.json"
import LogoBio from "@/components/LogoBio"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import { toCurrency } from "@/utils"

export default {
  name: "BioSiqoStep",
  components: { DsfrCurrencyField, LogoBio, PurchaseHint, ErrorHelper, FormErrorCallout },
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
      "Label Rouge",
      "Appellation d'origine (AOC / AOP)",
      "Indication géographique (IGP)",
      "Spécialité traditionnelle garantie (STG)",
    ]
    const commerceEquitableLogos = ["Commerce Équitable"]
    return {
      totalErrorMessage: "",
      siqoLabels: labels.filter((x) => siqoLogos.includes(x.title)),
      commerceEquitableLabels: labels.filter((x) => commerceEquitableLogos.includes(x.title)),
      errorHelperUsed: false,
      errorHelperFields: [],
    }
  },
  computed: {
    validators() {
      return validators
    },
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    totalError() {
      return !!this.totalErrorMessage
    },
    erroringFields() {
      return this.totalError ? this.errorHelperFields : []
    },
  },
  methods: {
    updatePayload() {
      this.checkTotal()
      if (!this.totalError) this.$emit("update-payload", { payload: this.payload })
    },
    checkTotal() {
      this.totalErrorMessage = null

      const d = this.payload
      const sumEgalim = this.sumAllEgalim()
      const total = d.valueTotalHt

      if (sumEgalim > total) {
        this.totalErrorMessage = `Le total de vos achats alimentaires (${toCurrency(
          d.valueTotalHt
        )}) doit être plus élévé que la somme des valeurs EGalim (${toCurrency(sumEgalim || 0)})`
        this.errorHelperFields = ["valueTotalHt", "valueEgalimOthersHt", "valueExternalityPerformanceHt"]
      }

      if (d.valueBioDontCommerceEquitableHt > d.valueBioHt) {
        this.totalErrorMessage = `La valeur de vos achats Bio et Commerce équitable (${toCurrency(
          d.valueBioDontCommerceEquitableHt
        )}) ne peut pas être plus élévée que la valeur de vos achats Bio ou en conversion Bio (${toCurrency(total)})`
      }
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
    errorUpdate() {
      this.errorHelperUsed = true
      this.checkTotal()
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

.input-child-icon {
  display: block;
  height: 100%;
  width: 100%;
  position: relative;
}

.input-child-icon::before {
  content: "";
  background-color: #000000;
  width: 50%;
  position: absolute;
  right: 0;
  bottom: 30%;
  height: 1px;
}

.input-child-icon::after {
  content: "";
  background-color: #000000;
  width: 1px;
  position: absolute;
  right: 50%;
  bottom: 30%;
  top: 0;
}
</style>
