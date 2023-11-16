<template>
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
        <label class="body-2 ml-4" :for="'meat-poultry-' + diagnostic.year">
          La valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total
        </label>
      </div>
      <DsfrCurrencyField
        :id="'meat-poultry-' + diagnostic.year"
        v-model.number="payload.valueMeatPoultryHt"
        @blur="checkTotal"
        :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
      />
      <PurchaseHint
        v-if="displayPurchaseHints"
        v-model="payload.valueMeatPoultryHt"
        @autofill="checkTotal"
        purchaseType="totaux viandes et volailles"
        :amount="purchasesSummary.valueMeatPoultryHt"
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
        v-model.number="payload.valueMeatPoultryEgalimHt"
        :error="meatPoultryError"
        @blur="checkTotal"
        :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
      />
      <PurchaseHint
        v-if="displayPurchaseHints"
        v-model="payload.valueMeatPoultryEgalimHt"
        @autofill="checkTotal"
        purchaseType="viandes et volailles EGAlim"
        :amount="purchasesSummary.valueMeatPoultryEgalimHt"
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
        v-model.number="payload.valueMeatPoultryFranceHt"
        :error="meatPoultryError"
        @blur="checkTotal"
        :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
      />
      <PurchaseHint
        v-if="displayPurchaseHints"
        v-model="payload.valueMeatPoultryFranceHt"
        @autofill="checkTotal"
        purchaseType="viandes et volailles provenance France"
        :amount="purchasesSummary.valueMeatPoultryFranceHt"
        :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
      />
    </v-col>
  </v-row>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"

export default {
  name: "MeatPoultryStep",
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
      totalError: false,
      meatPoultryError: false,
      totalErrorMessage: "",
    }
  },
  computed: {
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x)
    },
  },
  methods: {
    updatePayload() {
      this.$emit("update-payload", { payload: this.payload })
    },
    checkTotal() {
      return true
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
}
</script>

<style scoped>
.left-border {
  border-left: solid #4d4db2;
}
</style>
