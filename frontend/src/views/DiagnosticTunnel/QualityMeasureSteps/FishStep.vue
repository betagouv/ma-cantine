<template>
  <v-row>
    <v-col cols="12" md="8">
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
        v-model.number="payload.valueFishHt"
        :error="fishError || totalFishError"
        :messages="fishError || totalFishError ? [fishErrorMessage] : undefined"
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
        v-model.number="payload.valueFishEgalimHt"
        :error="fishError"
        @blur="checkTotal"
        :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
      />
      <PurchaseHint
        v-if="displayPurchaseHints"
        v-model="payload.valueFishEgalimHt"
        @autofill="checkTotal"
        purchaseType="poissons, produits de la mer et de l'aquaculture EGAlim"
        :amount="purchasesSummary.valueFishEgalimHt"
        :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
      />
    </v-col>
  </v-row>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"

export default {
  name: "FishStep",
  components: { DsfrCurrencyField },
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
      // TODO Add purchase summaries
      type: Object,
    },
  },
  data() {
    return {
      totalError: false,
      fishError: false,
      totalFishError: false,
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
