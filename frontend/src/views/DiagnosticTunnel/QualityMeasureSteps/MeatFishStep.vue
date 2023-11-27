<template>
  <div>
    <v-row>
      <v-col cols="12" md="8">
        <div class="d-block d-sm-flex align-center">
          <div class="d-flex">
            <v-icon size="30" color="brown">
              mdi-food-steak
            </v-icon>
            <v-icon size="30" color="brown">
              mdi-food-drumstick
            </v-icon>
          </div>
          <label class="fr-text ml-4" :for="'meat-poultry-' + diagnostic.year">
            La valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total
          </label>
        </div>
        <DsfrCurrencyField
          :id="'meat-poultry-' + diagnostic.year"
          v-model.number="payload.valueMeatPoultryHt"
          @blur="checkTotal"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
          :error="hasError"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueMeatPoultryHt"
          @autofill="checkTotal"
          purchaseType="totaux viandes et volailles"
          :amount="purchasesSummary.valueMeatPoultryHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
        <!-- Poissons -->
        <div class="d-block d-sm-flex align-center mt-8">
          <div class="d-flex">
            <v-icon size="30" color="blue">
              mdi-fish
            </v-icon>
          </div>
          <label class="fr-text ml-4" :for="'fish-' + diagnostic.year">
            La valeur (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture total
          </label>
        </div>
        <DsfrCurrencyField
          :id="'fish-' + diagnostic.year"
          v-model.number="payload.valueFishHt"
          :error="hasError"
          @blur="checkTotal"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload.valueFishHt"
          @autofill="checkTotal"
          purchaseType="totaux de poissons, produits de la mer et de l'aquaculture"
          :amount="purchasesSummary.valueFishHt"
          :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"

export default {
  name: "MeatFishStep",
  components: { DsfrCurrencyField, PurchaseHint },
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
    return {
      totalMeatPoultryError: false,
      meatPoultryError: false,
      totalFamiliesError: false,
      totalMeatPoultryErrorMessage: null,
      meatPoultryErrorMessage: null,
      totalFamiliesErrorMessage: null,
    }
  },
  computed: {
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
    },
  },
  methods: {
    checkTotal() {
      // TODO
    },
  },
}
</script>
