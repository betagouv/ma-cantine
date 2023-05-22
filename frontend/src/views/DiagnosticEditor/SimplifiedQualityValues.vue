<template>
  <div>
    <!-- Input used for cross-field validation : https://github.com/vuetifyjs/vuetify/issues/8698 -->
    <v-input hidden :rules="[checkTotal]" hide-details></v-input>

    <label :for="'total-' + diagnostic.year" class="body-2">
      La valeur (en HT) de mes achats alimentaires total
    </label>

    <DsfrCurrencyField
      :id="'total-' + diagnostic.year"
      v-model.number="diagnostic.valueTotalHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError || totalMeatPoultryError || totalFishError"
      :messages="totalError || totalMeatPoultryError || totalFishError ? [totalErrorMessage] : undefined"
      @blur="checkTotal"
      :class="$vuetify.display.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueTotalHt"
      @autofill="checkTotal"
      purchaseType="totaux"
      :amount="purchasesSummary.valueTotalHt"
      :class="$vuetify.display.mdAndUp ? 'narrow-field' : ''"
    />

    <v-divider class="my-4"></v-divider>

    <p class="caption">
      Produit ayant plusieurs labels : la valeur d’achat de ce produit ne pourra être comptée que dans une seule des 4
      catégories ci-dessous. Par exemple, un produit à la fois biologique et label rouge ne sera comptabilisé que dans
      la catégorie 'bio'.
    </p>
    <!-- Bio -->
    <div class="d-block d-sm-flex align-center">
      <LogoBio style="max-height: 30px;" />
      <label class="body-2 ml-4" :for="'bio-' + diagnostic.year">
        La valeur (en HT) de mes achats Bio ou en conversion Bio
      </label>
    </div>
    <DsfrCurrencyField
      :id="'bio-' + diagnostic.year"
      v-model.number="diagnostic.valueBioHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      @blur="checkTotal"
      :class="$vuetify.display.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueBioHt"
      @autofill="checkTotal"
      purchaseType="bio"
      :amount="purchasesSummary.valueBioHt"
      :class="$vuetify.display.mdAndUp ? 'narrow-field' : ''"
    />

    <!-- SIQO -->
    <div class="d-block d-sm-flex align-center mt-8">
      <div class="d-flex">
        <div v-for="label in siqoLabels" :key="label.title">
          <img
            :src="`/static/images/quality-labels/${label.src}`"
            :alt="label.title"
            :title="label.title"
            style="max-height: 30px;"
          />
        </div>
      </div>
      <label class="body-2 ml-4" :for="'siqo-' + diagnostic.year">
        La valeur (en HT) de mes achats SIQO (AOP/AOC, IGP, STG, Label Rouge)
      </label>
    </div>
    <DsfrCurrencyField
      :id="'siqo-' + diagnostic.year"
      v-model.number="diagnostic.valueSustainableHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      @blur="checkTotal"
      :class="$vuetify.display.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueSustainableHt"
      @autofill="checkTotal"
      purchaseType="SIQO"
      :amount="purchasesSummary.valueSustainableHt"
      :class="$vuetify.display.mdAndUp ? 'narrow-field' : ''"
    />

    <!-- Other EGAlim -->
    <div class="d-block d-sm-flex align-center mt-8">
      <div class="d-flex">
        <div v-for="label in otherLabels" :key="label.title">
          <img
            :src="`/static/images/quality-labels/${label.src}`"
            :alt="label.title"
            :title="label.title"
            style="max-height: 30px;"
          />
        </div>
        <v-icon size="30" color="brown">
          mdi-cow
        </v-icon>
      </div>
      <label class="body-2 ml-4" :for="'other-' + diagnostic.year">
        La valeur (en HT) des autres achats EGAlim
      </label>
    </div>
    <DsfrCurrencyField
      :id="'other-' + diagnostic.year"
      v-model.number="diagnostic.valueEgalimOthersHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      @blur="checkTotal"
      :class="$vuetify.display.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueEgalimOthersHt"
      @autofill="checkTotal"
      purchaseType="« autre EGAlim »"
      :amount="purchasesSummary.valueEgalimOthersHt"
      :class="$vuetify.display.mdAndUp ? 'narrow-field' : ''"
    />

    <!-- Performance Externalités -->
    <div class="d-block d-sm-flex align-center mt-8">
      <div class="d-flex">
        <v-icon size="30" color="purple">
          mdi-flower-tulip-outline
        </v-icon>
        <v-icon size="30" class="ml-2" color="green">
          mdi-chart-line
        </v-icon>
      </div>
      <label class="body-2 ml-4" :for="'ext-perf-' + diagnostic.year">
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
                <v-icon color="purple">
                  mdi-flower-tulip-outline
                </v-icon>
                <v-icon class="ml-1" color="green">
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
              environnementales liées au produit pendant son cycle de vie (production, transformation, conditionnement,
              transport, stockage, utilisation) - L'article 2152-10 du code de la commande publique dispose que, pour
              l'évaluation du coût du cycle de vie des produits, les acheteurs s'appuient sur une méthode accessible à
              tous, fondée sur des critères non-discriminatoires et vérifiables de manière objective et qui n'implique,
              pour les soumissionnaires, qu'un effort raisonnable dans la fourniture des données demandées.
            </v-card-text>
            <v-card-text class="text-sm-body-1 grey-text text-darken-3">
              Ni la loi EGALIM, ni le code de la commande publique n'imposent de soumettre la méthodologie de calcul du
              coût des externalités environnementales liées aux produits à une validation de l'administration. Dès lors
              qu'ils respectent les exigences du code de la commande publique, les acheteurs ayant recours à ce mode de
              sélection sont libres de définir les modalités qui leur semblent les plus pertinentes sous leur
              responsabilité. Certaines démarches collectives et/ou certains fournisseurs accompagnent déjà les
              acheteurs dans la mise en place d'une méthode.
            </v-card-text>
          </v-card>
        </v-dialog>
      </label>
    </div>
    <DsfrCurrencyField
      :id="'ext-perf-' + diagnostic.year"
      v-model.number="diagnostic.valueExternalityPerformanceHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      @blur="checkTotal"
      :class="$vuetify.display.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueExternalityPerformanceHt"
      @autofill="checkTotal"
      purchaseType="« critères d'achat »"
      :amount="purchasesSummary.valueExternalityPerformanceHt"
      :class="$vuetify.display.mdAndUp ? 'narrow-field' : ''"
    />

    <v-divider class="my-4"></v-divider>

    <div>
      <h3 class="text-h6 font-weight-bold mb-2">
        Zoom sur les familles « viandes et volailles » et « produits de la mer et de l'aquaculture»
      </h3>
      <p class="text-body-2">
        Depuis la loi Climat et Résilience, un nouvel objectif pour une alimentation saine et durable a été ajouté :
        pour les achats de 2024, au moins 60% de viandes et poissons de qualité et durables. Ce taux est porté à 100 %
        pour les restaurants collectifs gérés par l'Etat, ses établissements publics et les entreprises publiques
        nationales.
      </p>
      <p class="text-body-2">
        La réalisation du bilan annuel fait par l’administration implique également de connaitre la part des produits
        origine France. Pour ce type de saisie, l’information est requise seulement pour la famille des viandes.
      </p>
    </div>

    <v-divider class="my-8"></v-divider>

    <!-- Viande et volailles -->

    <div class="d-block d-sm-flex align-center">
      <div class="d-flex">
        <v-icon size="30" color="brown">
          mdi-food-steak
        </v-icon>
        <v-icon size="30" color="brown">
          mdi-food-drumstick
        </v-icon>
      </div>
      <label class="body-2 ml-4" :for="'meat-poultry-' + diagnostic.year">
        La valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total
      </label>
    </div>
    <DsfrCurrencyField
      :id="'meat-poultry-' + diagnostic.year"
      v-model.number="diagnostic.valueMeatPoultryHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="meatPoultryError || totalMeatPoultryError"
      :messages="meatPoultryError || totalMeatPoultryError ? [meatPoultryErrorMessage] : undefined"
      @blur="checkTotal"
      :class="$vuetify.display.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueMeatPoultryHt"
      @autofill="checkTotal"
      purchaseType="totaux viandes et volailles"
      :amount="purchasesSummary.valueMeatPoultryHt"
      :class="$vuetify.display.mdAndUp ? 'narrow-field' : ''"
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
      <label class="body-2 ml-4" :for="'meat-poultry-egalim-' + diagnostic.year">
        La valeur (en HT) des mes achats EGAlim en viandes et volailles fraiches ou surgelées
      </label>
    </div>
    <DsfrCurrencyField
      :id="'meat-poultry-egalim-' + diagnostic.year"
      v-model.number="diagnostic.valueMeatPoultryEgalimHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="meatPoultryError"
      @blur="checkTotal"
      :class="$vuetify.display.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueMeatPoultryEgalimHt"
      @autofill="checkTotal"
      purchaseType="viandes et volailles EGAlim"
      :amount="purchasesSummary.valueMeatPoultryEgalimHt"
      :class="$vuetify.display.mdAndUp ? 'narrow-field' : ''"
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
      <label class="body-2 ml-4" :for="'meat-poultry-france-' + diagnostic.year">
        La valeur (en HT) des mes achats provenance France en viandes et volailles fraiches ou surgelées
      </label>
    </div>
    <DsfrCurrencyField
      :id="'meat-poultry-france-' + diagnostic.year"
      v-model.number="diagnostic.valueMeatPoultryFranceHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="meatPoultryError"
      @blur="checkTotal"
      :class="$vuetify.display.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueMeatPoultryFranceHt"
      @autofill="checkTotal"
      purchaseType="viandes et volailles provenance France"
      :amount="purchasesSummary.valueMeatPoultryFranceHt"
      :class="$vuetify.display.mdAndUp ? 'narrow-field' : ''"
    />

    <!-- Poissons -->
    <v-divider class="my-8"></v-divider>

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
      v-model.number="diagnostic.valueFishHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="fishError || totalFishError"
      :messages="fishError || totalFishError ? [fishErrorMessage] : undefined"
      @blur="checkTotal"
      :class="$vuetify.display.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueFishHt"
      @autofill="checkTotal"
      purchaseType="totaux de poissons, produits de la mer et de l'aquaculture"
      :amount="purchasesSummary.valueFishHt"
      :class="$vuetify.display.mdAndUp ? 'narrow-field' : ''"
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
      v-model.number="diagnostic.valueFishEgalimHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="fishError"
      @blur="checkTotal"
      :class="$vuetify.display.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueFishEgalimHt"
      @autofill="checkTotal"
      purchaseType="poissons, produits de la mer et de l'aquaculture EGAlim"
      :amount="purchasesSummary.valueFishEgalimHt"
      :class="$vuetify.display.mdAndUp ? 'narrow-field' : ''"
    />
  </div>
