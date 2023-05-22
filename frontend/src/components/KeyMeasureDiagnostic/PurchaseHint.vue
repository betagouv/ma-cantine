<template>
  <v-sheet :color="backgroundColor" class="body-2 pr-3 pt-10 pb-1 mt-n9">
    <p class="mb-0 caption pl-3" v-if="!amount">
      {{ emptyLabel }}
    </p>
    <p class="mb-0 caption d-flex pl-3" v-else-if="compliant">
      <v-icon small class="mr-1">mdi-check</v-icon>
      <span>Correspond aux achats réalisés</span>
    </p>
    <v-row v-else align="center">
      <v-col cols="11" class="mx-0">
        <v-btn tabindex="0" @click="onFill" class="hint py-1" text>
          <span>
            <span class="font-weight-medium grey--text text--darken-3">{{ visibleLabel }}&nbsp;</span>
            <span class="text-decoration-underline primary--text text--darken-1">{{ toCurrency(amount) }}</span>
          </span>
        </v-btn>
      </v-col>
      <v-col cols="1" class="text-right mx-0">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon tabindex="0" v-bind="attrs" v-on="on" small>mdi-help-circle-outline</v-icon>
          </template>
          <span>{{ helpLabel }}</span>
        </v-tooltip>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script>
import { toCurrency } from "@/utils"

export default {
  name: "PurchaseHint",
  data() {
    return {
      shortLabel: "Remplir avec",
      label: `Remplir les achats ${this.purchaseType} avec`,
      helpLabel: `Ce montant provient des achats ${this.purchaseType} que vous avez enregistrés`,
      emptyLabel: `Vous n'avez pas d'achats ${this.purchaseType}`,
    }
  },
  props: {
    purchaseType: {
      type: String,
    },
    amount: {
      required: true,
    },
    value: {
      required: true,
    },
  },
  methods: {
    onFill() {
      this.$emit("input", this.amount)
      this.$emit("autofill")
    },
    toCurrency(value) {
      return toCurrency(value)
    },
  },
  computed: {
    visibleLabel() {
      // TODO: for screen readers only don't shorten label ever?
      return this.$vuetify.display.smAndDown ? this.shortLabel : this.label
    },
    compliant() {
      return this.value === this.amount
    },
    backgroundColor() {
      return !this.amount || this.compliant ? "grey lighten-4" : "primary lighten-5"
    },
  },
}
</script>

<style scoped>
.v-sheet {
  border-radius: 0 0 12px 12px !important;
}
.hint {
  max-width: 100%;
  height: auto !important;
  display: block;
  text-align: left;
  white-space: normal;
  word-wrap: break-word;
}
.hint > span {
  max-width: 100%;
}
</style>
