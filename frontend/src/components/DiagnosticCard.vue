<template>
  <v-card
    class="d-flex"
    :to="{ name: 'DiagnosticModification', params: { canteenUrlComponent, year: diagnostic.year } }"
  >
    <v-sheet color="grey lighten-4" width="150" class="d-flex flex-column justify-center px-4">
      <div class="text-h3 grey--text font-weight-black text-center">{{ diagnostic.year }}</div>
    </v-sheet>
    <div>
      <v-card-title class="font-weight-bold">{{ canteen.name }}</v-card-title>
      <v-card-text>Dernière modification {{ timeAgo(diagnostic.modificationDate, true) }}</v-card-text>
    </div>
  </v-card>
</template>

<script>
import { timeAgo } from "@/utils"

export default {
  name: "DiagnosticCard",
  props: {
    diagnostic: {
      type: Object,
      required: true,
    },
  },
  computed: {
    canteen() {
      return this.$store.state.userCanteens.find((canteen) =>
        canteen.diagnostics.some((diagnostic) => diagnostic.id === this.diagnostic.id)
      )
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
    dataStatus() {
      return {
        PUBLISHED: "Données complètées, sauvegardées, et publiées",
        INCOMPLETE: "Données incomplètées",
      }[this.diagnostic.status]
    },
  },
  methods: {
    timeAgo: timeAgo,
  },
}
</script>

<style scoped>
.v-sheet {
  border-radius: 0;
}
</style>
