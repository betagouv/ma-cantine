<template>
  <v-dialog v-model="isOpen" max-width="900">
    <!-- maybe make dialog fullscreen for xs (and s) ? -->
    <!-- TODO: add visualisation of canteen count if passed diagnostics array -->
    <SingleView :canteen="canteenForTD" :diagnostic="diagnosticForTD" @teledeclare="teledeclare" @close="close" />
  </v-dialog>
</template>

<script>
import SingleView from "./SingleView"

export default {
  components: { SingleView },
  props: {
    value: {
      required: true,
    },
    diagnostic: Object,
    canteen: Object,
    diagnostics: Array,
  },
  data() {
    return {
      idx: 0,
    }
  },
  computed: {
    isOpen: {
      get() {
        return this.value
      },
      set(newValue) {
        this.$emit("input", newValue)
      },
    },
    canteenForTD() {
      return this.canteen || this.diagnosticForTD?.canteen
    },
    diagnosticForTD() {
      return this.diagnostic || this.diagnostics[this.idx]
    },
  },
  methods: {
    teledeclare() {
      // TODO: handle multi teledeclarations
      this.$emit("teledeclare")
    },
    close() {
      this.$emit("input", false)
    },
  },
}
</script>
