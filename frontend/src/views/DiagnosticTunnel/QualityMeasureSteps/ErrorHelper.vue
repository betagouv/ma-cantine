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
          v-model.number="payload.valueTotalHt"
          @blur="$emit('update-payload', payload)"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueTotalHt"
          @autofill="$emit('update-payload', payload)"
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
          v-model.number="payload.valueBioHt"
          @blur="$emit('update-payload', payload)"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueBioHt"
          @autofill="$emit('update-payload', payload)"
          purchaseType="bio"
          :amount="purchasesSummary.valueBioHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </div>

      <!-- SIQO -->
      <div class="my-2" v-if="showField('valueSustainableHt')">
        <label class="fr-text-sm" for="siqo">
          La valeur (en HT) de mes achats SIQO (Label Rouge, AOC / AOP, IGP, STG)
        </label>
        <DsfrCurrencyField
          id="siqo"
          v-model.number="payload.valueSustainableHt"
          @blur="$emit('update-payload', payload)"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueSustainableHt"
          @autofill="$emit('update-payload', payload)"
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
          v-model.number="payload.valueEgalimOthersHt"
          @blur="$emit('update-payload', payload)"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueEgalimOthersHt"
          @autofill="$emit('update-payload', payload)"
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
          v-model.number="payload.valueExternalityPerformanceHt"
          @blur="$emit('update-payload', payload)"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueExternalityPerformanceHt"
          @autofill="$emit('update-payload', payload)"
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
          v-model.number="payload.valueMeatPoultryHt"
          @blur="$emit('update-payload', payload)"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryHt"
          @autofill="$emit('update-payload', payload)"
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
          v-model.number="payload.valueMeatPoultryEgalimHt"
          @blur="$emit('update-payload', payload)"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryEgalimHt"
          @autofill="$emit('update-payload', payload)"
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
          v-model.number="payload.valueMeatPoultryFranceHt"
          @blur="$emit('update-payload', payload)"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryFranceHt"
          @autofill="$emit('update-payload', payload)"
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
          v-model.number="payload.valueFishHt"
          @blur="$emit('update-payload', payload)"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueFishHt"
          @autofill="$emit('update-payload', payload)"
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
          v-model.number="payload.valueFishEgalimHt"
          @blur="$emit('update-payload', payload)"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueFishEgalimHt"
          @autofill="$emit('update-payload', payload)"
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
  data() {
    const payload = {}
    this.showFields.forEach((field) => {
      payload[field] = this.diagnostic[field]
    })
    return {
      payload,
    }
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