</template>

<script>
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import labels from "@/data/quality-labels.json"
import validators from "@/validators"
import LogoBio from "@/components/LogoBio"
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import { toCurrency } from "@/utils"

const DEFAULT_TOTAL_ERROR = "Le total doit être plus que la somme des valeurs par label"
const DEFAULT_FAMILY_TOTAL_ERROR = "La somme des achats par famille ne peut pas excéder le total des achats"
const DEFAULT_MEAT_POULTRY_ERROR = "La valeur totale doit être supérieure que celle des labels"
const DEFAULT_FISH_ERROR = "La valeur totale doit être supérieure que la valeur EGAlim"

export default {
  name: "SimplifiedQualityValues",
  props: {
    originalDiagnostic: Object,
    purchasesSummary: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    PurchaseHint,
    LogoBio,
    DsfrCurrencyField,
  },
  data() {
    const siqoLogos = [
      "Logo Label Rouge",
      "Logo Appellation d'origine (AOC/AOP)",
      "Logo indication géographique",
      "Logo Spécialité traditionnelle garantie",
    ]
    const otherLogos = [
      "Logo Haute Valeur Environnementale",
      "Écolabel pêche durable",
      "Logo Région Ultrapériphérique",
      "Logo Commerce Équitable",
    ]
    return {
      totalMeatPoultryError: false,
      totalFishError: false,
      totalError: false,
      totalErrorMessage: DEFAULT_TOTAL_ERROR,
      meatPoultryError: false,
      meatPoultryErrorMessage: DEFAULT_MEAT_POULTRY_ERROR,
      fishError: false,
      fishErrorMessage: DEFAULT_FISH_ERROR,
      siqoLabels: labels.filter((x) => siqoLogos.includes(x.title)),
      otherLabels: labels.filter((x) => otherLogos.includes(x.title)),
      valueExternalityPerformanceHtDialog: false,
    }
  },
  computed: {
    validators() {
      return validators
    },
    diagnostic() {
      return this.originalDiagnostic
    },
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x) && !this.readonly
    },
    hasActiveTeledeclaration() {
      return this.diagnostic.teledeclaration && this.diagnostic.teledeclaration.status === "SUBMITTED"
    },
  },
  methods: {
    checkTotal() {
      const d = this.diagnostic
      const sumEgalim = this.sumAllEgalim()
      // Note that we do Math.max because some meat-poultry may be overlapped : both bio and provenance France
      const sumMeatPoultry = Math.max(d.valueMeatPoultryEgalimHt, d.valueMeatPoultryFranceHt)
      const sumFish = d.valueFishEgalimHt
      const total = d.valueTotalHt
      const totalMeatPoultry = d.valueMeatPoultryHt
      const totalFish = d.valueFishHt
      const totalFamilies = totalMeatPoultry + totalFish

      this.totalError = sumEgalim > total
      this.totalMeatPoultryError = !this.totalError && (totalMeatPoultry > total || totalFamilies > total)
      this.totalFishError = !this.totalError && (totalFish > total || totalFamilies > total)
      this.meatPoultryError = !this.totalMeatPoultryError && sumMeatPoultry > totalMeatPoultry
      this.fishError = !this.totalFishError && sumFish > totalFish

      if (this.totalError) {
        this.totalErrorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${toCurrency(sumEgalim || 0)}`
      }
      if (this.totalMeatPoultryError) {
        this.meatPoultryErrorMessage = this.totalErrorMessage = `${DEFAULT_FAMILY_TOTAL_ERROR}`
      }
      if (this.totalFishError) {
        this.fishErrorMessage = this.totalErrorMessage = `${DEFAULT_FAMILY_TOTAL_ERROR}`
      }
      if (!this.totalError && !this.totalMeatPoultryError && !this.totalFishError) {
        this.meatPoultryErrorMessage = this.fishErrorMessage = this.totalErrorMessage = ""
      }

      this.meatPoultryErrorMessage =
        this.meatPoultryErrorMessage ||
        (this.meatPoultryError ? `${DEFAULT_MEAT_POULTRY_ERROR}, actuellement ${toCurrency(sumMeatPoultry || 0)}` : "")

      this.fishErrorMessage =
        this.fishErrorMessage ||
        (this.fishError ? `${DEFAULT_FISH_ERROR}, actuellement ${toCurrency(sumFish || 0)}` : "")

      return [
        this.totalError,
        this.totalMeatPoultryError,
        this.totalFishError,
        this.meatPoultryError,
        this.fishError,
      ].every((x) => !x)
    },
    sumAllEgalim() {
      const d = this.diagnostic
      const egalimValues = [d.valueBioHt, d.valueSustainableHt, d.valueExternalityPerformanceHt, d.valueEgalimOthersHt]
      let total = 0
      egalimValues.forEach((val) => {
        total += parseFloat(val) || 0
      })
      return total
    },
  },
}
</script>

<style scoped>
fieldset {
  border: none;
}
.narrow-field {
  width: 50%;
}
</style>
