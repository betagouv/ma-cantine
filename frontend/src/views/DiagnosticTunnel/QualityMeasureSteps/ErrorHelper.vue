<template>
  <v-card outlined>
    <v-card-text class="pb-0 d-flex">
      <v-icon>$error-warning-fill</v-icon>
      <p class="ma-0 ml-2">L'erreur de validation pourrait se trouver dans un de ces champs</p>
    </v-card-text>
    <v-card-text>
      <!-- TOTAL -->
      <div class="my-2" v-if="showField('valueTotalHt')">
        <label :for="'total-' + diagnostic.year" class="body-2">
          La valeur (en HT) de mes achats alimentaires total
        </label>

        <DsfrCurrencyField
          :id="'total-' + diagnostic.year"
          v-model.number="diagnostic.valueTotalHt"
          @blur="$emit('check-total')"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueTotalHt"
          @autofill="$emit('check-total')"
          purchaseType="totaux"
          :amount="purchasesSummary.valueTotalHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>

      <!-- BIO -->
      <div class="my-2" v-if="showField('valueBioHt')">
        <label class="body-2" :for="'bio-' + diagnostic.year">
          La valeur (en HT) de mes achats Bio ou en conversion Bio
        </label>
        <DsfrCurrencyField
          :id="'bio-' + diagnostic.year"
          v-model.number="diagnostic.valueBioHt"
          @blur="$emit('check-total')"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueBioHt"
          @autofill="$emit('check-total')"
          purchaseType="bio"
          :amount="purchasesSummary.valueBioHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>

      <!-- SIQO -->
      <div class="my-2" v-if="showField('valueSustainableHt')">
        <label class="body-2" :for="'siqo-' + diagnostic.year">
          La valeur (en HT) de mes achats SIQO (AOP/AOC, IGP, STG, Label Rouge)
        </label>
        <DsfrCurrencyField
          :id="'siqo-' + diagnostic.year"
          v-model.number="diagnostic.valueSustainableHt"
          @blur="$emit('check-total')"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueSustainableHt"
          @autofill="$emit('check-total')"
          purchaseType="SIQO"
          :amount="purchasesSummary.valueSustainableHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>

      <!-- Other EGAlim -->
      <div class="my-2" v-if="showField('valueEgalimOthersHt')">
        <label class="body-2" :for="'other-' + diagnostic.year">
          La valeur (en HT) des autres achats EGAlim
        </label>
        <DsfrCurrencyField
          :id="'other-' + diagnostic.year"
          v-model.number="diagnostic.valueEgalimOthersHt"
          @blur="$emit('check-total')"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueEgalimOthersHt"
          @autofill="$emit('check-total')"
          purchaseType="« autre EGAlim »"
          :amount="purchasesSummary.valueEgalimOthersHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>

      <!-- Performance Externalités -->
      <div class="my-2" v-if="showField('valueExternalityPerformanceHt')">
        <label class="body-2" :for="'ext-perf-' + diagnostic.year">
          Critères d'achat : La valeur (en HT) de mes achats prenant en compte les coûts imputés aux externalités
          environnementales ou acquis sur la base de leurs performances en matière environnementale.
        </label>
        <DsfrCurrencyField
          :id="'ext-perf-' + diagnostic.year"
          v-model.number="diagnostic.valueExternalityPerformanceHt"
          @blur="$emit('check-total')"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueExternalityPerformanceHt"
          @autofill="$emit('check-total')"
          purchaseType="« critères d'achat »"
          :amount="purchasesSummary.valueExternalityPerformanceHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>

      <!-- Viande et volailles -->
      <div class="my-2" v-if="showField('valueMeatPoultryHt')">
        <label class="body-2" :for="'meat-poultry-' + diagnostic.year">
          La valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total
        </label>
        <DsfrCurrencyField
          :id="'meat-poultry-' + diagnostic.year"
          v-model.number="diagnostic.valueMeatPoultryHt"
          @blur="$emit('check-total')"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueMeatPoultryHt"
          @autofill="$emit('check-total')"
          purchaseType="totaux viandes et volailles"
          :amount="purchasesSummary.valueMeatPoultryHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>
      <div class="my-2" v-if="showField('valueMeatPoultryEgalimHt')">
        <label class="body-2" :for="'meat-poultry-egalim-' + diagnostic.year">
          La valeur (en HT) des mes achats EGAlim en viandes et volailles fraiches ou surgelées
        </label>
        <DsfrCurrencyField
          :id="'meat-poultry-egalim-' + diagnostic.year"
          v-model.number="diagnostic.valueMeatPoultryEgalimHt"
          @blur="$emit('check-total')"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueMeatPoultryEgalimHt"
          @autofill="$emit('check-total')"
          purchaseType="viandes et volailles EGAlim"
          :amount="purchasesSummary.valueMeatPoultryEgalimHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>
      <div class="my-2" v-if="showField('valueMeatPoultryFranceHt')">
        <label class="body-2" :for="'meat-poultry-france-' + diagnostic.year">
          La valeur (en HT) des mes achats provenance France en viandes et volailles fraiches ou surgelées
        </label>
        <DsfrCurrencyField
          :id="'meat-poultry-france-' + diagnostic.year"
          v-model.number="diagnostic.valueMeatPoultryFranceHt"
          @blur="$emit('check-total')"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueMeatPoultryFranceHt"
          @autofill="$emit('check-total')"
          purchaseType="viandes et volailles provenance France"
          :amount="purchasesSummary.valueMeatPoultryFranceHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>

      <!-- Poissons -->
      <div class="my-2" v-if="showField('valueFishHt')">
        <label class="body-2" :for="'fish-' + diagnostic.year">
          La valeur (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture total
        </label>
        <DsfrCurrencyField
          :id="'fish-' + diagnostic.year"
          v-model.number="diagnostic.valueFishHt"
          @blur="$emit('check-total')"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueFishHt"
          @autofill="$emit('check-total')"
          purchaseType="totaux de poissons, produits de la mer et de l'aquaculture"
          :amount="purchasesSummary.valueFishHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>
      <div class="my-2" v-if="showField('valueFishEgalimHt')">
        <label class="body-2" :for="'fish-egalim-' + diagnostic.year">
          La valeur (en HT) des mes achats EGAlim en poissons, produits de la mer et de l'aquaculture
        </label>
        <DsfrCurrencyField
          :id="'fish-egalim-' + diagnostic.year"
          v-model.number="diagnostic.valueFishEgalimHt"
          @blur="$emit('check-total')"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="diagnostic.valueFishEgalimHt"
          @autofill="$emit('check-total')"
          purchaseType="poissons, produits de la mer et de l'aquaculture EGAlim"
          :amount="purchasesSummary.valueFishEgalimHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"

export default {
  name: "ErrorHelper",
  components: { DsfrCurrencyField, PurchaseHint },
  props: {
    showFields: {
      type: Array,
      default: () => [],
    },
    diagnostic: {
      type: Object,
      required: true,
    },
    purchasesSummary: {
      type: Object,
    },
  },
  computed: {
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
    },
  },
  methods: {
    showField(fieldName) {
      return this.showFields.indexOf(fieldName) > -1
    },
  },
}
</script>
