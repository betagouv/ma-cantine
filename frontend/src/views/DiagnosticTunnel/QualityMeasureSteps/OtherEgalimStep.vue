<template>
  <div>
    <p>
      <strong>Produit ayant plusieurs labels</strong>
      : la valeur d’achat ne pourra être comptée que dans une seule des catégories.
    </p>

    <FormErrorCallout v-if="totalError" :errorMessages="[totalErrorMessage]" />

    <!-- Other EGAlim -->
    <v-row class="my-0 my-md-6">
      <v-col cols="12" md="8" class="pr-4 pr-md-10">
        <div class="d-block d-sm-flex align-center">
          <div class="d-flex" v-if="$vuetify.breakpoint.smAndDown">
            <div v-for="label in otherLabels" :key="label.title">
              <img
                :src="`/static/images/quality-labels/${label.src}`"
                :alt="label.title"
                :title="label.title"
                style="max-height: 30px;"
              />
            </div>
            <v-icon size="30" color="brown" aria-label="Fermier" title="Fermier" aria-hidden="false" role="img">
              mdi-cow
            </v-icon>
          </div>

          <label class="ml-4 ml-md-0" for="other">
            La valeur (en HT) des autres achats EGAlim
            <span class="fr-hint-text mt-2">Optionnel</span>
          </label>
        </div>
        <DsfrCurrencyField
          id="other"
          v-model.number="payload.valueEgalimOthersHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="totalError"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueEgalimOthersHt"
          @autofill="checkTotal"
          purchaseType="« autre EGAlim »"
          :amount="purchasesSummary.valueEgalimOthersHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </v-col>
      <v-col md="4" class="d-flex align-center left-border" v-if="$vuetify.breakpoint.mdAndUp">
        <div class="d-flex pl-10">
          <div v-for="label in otherLabels" :key="label.title">
            <img
              :src="`/static/images/quality-labels/${label.src}`"
              :alt="label.title"
              :title="label.title"
              class="mr-1"
              style="max-height: 40px;"
            />
          </div>
          <v-icon size="40" color="brown" aria-label="Fermier" title="Fermier" aria-hidden="false" role="img">
            mdi-cow
          </v-icon>
        </div>
      </v-col>
    </v-row>

    <!-- Externalités -->
    <v-row>
      <v-col cols="12" md="8" class="pr-4 pr-md-10">
        <div class="d-block d-sm-flex align-center">
          <div class="d-flex" v-if="$vuetify.breakpoint.smAndDown">
            <v-icon size="30" color="purple">
              mdi-flower-tulip-outline
            </v-icon>
            <v-icon size="30" class="ml-2" color="green">
              mdi-chart-line
            </v-icon>
          </div>
          <label class="ml-4 ml-md-0" for="ext-perf">
            Critères d'achat : La valeur (en HT) de mes achats prenant en compte les coûts imputés aux externalités
            environnementales ou acquis sur la base de leurs performances en matière environnementale.
            <br />
            <v-dialog v-model="valueExternalityPerformanceHtDialog" max-width="600">
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" outlined small v-bind="attrs" v-on="on">
                  <v-icon small class="mr-2">$information-line</v-icon>
                  Plus d'informations
                </v-btn>
              </template>
              <v-card class="text-left">
                <div class="pa-4 d-flex align-center" style="background-color: #F5F5F5">
                  <div class="d-flex">
                    <v-icon color="purple" alt="" title="Externalités environnementales">
                      mdi-flower-tulip-outline
                    </v-icon>
                    <v-icon class="ml-1" color="green" alt="" title="Performance environnementale">
                      mdi-chart-line
                    </v-icon>
                  </div>
                  <v-card-title class="text-h6">
                    Quels achats rentrent dans ce champ ?
                  </v-card-title>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" outlined @click="valueExternalityPerformanceHtDialog = false">
                    Fermer
                  </v-btn>
                </div>
                <v-card-text class="text-sm-body-1 grey-text text-darken-3 pt-6">
                  Produit acquis suivant des modalités prenant en compte les coûts imputés aux externalités
                  environnementales liées au produit pendant son cycle de vie (production, transformation,
                  conditionnement, transport, stockage, utilisation) - L'article 2152-10 du code de la commande publique
                  dispose que, pour l'évaluation du coût du cycle de vie des produits, les acheteurs s'appuient sur une
                  méthode accessible à tous, fondée sur des critères non-discriminatoires et vérifiables de manière
                  objective et qui n'implique, pour les soumissionnaires, qu'un effort raisonnable dans la fourniture
                  des données demandées.
                </v-card-text>
                <v-card-text class="text-sm-body-1 grey-text text-darken-3">
                  Ni la loi EGALIM, ni le code de la commande publique n'imposent de soumettre la méthodologie de calcul
                  du coût des externalités environnementales liées aux produits à une validation de l'administration.
                  Dès lors qu'ils respectent les exigences du code de la commande publique, les acheteurs ayant recours
                  à ce mode de sélection sont libres de définir les modalités qui leur semblent les plus pertinentes
                  sous leur responsabilité. Certaines démarches collectives et/ou certains fournisseurs accompagnent
                  déjà les acheteurs dans la mise en place d'une méthode.
                </v-card-text>
              </v-card>
            </v-dialog>
            <span class="fr-hint-text mt-2">Optionnel</span>
          </label>
        </div>
        <DsfrCurrencyField
          id="ext-perf"
          v-model.number="payload.valueExternalityPerformanceHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="totalError"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueExternalityPerformanceHt"
          @autofill="checkTotal"
          purchaseType="« critères d'achat »"
          :amount="purchasesSummary.valueExternalityPerformanceHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </v-col>
      <v-col md="4" class="d-flex align-center pl-10 left-border" v-if="$vuetify.breakpoint.mdAndUp">
        <div class="d-flex">
          <v-icon size="30" color="purple" alt="" title="Externalités environnementales">
            mdi-flower-tulip-outline
          </v-icon>
          <v-icon size="30" class="ml-2" color="green" alt="" title="Performance environnementale">
            mdi-chart-line
          </v-icon>
        </div>
      </v-col>
    </v-row>
    <ErrorHelper
      :showFields="['valueTotalHt', 'valueBioHt', 'valueSustainableHt']"
      :class="`${totalError ? '' : 'd-none'}`"
      :diagnostic="payload"
      @check-total="checkTotal"
      :purchasesSummary="purchasesSummary"
    />
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import labels from "@/data/quality-labels.json"
import { toCurrency } from "@/utils"
import ErrorHelper from "./ErrorHelper"
import FormErrorCallout from "@/components/FormErrorCallout"

export default {
  name: "OtherEgalimStep",
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
    const otherLogos = [
      "Logo Haute Valeur Environnementale",
      "Écolabel pêche durable",
      "Logo Région Ultrapériphérique",
      "Logo Commerce Équitable",
    ]
    return {
      totalErrorMessage: null,
      otherLabels: labels.filter((x) => otherLogos.includes(x.title)),
      valueExternalityPerformanceHtDialog: false,
    }
  },
  computed: {
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
    totalError() {
      return !!this.totalErrorMessage
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

      if (sumEgalim > total) {
        this.totalErrorMessage = `Le total de vos achats alimentaires (${toCurrency(
          d.valueTotalHt
        )}) doit être plus élévé que la somme des valeurs EGAlim (${toCurrency(sumEgalim || 0)})`
      } else this.totalErrorMessage = null
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
