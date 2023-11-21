<template>
  <v-card outlined>
    <v-card-text class="pb-0 d-flex">
      <v-icon>$error-warning-fill</v-icon>
      <p class="ma-0 ml-2">L'erreur de validation pourrait se trouver dans un de ces champs</p>
    </v-card-text>
    <v-card-text>
      <!-- TOTAL -->
      <div class="my-2" v-if="showField('valueTotalHt')">
        <label for="total" class="fr-text-sm">
          La valeur (en HT) de mes achats alimentaires total
        </label>

        <DsfrCurrencyField
          id="total"
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
        <label class="fr-text-sm" for="bio">
          La valeur (en HT) de mes achats Bio ou en conversion Bio
        </label>
        <DsfrCurrencyField
          id="bio"
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
        <label class="fr-text-sm" for="siqo">
          La valeur (en HT) de mes achats SIQO (AOP/AOC, IGP, STG, Label Rouge)
        </label>
        <DsfrCurrencyField
          id="siqo"
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
        <label class="fr-text-sm" for="other">
          La valeur (en HT) des autres achats EGAlim
        </label>
        <DsfrCurrencyField
          id="other"
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
        <label class="fr-text-sm" for="ext-perf">
          Critères d'achat : La valeur (en HT) de mes achats prenant en compte les coûts imputés aux externalités
          environnementales ou acquis sur la base de leurs performances en matière environnementale.
        </label>
        <DsfrCurrencyField
          id="ext-perf"
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
        <label class="fr-text-sm" for="meat-poultry">
          La valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total
        </label>
        <DsfrCurrencyField
          id="meat-poultry"
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
        <label class="fr-text-sm" for="meat-poultry-egalim">
          La valeur (en HT) des mes achats EGAlim en viandes et volailles fraiches ou surgelées
        </label>
        <DsfrCurrencyField
          id="meat-poultry-egalim"
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
        <label class="fr-text-sm" for="meat-poultry-france">
          La valeur (en HT) des mes achats provenance France en viandes et volailles fraiches ou surgelées
        </label>
        <DsfrCurrencyField
          id="meat-poultry-france"
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
        <label class="fr-text-sm" for="fish">
          La valeur (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture total
        </label>
        <DsfrCurrencyField
          id="fish"
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
        <label class="fr-text-sm" for="fish-egalim">
          La valeur (en HT) des mes achats EGAlim en poissons, produits de la mer et de l'aquaculture
        </label>
        <DsfrCurrencyField
          id="fish-egalim"
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
      return !!this.purchasesSummary
    },
  },
  methods: {
    showField(fieldName) {
      return this.showFields.indexOf(fieldName) > -1
    },
  },
}
</script>
