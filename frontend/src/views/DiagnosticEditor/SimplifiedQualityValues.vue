<template>
  <div>
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
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueTotalHt"
      @autofill="checkTotal"
      purchaseType="totaux"
      :amount="purchasesSummary.total"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />

    <!-- Bio -->
    <v-divider class="my-4"></v-divider>
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
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueBioHt"
      @autofill="checkTotal"
      purchaseType="bio"
      :amount="purchasesSummary.bio"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
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
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
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
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
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
        environnementales ou acquis sur la base de leurs performances en matière environnementale
      </label>
    </div>
    <DsfrCurrencyField
      :id="'ext-perf-' + diagnostic.year"
      v-model.number="diagnostic.valueExternalityPerformanceHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      @blur="checkTotal"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />

    <v-divider class="my-4"></v-divider>

    <div>
      <h3 class="text-h6 font-weight-bold mb-2">
        Zoom sur les familles « viandes et volailles » et « Produits de la mer »
      </h3>
      <p class="text-body-2">
        Depuis la loi Climat et Résilience, un nouvel objectif pour une alimentation saine a été ajoutée : au moins 60%
        de viandes et poissons de qualité et durables et porté à 100 % pour les restaurants collectifs gérés par l'Etat,
        ses établissements publics et les entreprises publiques nationales des produits carnés et issus de la mer plus
        durables, ainsi que davantage de viandes provenant de France. La réalisation du bilan annuel fait par
        l'administration implique également de connaitre la part des produits origine France. Pour ce type de saisie,
        l'information est requise seulement pour la famille des viandes.
      </p>
    </div>

    <v-divider class="my-4"></v-divider>

    <div>
      60% - 100% pour les restaurants d'Etat de « viandes et volailles » EGAlim
    </div>

    <!-- Viande et volailles -->

    <div class="d-block d-sm-flex align-center mt-8">
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
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueMeatPoultryHt"
      @autofill="checkTotal"
      purchaseType="totaux viandes et volailles"
      :amount="purchasesSummary.meatPoultryTotal"
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
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueMeatPoultryEgalimHt"
      @autofill="checkTotal"
      purchaseType="viandes et volailles EGAlim"
      :amount="purchasesSummary.meatPoultryEgalim"
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
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueMeatPoultryFranceHt"
      @autofill="checkTotal"
      purchaseType="viandes et volailles provenance France"
      :amount="purchasesSummary.meatPoultryFrance"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />

    <!-- Poissons -->
    <v-divider class="mb-4 mt-8"></v-divider>

    <div>
      60% - 100% pour les restaurants d'Etat de « poissons, produits de la mer et aquaculture » EGAlim
    </div>
    <div class="d-block d-sm-flex align-center mt-8">
      <div class="d-flex">
        <v-icon size="30" color="blue">
          mdi-fish
        </v-icon>
      </div>
      <label class="body-2 ml-4" :for="'fish-' + diagnostic.year">
        La valeur (en HT) des mes achats en poissons, produits de la mer et aquaculture total
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
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueFishHt"
      @autofill="checkTotal"
      purchaseType="totaux de poissons, produits de la mer et aquaculture"
      :amount="purchasesSummary.fishTotal"
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
        La valeur (en HT) des mes achats EGAlim en poissons, produits de la mer et aquaculture
      </label>
    </div>
    <DsfrCurrencyField
      :id="'fish-egalim-' + diagnostic.year"
      v-model.number="diagnostic.valueFishEgalimHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="fishError"
      @blur="checkTotal"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueFishEgalimHt"
      @autofill="checkTotal"
      purchaseType="poissons, produits de la mer et aquaculture EGAlim"
      :amount="purchasesSummary.fishEgalim"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />
  </div>
</template>

<script>
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import labels from "@/data/quality-labels.json"
import validators from "@/validators"
import LogoBio from "@/components/LogoBio"
import DsfrCurrencyField from "@/components/DsfrCurrencyField"

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
        this.totalErrorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${sumEgalim || 0} €`
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
        (this.meatPoultryError ? `${DEFAULT_MEAT_POULTRY_ERROR}, actuellement ${sumMeatPoultry || 0} €` : "")

      this.fishErrorMessage =
        this.fishErrorMessage || (this.fishError ? `${DEFAULT_FISH_ERROR}, actuellement ${sumFish || 0} €` : "")
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
