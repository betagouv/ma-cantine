<template>
  <div>
    <p>
      <strong>Produit ayant plusieurs labels</strong>
      : la valeur d’achat ne pourra être comptée que dans une seule des catégories.
    </p>

    <FormErrorCallout v-if="totalError" :errorMessages="[totalErrorMessage]" />

    <!-- Other EGalim -->
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
            <v-icon size="30" color="brown" aria-hidden="true" title="Fermier">
              mdi-cow
            </v-icon>
          </div>

          <label class="ml-4 ml-md-0" for="other">
            La valeur (en € HT) des autres achats EGalim
          </label>
        </div>
        <DsfrCurrencyField
          id="other"
          v-model.number="payload.valueEgalimOthersHt"
          @blur="updatePayload"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="totalError"
          :rules="[validators.required, validators.decimalPlaces(2)]"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueEgalimOthersHt"
          @autofill="updatePayload"
          purchaseType="« autre EGalim »"
          :amount="purchasesSummary.valueEgalimOthersHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </v-col>
      <v-col md="4" class="d-flex align-center pl-10 left-border" v-if="$vuetify.breakpoint.mdAndUp">
        <div v-for="label in otherLabels" :key="label.title">
          <img
            :src="`/static/images/quality-labels/${label.src}`"
            :alt="label.title"
            :title="label.title"
            class="mr-1"
            style="max-height: 40px;"
          />
        </div>
        <v-icon size="40" color="brown" alt="Fermier" title="Fermier">
          mdi-cow
        </v-icon>
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
            Critères d'achat : La valeur (en € HT) mes achats réalisés selon des modalités de sélection prenant en
            compte les coûts imputés aux externalités environnementales ou prenant en compte les performances
            environnementales et d’approvisionnements directs
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
                    <v-icon color="purple" aria-hidden="true" title="Externalités environnementales">
                      mdi-flower-tulip-outline
                    </v-icon>
                    <v-icon class="ml-1" color="green" aria-hidden="true" title="Performance environnementale">
                      mdi-chart-line
                    </v-icon>
                  </div>
                  <v-card-title>
                    <h1 class="fr-h6 mb-0">
                      Quels achats rentrent dans ce champ ?
                    </h1>
                  </v-card-title>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" outlined @click="valueExternalityPerformanceHtDialog = false">
                    Fermer
                  </v-btn>
                </div>
                <v-card-text class="text-sm-body-1 grey-text text-darken-3 pt-6">
                  <p class="mb-0">
                    Deux catégories, prévues par la loi, s'appuient sur des critères de sélection des offres lors des
                    marchés publics ou appels d'offre, et non sur des labels, certifications.
                  </p>
                </v-card-text>
                <v-card-text class="text-sm-body-1 grey-text text-darken-3">
                  <p>Ces deux catégories sont :</p>
                  <ul>
                    <li>
                      Produit acquis suivant des modalités prenant en compte les coûts imputés aux externalités
                      environnementales liées au produit pendant son cycle de vie ;
                    </li>
                    <li>
                      Les produits dont l’acquisition a été fondée principalement sur la base de leurs performances en
                      matière de protection de l’environnement et de développement des approvisionnements directs de
                      produits de l’agriculture.
                    </li>
                  </ul>
                </v-card-text>
                <v-card-text class="text-sm-body-1 grey-text text-darken-3">
                  <p class="mb-0">
                    Ni la loi EGalim, ni le code de la commande publique n'imposent de soumettre la méthodologie de
                    sélection à une validation de l'administration. Dès lors qu'ils respectent les exigences du code de
                    la commande publique, les acheteurs ayant recours à ce mode de sélection sont libres de définir les
                    modalités qui leur semblent les plus pertinentes sous leur responsabilité. Certaines démarches
                    collectives et/ou certains fournisseurs accompagnent déjà les acheteurs dans la mise en place d'une
                    méthode.
                  </p>
                </v-card-text>
              </v-card>
            </v-dialog>
            <span class="fr-hint-text mt-2">Optionnel</span>
          </label>
        </div>
        <DsfrCurrencyField
          id="ext-perf"
          v-model.number="payload.valueExternalityPerformanceHt"
          @blur="updatePayload"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="totalError"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueExternalityPerformanceHt"
          @autofill="updatePayload"
          purchaseType="« critères d'achat »"
          :amount="purchasesSummary.valueExternalityPerformanceHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </v-col>
      <v-col md="4" class="d-flex align-center pl-10 left-border" v-if="$vuetify.breakpoint.mdAndUp">
        <div class="d-flex">
          <v-icon size="30" color="purple" aria-hidden="true" title="Externalités environnementales">
            mdi-flower-tulip-outline
          </v-icon>
          <v-icon size="30" class="ml-2" color="green" aria-hidden="true" title="Performance environnementale">
            mdi-chart-line
          </v-icon>
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
      "Haute Valeur Environnementale (HVE)",
      "Écolabel pêche durable",
      "Région Ultrapériphérique (RUP)",
      "Commerce Équitable",
    ]
    return {
      totalErrorMessage: null,
      otherLabels: labels.filter((x) => otherLogos.includes(x.title)),
      valueExternalityPerformanceHtDialog: false,
      errorHelperUsed: false,
      errorHelperFields: ["valueTotalHt", "valueBioHt", "valueSustainableHt"],
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
</style>
