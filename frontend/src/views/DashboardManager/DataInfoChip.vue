<template>
  <v-chip
    color="primary lighten-5"
    class="blue--text text--darken-4"
    style="border-radius: 4px !important;"
    small
    label
    v-if="body"
  >
    <v-icon small class="mr-2">$information-fill</v-icon>
    <p class="ma-0 pa-0">{{ body }}</p>
  </v-chip>
  <span v-else></span>
</template>
<script>
export default {
  name: "DataInfoChip",
  props: {
    currentYear: {
      default: false,
      type: Boolean,
    },
    missingData: {
      default: false,
      type: Boolean,
    },
  },
  computed: {
    body() {
      if (this.currentYear) return "ANNÉE EN COURS"
      if (this.missingData) return "DONNÉES À COMPLETER"
      return null
    },
  },
}
</script>
