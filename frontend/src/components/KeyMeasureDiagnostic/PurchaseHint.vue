<template>
  <v-sheet color="grey lighten-4" class="body-2 px-3 pt-8 pb-1 mt-n7">
    <div v-if="!amount">
      {{ emptyLabel }}
    </div>
    <div v-else-if="compliant" class="d-flex">
      <v-icon small class="mr-1">mdi-check</v-icon>
      <span>Correspond aux achats réalisés</span>
    </div>
    <div v-else class="d-flex">
      <div>
        {{ visibleLabel }}
        <a color="primary" tabindex="0" @click="$emit('input', amount)" class="text-decoration-underline" text>
          {{ amount }} €
        </a>
      </div>
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
  computed: {
    visibleLabel() {
      return this.$vuetify.breakpoint.smAndDown ? this.shortLabel : this.label
    },
    compliant() {
      return this.value === this.amount
    },
  },
}
</script>

<style scoped>
.v-sheet {
  border-radius: 12px !important;
}
</style>
