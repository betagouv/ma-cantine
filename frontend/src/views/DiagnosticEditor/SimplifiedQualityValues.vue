<template>
  <div>
    <label :for="'total-' + diagnostic.year" class="body-2">
      La valeur (en HT) de mes achats alimentaires total
    </label>

    <v-text-field
      :id="'total-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueTotalHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      :messages="totalError ? [totalErrorMessage] : undefined"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueTotalHt"
      @autofill="checkTotal"
      purchaseType="totaux"
      :amount="purchasesSummary.total"
    />

    <!-- Bio -->
    <v-divider class="my-4"></v-divider>
    <div class="d-block d-sm-flex align-center">
      <LogoBio style="max-height: 30px;" />
      <label class="body-2 ml-4" :for="'bio-' + diagnostic.year">
        La valeur (en HT) de mes achats Bio ou en conversion Bio
      </label>
    </div>
    <v-text-field
      :id="'bio-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueBioHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueBioHt"
      @autofill="checkTotal"
      purchaseType="bio"
      :amount="purchasesSummary.bio"
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
        La valeur (en HT) de mes achats SIQO (AOP/AOC, IGP, STG)
      </label>
    </div>
    <v-text-field
      :id="'siqo-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueSustainableHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>

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
        La valeur (en HT) de mes achats prenant en compte les coûts imputés aux externalités environnementales ou acquis
        sur la base de leurs performances en matière environnementale
      </label>
    </div>
    <v-text-field
      :id="'ext-perf-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueExternalityPerformanceHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>

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
    <v-text-field
      :id="'other-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueEgalimOthersHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>

    <v-divider class="my-4"></v-divider>

    <div>
      <div class="text-h6 font-weight-bold mb-2">
        Zoom sur les familles « viandes et volailles » et « Produits de la mer »
      </div>
      <div>
        Depuis la loi Climat et Résilience, un nouvel objectif pour une alimentation saine a été ajoutée : des produits
        carnés et issus de la mer plus durables, ainsi que davantage de viandes provenant de France.
      </div>
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
    <v-text-field
      :id="'meat-poultry-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueMeatPoultryHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="meatPoultryError"
      :messages="meatPoultryError ? [meatPoultryErrorMessage] : undefined"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>

    <!-- Viande et volailles EGALIM -->
    <div class="d-block d-sm-flex align-center mt-8">
      <div class="d-flex">
        <v-icon size="30" color="green">
          mdi-check-circle
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
    <v-text-field
      :id="'meat-poultry-egalim-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueMeatPoultryEgalimHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="meatPoultryError"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>

    <!-- Viande et volailles provenance FRANCE -->
    <div class="d-block d-sm-flex align-center mt-8">
      <div class="d-flex">
        <v-icon size="30" color="indigo">
          mdi-hexagon-outline
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
    <v-text-field
      :id="'meat-poultry-france-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueMeatPoultryFranceHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="meatPoultryError"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>

    <!-- Poissons -->
    <v-divider class="mb-4 mt-8"></v-divider>

    <div>
      60% - 100% pour les restaurants d'Etat de « poissons et produits aquatiques » EGAlim
    </div>
    <div class="d-block d-sm-flex align-center mt-8">
      <div class="d-flex">
        <v-icon size="30" color="blue">
          mdi-fish
        </v-icon>
      </div>
      <label class="body-2 ml-4" :for="'fish-' + diagnostic.year">
        La valeur (en HT) des mes achats en poissons et produits aquatiques total
      </label>
    </div>
    <v-text-field
      :id="'fish-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueFishHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="fishError"
      :messages="fishError ? [fishErrorMessage] : undefined"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>

    <!-- Poissons EGALIM -->
    <div class="d-block d-sm-flex align-center mt-8">
      <div class="d-flex">
        <v-icon size="30" color="green">
          mdi-check-circle
        </v-icon>
        <v-icon size="30" color="blue">
          mdi-fish
        </v-icon>
      </div>
      <label class="body-2 ml-4" :for="'fish-egalim-' + diagnostic.year">
        La valeur (en HT) des mes achats EGAlim en poissons et produits aquatiques
      </label>
    </div>
    <v-text-field
      :id="'fish-egalim-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueFishEgalimHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="fishError"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>
  </div>
</template>

<script>
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import labels from "@/data/quality-labels.json"
import validators from "@/validators"
import LogoBio from "@/components/LogoBio"

const DEFAULT_TOTAL_ERROR = "Le totale doit être plus que la somme des valeurs par label"
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

      this.totalError = sumEgalim > total
      this.totalErrorMessage = this.totalError ? `${DEFAULT_TOTAL_ERROR}, actuellement ${sumEgalim || 0} €` : ""

      this.meatPoultryError = sumMeatPoultry > totalMeatPoultry
      this.meatPoultryErrorMessage = this.meatPoultryError
        ? `${DEFAULT_MEAT_POULTRY_ERROR}, actuellement ${sumMeatPoultry || 0} €`
        : ""

      this.fishError = sumFish > totalFish
      this.fishErrorMessage = this.fishError ? `${DEFAULT_FISH_ERROR}, actuellement ${sumFish || 0} €` : ""
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
</style>
