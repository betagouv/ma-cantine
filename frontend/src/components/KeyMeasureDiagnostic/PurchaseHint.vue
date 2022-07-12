<template>
  <v-sheet :color="backgroundColor" class="body-2 px-3 pt-8 pb-1 mt-n7">
    <p class="mb-0 caption" v-if="!amount">
      {{ emptyLabel }}
    </p>
    <p class="mb-0 caption d-flex" v-else-if="compliant">
      <v-icon small class="mr-1">mdi-check</v-icon>
      <span>Correspond aux achats réalisés</span>
    </p>
    <div v-else class="d-flex">
      <p class="mb-0">
        {{ visibleLabel }}
        <a color="primary" tabindex="0" @click="onFill" class="text-decoration-underline font-weight-bold" text>
          {{ amount }} €
        </a>
      </p>
      <v-spacer></v-spacer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon tabindex="0" v-bind="attrs" v-on="on" small>mdi-help-circle-outline</v-icon>
        </template>
        <span>{{ helpLabel }}</span>
      </v-tooltip>
    </div>
  </v-sheet>
</template>

<script>
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
  },
  computed: {
    visibleLabel() {
      return this.$vuetify.breakpoint.smAndDown ? this.shortLabel : this.label
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
  border-radius: 12px !important;
}
</style>
