<template>
  <v-sheet color="grey lighten-4" class="body-2 px-3 pt-4 pb-1 mt-n3">
    <div v-if="compliant" class="d-flex">
      <v-icon small class="mr-1">mdi-check</v-icon>
      <span>Correspond aux achats réalisés</span>
    </div>
    <div v-else class="d-flex">
      <div>
        {{ visibleLabel }}
        <a color="primary" @click="$emit('input', amount)" class="text-decoration-underline" text>{{ amount }} €</a>
      </div>
      <v-spacer></v-spacer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on" small>mdi-help-circle-outline</v-icon>
        </template>
        <span>{{ helpLabel }}</span>
      </v-tooltip>
    </div>
  </v-sheet>
</template>

<script>
export default {
  name: "PurchaseHint",
  props: {
    shortLabel: {
      type: String,
      default: "Remplir avec",
    },
    label: {
      type: String,
      default: "Remplir avec",
    },
    amount: {
      required: true,
    },
    helpLabel: {
      type: String,
      default: "Ce montant provient des achats que vous avez enregistrés",
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
  border-radius: 0px 0px 12px 12px !important;
}
</style>
